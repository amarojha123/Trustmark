"""Offline, reproducible labelled smoke evaluation of the deterministic checks."""
import asyncio
from main import analyze, AnalyzeRequest

G={'brand':'Acme Cloud','tone':'Clear and factual','claimsPolicy':'Superlatives require approved evidence.','bannedTerms':[{'term':'app','replacement':'platform'}],'facts':[{'incorrect':'5 million','approved':'3.2 million','source':'Approved customer report'}]}
CASES=[
 ('Our app is useful.',{'Terminology'}),
 ('We serve 5 million customers.',{'Outdated fact'}),
 ('The fastest platform.',{'Unsupported claim'}),
 ('Our platform is easy to use.',set()),
 ('Guaranteed results for everyone.',{'Unsupported claim'}),
 ('Trusted by 3.2 million customers.',set()),
 ('The app has 5 million users.',{'Terminology','Outdated fact'}),
 ('We provide reliable support.',set()),
 ('Our platform is 100% secure.',{'Unsupported claim'}),
 ('A friendly and helpful service.',set()),
]
async def main():
    tp=fp=fn=0
    for text,expected in CASES:
        response=await analyze(AnalyzeRequest(text=text,guidelines=G))
        actual={f['type'] for f in response['findings']}
        tp+=len(actual&expected);fp+=len(actual-expected);fn+=len(expected-actual)
        print(('PASS' if actual==expected else 'FAIL'),text, 'expected=',sorted(expected),'actual=',sorted(actual))
    precision=tp/(tp+fp) if tp+fp else 0
    recall=tp/(tp+fn) if tp+fn else 0
    print(f'Precision={precision:.3f} Recall={recall:.3f} TP={tp} FP={fp} FN={fn}')
    print('Note: 10 synthetic cases, not representative production accuracy. Gemini output may vary.')
if __name__=='__main__':asyncio.run(main())
