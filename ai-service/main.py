from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from llm import llm_findings
from retrieval import retrieve_sources, source_catalog
import re
load_dotenv()
app=FastAPI(title='TRUST MARK Compliance Service')
class AnalyzeRequest(BaseModel):
    text:str
    guidelines:dict

def finding(index,kind,risk,snippet,explanation,guideline,evidence,suggestion,source_id):
    return dict(id=f'r{index}',type=kind,risk=risk,snippet=snippet,explanation=explanation,guideline=guideline,evidence=evidence,suggestion=suggestion,sourceId=source_id,decision='open')

@app.get('/health')
def health():return {'status':'ok'}

@app.post('/analyze')
async def analyze(request:AnalyzeRequest):
    text=request.text[:20000];g=request.guidelines;results=[]
    for i,term in enumerate(g.get('bannedTerms',[])):
        bad,good=str(term.get('term','')).strip(),str(term.get('replacement','')).strip()
        if not bad:continue
        for m in re.finditer(r'(?<!\w)'+re.escape(bad)+r'(?!\w)',text,re.I):
            results.append(finding(len(results)+1,'Terminology','medium',m.group(),f'Use approved term “{good}” instead.','Approved terminology',f'Banned: {bad}; preferred: {good}',good or m.group(),f'term:{i}'))
    for i,fact in enumerate(g.get('facts',[])):
        wrong,right=str(fact.get('incorrect','')).strip(),str(fact.get('approved','')).strip()
        if wrong and right:
            for m in re.finditer(re.escape(wrong),text,re.I):
                results.append(finding(len(results)+1,'Outdated fact','high',m.group(),'This value differs from the approved fact.',fact.get('source','Approved facts'),f'Approved value: {right}',right,f'fact:{i}'))
    patterns=[r'\bguaranteed results\b',r'\b100\s*%\s*secure\b',r'\bthe fastest\b',r'\bmost secure\b',r'\bclinically proven\b']
    for pattern in patterns:
        for m in re.finditer(pattern,text,re.I):
            results.append(finding(len(results)+1,'Unsupported claim','high',m.group(),'This strong claim needs evidence; no benchmark is attached.','Claims policy','No approved evidence supplied for this claim.','designed for reliable performance','claimsPolicy'))
    sources=retrieve_sources(text,g)
    extra,mode,warning=await llm_findings(text,g,sources)
    existing={(x['type'],x['snippet'].lower()) for x in results}
    for item in extra:
        if (item['type'],item['snippet'].lower()) not in existing:
            item['id']=f'ai-{len(results)+1}';item['decision']='open';results.append(item)
    for f in results:
        source=source_catalog(g).get(f.get('sourceId'))
        f['sourceExcerpt']=source['text'] if source else 'No approved evidence attached; manual verification required.'
        f['evidenceStatus']='approved-source' if source and f['type']!='Unsupported claim' else 'unverified-claim' if f['type']=='Unsupported claim' else 'missing-source'
    high=sum(1 for f in results if f['risk']=='high'); medium=sum(1 for f in results if f['risk']=='medium'); low=sum(1 for f in results if f['risk']=='low')
    score=max(0,100-20*high-10*medium-5*low)
    return {'findings':results,'mode':mode,'warning':warning,'score':score,'scoreFormula':'max(0, 100 - 20 × high - 10 × medium - 5 × low)','retrievedSources':sources,'disclaimer':'Heuristic review score, not a guarantee of legal or brand compliance. All findings require human review.'}
