"""Transparent token-overlap retrieval for the hackathon. Not vector/semantic RAG."""
import re
def source_catalog(g):
    sources={}
    for i,t in enumerate(g.get('bannedTerms',[])):
        sources[f'term:{i}']={'sourceId':f'term:{i}','text':f"Avoid '{t.get('term','')}', use '{t.get('replacement','')}'."}
    for i,f in enumerate(g.get('facts',[])):
        sources[f'fact:{i}']={'sourceId':f'fact:{i}','text':f"Approved: {f.get('approved','')}; outdated: {f.get('incorrect','')}; reference: {f.get('source','Unspecified')}"}
    for key in ('tone','claimsPolicy'):
        if g.get(key):sources[key]={'sourceId':key,'text':str(g[key])}
    return sources
def retrieve_sources(text,g,limit=12):
    words=set(re.findall(r'[a-z0-9]+',text.lower()))
    ranked=[]
    for source in source_catalog(g).values():
        tokens=set(re.findall(r'[a-z0-9]+',source['text'].lower()))
        overlap=len(words&tokens)
        if overlap:ranked.append((overlap,source))
    ranked.sort(key=lambda x:-x[0])
    selected=[s for _,s in ranked[:limit]]
    for key in ('tone','claimsPolicy'):
        source=source_catalog(g).get(key)
        if source and source not in selected:selected.append(source)
    return selected
