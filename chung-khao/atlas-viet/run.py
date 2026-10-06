"""Portable launcher. API keys stay in backend environment or local .env."""
import argparse
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
    if sys.version_info<(3,10):raise SystemExit('Cần Python 3.10 trở lên.')
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=4322);parser.add_argument('--no-browser',action='store_true');args=parser.parse_args()
    sys.path.insert(0,str(ROOT/'rag'))
    from config import load_env
    load_env()
    import server
    sys.argv=['server.py','serve','--port',str(args.port)]
    if not args.no_browser:sys.argv.append('--open-browser')
    server.main()
if __name__=='__main__':main()
