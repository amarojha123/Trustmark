import unittest
from retrieval import retrieve_sources,source_catalog
class TestRetrieval(unittest.TestCase):
 def test_sources(self):
  g={'facts':[{'incorrect':'5 million','approved':'3.2 million','source':'Report'}],'bannedTerms':[{'term':'app','replacement':'platform'}],'claimsPolicy':'Superlatives need evidence'}
  self.assertIn('fact:0',source_catalog(g))
  self.assertIn('claimsPolicy',[x['sourceId'] for x in retrieve_sources('fastest app with 5 million customers',g)])
if __name__=='__main__':unittest.main()
