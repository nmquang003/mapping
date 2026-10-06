"""Serve Atlas Viet and its RAG API. No API keys are sent to the browser."""
import argparse
import json
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from engine import RAG, ROOT


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['serve','build-index'])
    parser.add_argument('--port', type=int, default=4322)
    args = parser.parse_args()
    rag = RAG()
    if args.command=='build-index':
        print(json.dumps(rag.build_index(),ensure_ascii=False))
        return
    startup_error = None
    try:
        print(json.dumps(rag.build_index(),ensure_ascii=False),flush=True)
    except (RuntimeError,ValueError,OSError) as error:
        startup_error = str(error)
        print(startup_error,file=sys.stderr)
    slots = threading.BoundedSemaphore(2)
    origins = {f'http://127.0.0.1:{args.port}',f'http://localhost:{args.port}',
               'http://127.0.0.1:4321','http://localhost:4321'}
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*a,**kw):
            super().__init__(*a,directory=str(ROOT/'dist'),**kw)

        def end_headers(self):
            origin = self.headers.get('Origin')
            if origin in origins:
                self.send_header('Access-Control-Allow-Origin',origin)
                self.send_header('Vary','Origin')
            self.send_header('Cache-Control','no-store')
            super().end_headers()

        def respond(self,status,value):
            content=json.dumps(value,ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Content-Length',str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        def do_OPTIONS(self):
            if self.headers.get('Origin') not in origins:
                self.respond(403,{'error':'Origin không được phép.'});return
            self.send_response(204)
            self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers','Content-Type')
            self.end_headers()

        def do_GET(self):
            if urlparse(self.path).path=='/api/status':
                self.respond(200,{**rag.status(),'startup_error':startup_error});return
            if self.path.startswith('/api/'):
                self.respond(404,{'error':'Không tìm thấy API.'});return
            super().do_GET()

        def do_POST(self):
            if self.headers.get('Origin') not in origins:
                self.respond(403,{'error':'Origin không được phép.'});return
            if urlparse(self.path).path!='/api/chat':
                self.respond(404,{'error':'Không tìm thấy API.'});return
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=20000:
                    raise ValueError('Câu hỏi quá dài hoặc thiếu dữ liệu.')
                body=json.loads(self.rfile.read(size))
                question=body.get('question')
                if not isinstance(question,str) or not 1<=len(question.strip())<=1500:
                    raise ValueError('Câu hỏi cần có từ 1 đến 1500 ký tự.')
                history=body.get('history',[])
                if not isinstance(history,list) or len(history)>6 or any(not isinstance(r,dict) or r.get('role') not in ['user','assistant'] or not isinstance(r.get('content'),str) or len(r['content'])>4000 for r in history):
                    raise ValueError('Lịch sử hội thoại không hợp lệ.')
                selected=body.get('dataset_id')
                if selected is not None and not isinstance(selected,str):
                    raise ValueError('Địa phương không hợp lệ.')
            except (ValueError,AttributeError) as error:
                self.respond(400,{'error':str(error)});return
            if not slots.acquire(blocking=False):
                self.respond(429,{'error':'Atlas đang xử lý câu hỏi khác. Vui lòng thử lại sau.'});return
            try:
                self.respond(200,rag.answer(question.strip(),selected,history))
            except (RuntimeError,ValueError,OSError,KeyError,TypeError) as error:
                message=str(error) if isinstance(error,RuntimeError) else 'Backend chưa xử lý được dữ liệu. Vui lòng thử lại.'
                self.respond(503,{'error':message})
            finally:
                slots.release()
    print(f'Atlas RAG: http://127.0.0.1:{args.port}/',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()


if __name__=='__main__':
    main()
