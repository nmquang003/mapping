import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from vercel_api import AtlasHandler, validate


class HandlerTests(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), AtlasHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def request(self, path, body=None, origin=None):
        headers = {'Content-Type': 'application/json'}
        if origin:
            headers['Origin'] = origin
        request = urllib.request.Request(self.url+path,
            data=json.dumps(body).encode() if body is not None else None, headers=headers)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            return response.status, json.load(response), response.headers

    @patch('vercel_api.get_rag')
    def test_status_and_valid_chat(self, get_rag):
        get_rag.return_value.status.return_value = {'ready': True, 'provider': 'btc'}
        get_rag.return_value.answer.return_value = {'answer': 'Tam Cốc', 'sources': []}
        status, body, headers = self.request('/api/status')
        self.assertEqual((status, body['provider']), (200, 'btc'))
        self.assertEqual(headers['Cache-Control'], 'no-store')
        status, body, _ = self.request('/api/chat', {'question': ' Tam Cốc ', 'dataset_id': 'ninh-binh'}, self.url)
        self.assertEqual(status, 200)
        get_rag.return_value.answer.assert_called_once_with('Tam Cốc', 'ninh-binh', [])

    @patch('vercel_api.get_rag')
    def test_rejected_inputs_never_call_ai(self, get_rag):
        for body in [[], {'question': ''}, {'question': 'x'*1501},
                     {'question': 'x', 'history': [{'role': 'system', 'content': 'x'}]},
                     {'question': 'x', 'dataset_id': []}]:
            self.assertEqual(self.request('/api/chat', body, self.url)[0], 400)
        self.assertEqual(self.request('/api/chat', {'question': 'x'}, 'https://other.example')[0], 403)
        get_rag.assert_not_called()

    @patch('vercel_api.get_rag', side_effect=RuntimeError('secret must never escape'))
    def test_errors_do_not_expose_credentials(self, get_rag):
        for path, body in [('/api/status', None), ('/api/chat', {'question': 'x'})]:
            status, payload, _ = self.request(path, body, self.url)
            self.assertEqual(status, 503)
            self.assertNotIn('secret', json.dumps(payload))


if __name__ == '__main__':
    unittest.main()
