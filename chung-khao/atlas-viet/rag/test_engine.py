"""Deterministic checks of indexing, scope routing and citation fail-closed behavior."""
import json
import tempfile
import unittest
from pathlib import Path
from engine import RAG, Gateway, load_corpus, unit_vector


class FakeGateway:
    key = 'test-only'
    base = 'mock://btc'
    embedding_model = 'text-multilingual-embedding-002'
    chat_model = 'mock'
    def __init__(self, replies=None):
        self.replies = list(replies or [])
        self.embedded = 0
    def embed(self,texts):
        self.embedded += len(texts)
        return [[1.0]+[0.0]*767 for _ in texts]
    def json_chat(self,instruction,payload):
        return self.replies.pop(0)


class RAGTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.gateway = FakeGateway()
        self.rag = RAG(self.gateway,Path(self.temp.name)/'index.json')
        self.rag.build_index()
    def tearDown(self):
        self.temp.cleanup()
    def route(self, **overrides):
        return {'scope':'in_scope','dataset_ids':['ninh-binh'],'entity_ids':['hoa-lu'],
                'query':'Hoa Lư trong lịch sử','requires_current':False,**overrides}
    def test_readonly_corpus(self):
        docs,datasets=load_corpus()
        self.assertEqual(len(docs),142)
        self.assertEqual(len(set(d['id'] for d in docs)),142)
        self.assertEqual(set(datasets),{'ninh-binh','ha-noi','quang-ninh','lao-cai'})
        for d in docs:
            self.assertTrue(d['sources'])
            self.assertIn(d['status'],['source_checked','dated_reference'])
            self.assertNotEqual(d['kind'],'practical')
            self.assertTrue(all(s['status']=='source_checked' for s in d['sources']))
    def test_cache_reuse_and_model_change(self):
        self.assertEqual(self.rag.build_index()['embedded_now'],0)
        self.gateway.embedding_model='text-embedding-005'
        self.assertEqual(self.rag.build_index()['embedded_now'],142)
    def test_scope_retrieval(self):
        records=self.rag.retrieve('Hoa Lư', ['ninh-binh'],['hoa-lu'])
        self.assertTrue(records)
        self.assertTrue(all(d['dataset_id']=='ninh-binh' and d['entity_id'] in ['hoa-lu','ninh-binh'] for d in records))
    def test_out_of_scope_no_embedding(self):
        before=self.gateway.embedded
        self.gateway.replies=[self.route(scope='out_of_scope')]
        self.assertEqual(self.rag.answer('Huế?')['status'],'out_of_scope')
        self.assertEqual(self.gateway.embedded,before)
    def test_current_info_is_not_published(self):
        self.gateway.replies=[self.route(requires_current=True)]
        self.assertEqual(self.rag.answer('Giá vé hôm nay?')['status'],'insufficient_data')
    def test_unknown_dataset(self):
        self.assertEqual(self.rag.answer('Địa lý', 'hue')['status'],'out_of_scope')
    def test_unknown_route_id(self):
        self.gateway.replies=[self.route(entity_ids=['unknown'])]
        self.assertEqual(self.rag.answer('Nơi khác?')['status'],'insufficient_data')
    def test_fabricated_citation_rejected(self):
        self.gateway.replies=[self.route(),{'supported':True,'claims':[{'text':'Sai','record_ids':['ha-noi:F01']}]}]
        result=self.rag.answer('Hoa Lư')
        self.assertEqual(result['status'],'insufficient_data')
        self.assertFalse(result['sources'])
    def test_unentailed_claim_rejected(self):
        self.gateway.replies=[self.route(),{'supported':True,'claims':[{'text':'Năm 1000','record_ids':['ninh-binh:F09']}]},{'supported':False}]
        self.assertEqual(self.rag.answer('Hoa Lư')['status'],'insufficient_data')
    def test_valid_citations_resolve_from_db(self):
        self.gateway.replies=[self.route(),{'supported':True,'claims':[{'text':'Năm 968, Đinh Bộ Lĩnh chọn Hoa Lư làm kinh đô.','record_ids':['ninh-binh:F09']}]},{'supported':True,'record_ids_per_claim':[['ninh-binh:F09']]}]
        result=self.rag.answer('Hoa Lư')
        self.assertEqual(result['status'],'answered')
        self.assertEqual(result['sources'][0]['id'],'ninh-binh:S05')
        self.assertTrue(result['sources'][0]['url'].startswith('https://'))
    def test_model_two_single_requests(self):
        gateway=Gateway()
        gateway.embedding_model='gemini-embedding-2'
        batches=[]
        def request(path,payload):
            batches.append(payload['input'])
            return {'data':[{'index':0,'embedding':[1]+[0]*3071}]}
        gateway.request=request
        self.assertEqual(len(gateway.embed(['một','hai'])),2)
        self.assertEqual(batches,[['một'],['hai']])
    def test_bad_vectors_rejected(self):
        for vector in [[0]*768,[float('nan')]*768,[1]*767]:
            with self.assertRaises(ValueError):unit_vector(vector,768)


if __name__=='__main__':
    unittest.main()
