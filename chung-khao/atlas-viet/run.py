"""Portable launcher. API keys stay in backend environment or local .env."""
import argparse
import os
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ALLOWED={'THUCCHIEN_API_KEY','AITC_API_KEY','AITC_BASE_URL','ATLAS_EMBEDDING_MODEL','ATLAS_CHAT_MODEL','ATLAS_MIN_SIMILARITY'}
def main():
    if sys.version_info<(3,10):raise SystemExit('Cần Python 3.10 trở lên.')
    env=ROOT/'.env'
    if env.exists():
        for raw in env.read_text(encoding='utf-8-sig').splitlines():
            line=raw.strip()
            if not line or line.startswith('#'):continue
            key,sep,value=line.partition('=');key=key.strip();value=value.strip()
            if sep and key in ALLOWED:
                if len(value)>1 and value[0]==value[-1] and value[0] in ['"',"'"]:value=value[1:-1]
                os.environ.setdefault(key,value)
    if not (os.environ.get('THUCCHIEN_API_KEY') or os.environ.get('AITC_API_KEY')):
        raise SystemExit('Sao chép .env.example thành .env, điền key BTC rồi chạy lại. Không chia sẻ .env.')
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=4322);parser.add_argument('--no-browser',action='store_true');args=parser.parse_args()
    sys.path.insert(0,str(ROOT/'rag'))
    import server
    sys.argv=['server.py','serve','--port',str(args.port)]
    if not args.no_browser:sys.argv.append('--open-browser')
    server.main()
if __name__=='__main__':main()
