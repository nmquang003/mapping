"""Same-origin Atlas API; credentials stay in Vercel environment variables."""
import json
import os
import shutil
import threading
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('ATLAS_DATA_ROOT', str(ROOT/'data'))
from engine import RAG

_rag = None
_lock = threading.Lock()
_slots = threading.BoundedSemaphore(2)


def get_rag():
    global _rag
    with _lock:
        if _rag is None:
            cache = Path('/tmp/atlas-rag/index-btc.json')
            cache.parent.mkdir(parents=True, exist_ok=True)
            if not cache.exists():
                shutil.copy2(ROOT/'rag/index-btc.json', cache)
            candidate = RAG(cache_path=cache)
            candidate.build_index()
            _rag = candidate
    return _rag


def validate(body):
    if not isinstance(body, dict):
        raise ValueError('Dữ liệu câu hỏi không hợp lệ.')
    question = body.get('question')
    if not isinstance(question, str) or not 1 <= len(question.strip()) <= 1500:
        raise ValueError('Câu hỏi cần có từ 1 đến 1500 ký tự.')
    history = body.get('history', [])
    if not isinstance(history, list) or len(history) > 6 or any(
        not isinstance(r, dict) or r.get('role') not in ('user', 'assistant')
        or not isinstance(r.get('content'), str) or len(r['content']) > 4000 for r in history
    ):
        raise ValueError('Lịch sử hội thoại không hợp lệ.')
    selected = body.get('dataset_id')
    if selected is not None and not isinstance(selected, str):
        raise ValueError('Địa phương không hợp lệ.')
    return question.strip(), selected, history


class AtlasHandler(BaseHTTPRequestHandler):
    def respond(self, status, value):
        content = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if urlparse(self.path).path != '/api/status':
            self.respond(405, {'error': 'Phương thức không được hỗ trợ.'})
            return
        try:
            self.respond(200, {**get_rag().status(), 'startup_error': None})
        except Exception:
            self.respond(503, {'error': 'Atlas chưa khởi tạo được dữ liệu.'})

    def do_POST(self):
        if urlparse(self.path).path != '/api/chat':
            self.respond(405, {'error': 'Phương thức không được hỗ trợ.'})
            return
        origin = self.headers.get('Origin')
        if origin and urlparse(origin).netloc != self.headers.get('Host'):
            self.respond(403, {'error': 'Origin không được phép.'})
            return
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 20000:
                raise ValueError('Câu hỏi quá dài hoặc thiếu dữ liệu.')
            args = validate(json.loads(self.rfile.read(size)))
        except (ValueError, UnicodeError) as error:
            self.respond(400, {'error': str(error)})
            return
        if not _slots.acquire(blocking=False):
            self.respond(429, {'error': 'Atlas đang bận. Vui lòng thử lại sau.'})
            return
        try:
            self.respond(200, get_rag().answer(*args))
        except Exception:
            self.respond(503, {'error': 'Dịch vụ AI tạm thời chưa phản hồi. Vui lòng thử lại.'})
        finally:
            _slots.release()
