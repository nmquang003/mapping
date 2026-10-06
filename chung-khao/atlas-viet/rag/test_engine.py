"""Deterministic checks of indexing, scope routing and citation fail-closed behavior."""
import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from engine import RAG, Gateway, load_corpus, unit_vector
from config import load_env


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
    def test_province_travel_retrieves_landmark_profiles(self):
        records = self.rag.retrieve('Tràng An', ['ninh-binh'], ['ninh-binh'], limit=100)
        self.assertTrue(any(d['entity_id'] == 'trang-an' for d in records))
        self.assertTrue(all(d['dataset_id'] == 'ninh-binh' for d in records))
    def test_out_of_scope_no_embedding(self):
        before=self.gateway.embedded
        self.gateway.replies=[self.route(scope='out_of_scope')]
        self.assertEqual(self.rag.answer('Huế?')['status'],'out_of_scope')
        self.assertEqual(self.gateway.embedded,before)
    def test_current_info_is_not_published(self):
        self.gateway.replies=[self.route(requires_current=True)]
        self.assertEqual(self.rag.answer('Giá vé hôm nay?')['status'],'insufficient_data')
    def test_guide_greeting_needs_no_embedding(self):
        before = self.gateway.embedded
        self.gateway.replies = [self.route(scope='conversation')]
        result = self.rag.answer('Chào bạn!', 'ninh-binh')
        self.assertEqual(result['status'], 'conversation')
        self.assertIn('hướng dẫn viên', result['answer'])
        self.assertIn('Ninh Bình', result['answer'])
        self.assertEqual(self.gateway.embedded, before)
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
        self.assertTrue(any(image['id']=='hoa-lu' for image in result['illustrations']))
    def test_illustrations_match_cited_landmark(self):
        images = self.rag.illustrations_for('Khám phá Tràng An.', [{'record_ids':['ninh-binh:F07']}])
        self.assertTrue(images)
        self.assertEqual(images[0]['id'], 'trang-an')
        self.assertTrue(all(image['src'].startswith('assets/ai/ninh-binh/') for image in images))
        self.assertTrue(all((Path(__file__).resolve().parents[1]/'dist'/image['src']).is_file() for image in images))
        self.assertEqual(self.rag.illustrations_for('Cho xem ảnh Tràng An.', []), [])
    def test_missing_optional_images_leave_text_available(self):
        self.rag.illustrations = []
        self.gateway.replies = [self.route(entity_ids=['trang-an']),
            {'supported':True,'claims':[{'text':'Tràng An có cảnh quan núi đá vôi.','record_ids':['ninh-binh:F07']}]},
            {'supported':True,'record_ids_per_claim':[['ninh-binh:F07']]}]
        result = self.rag.answer('Cho xem ảnh minh họa Tràng An.')
        self.assertEqual(result['status'], 'answered')
        self.assertEqual(result['illustrations'], [])
        self.assertIn('chưa có ảnh', result['illustration_note'])
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


class ConfigurationTests(unittest.TestCase):
    def test_dotenv_precedence_and_allowlist(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict('os.environ', {'ATLAS_PROVIDER':'btc'}, clear=True):
            local, root = Path(directory)/'local.env', Path(directory)/'root.env'
            local.write_text('OPENROUTER_API_KEY="local-test"\nATLAS_PROVIDER=openrouter\nOTHER_SECRET=ignored\n')
            root.write_text('OPENROUTER_API_KEY=root-test\nATLAS_CHAT_MODEL=deepseek-flash # model\n')
            load_env([local, root])
            import os
            self.assertEqual(os.environ['OPENROUTER_API_KEY'], 'local-test')
            self.assertEqual(os.environ['ATLAS_PROVIDER'], 'btc')
            self.assertEqual(os.environ['ATLAS_CHAT_MODEL'], 'deepseek-flash')
            self.assertNotIn('OTHER_SECRET', os.environ)

    @patch('engine.load_env')
    def test_openrouter_uses_own_key_models_and_paths(self, load):
        with patch.dict('os.environ', {'OPENROUTER_API_KEY':'router-test', 'THUCCHIEN_API_KEY':'btc-test',
                                     'ATLAS_CHAT_MODEL':'deepseek-flash', 'ATLAS_EMBEDDING_MODEL':'text-multilingual-embedding-002'}, clear=True):
            gateway = Gateway()
        self.assertEqual(gateway.key, 'router-test')
        self.assertEqual(gateway.base, 'https://openrouter.ai/api/v1')
        self.assertEqual(gateway.embedding_model, 'openai/text-embedding-3-small')
        calls = []
        def request(path, payload):
            calls.append((path, payload))
            if path == '/embeddings':
                return {'data':[{'index':0, 'embedding':[1]+[0]*1535}]}
            return {'choices':[{'message':{'content':'{"supported":true}'}}]}
        gateway.request = request
        self.assertEqual(len(gateway.embed(['Ninh Bình'])[0]), 1536)
        self.assertTrue(gateway.json_chat('Return JSON.', {})['supported'])
        self.assertEqual([call[0] for call in calls], ['/embeddings', '/chat/completions'])
        self.assertEqual(calls[1][1]['response_format'], {'type':'json_object'})
        self.assertNotIn('thinking', calls[1][1])
        gateway.json_chat('Cite the provided records.', {'allowed_record_ids':['ninh-binh:F07']})
        format = calls[-1][1]['response_format']
        self.assertEqual(format['type'], 'json_schema')
        self.assertEqual(format['json_schema']['schema']['properties']['claims']['items']['properties']['record_ids']['items']['enum'], ['ninh-binh:F07'])

    @patch('engine.load_env')
    def test_explicit_btc_switch(self, load):
        with patch.dict('os.environ', {'ATLAS_PROVIDER':'btc', 'OPENROUTER_API_KEY':'router-test',
                                     'THUCCHIEN_API_KEY':'btc-test'}, clear=True):
            gateway = Gateway()
        self.assertEqual(gateway.provider, 'btc')
        self.assertEqual(gateway.key, 'btc-test')
        self.assertEqual(gateway.chat_path, '/v1/chat/completions')

    @patch('engine.load_env')
    def test_invalid_upstream_emoji_cannot_break_http(self, load):
        with patch.dict('os.environ', {'OPENROUTER_API_KEY':'router-test'}, clear=True):
            gateway = Gateway()
        gateway.request = lambda path, payload: {'choices':[{'message':{'content':'{"text":"hello \\ud83d"}'}}]}
        result = gateway.json_chat('Return JSON.', {})
        self.assertTrue(json.dumps(result, ensure_ascii=False).encode('utf-8'))


if __name__=='__main__':
    unittest.main()
