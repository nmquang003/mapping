"""Package explicit runtime allowlist. Never include API credentials."""
import json
import os
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA_ROOT=ROOT.parent
PREFIX='atlas-viet-rag/'
def main():
    files={}
    def add(path,target):
        if not path.is_file():raise ValueError(f'Missing package file: {path.name}')
        if path.name=='.env' or '__pycache__' in path.parts:raise ValueError('Secret/cache file not allowed')
        files[PREFIX+target]=path.read_bytes()
    for path in sorted((ROOT/'dist').rglob('*')):
        if path.is_file():add(path,'atlas-viet/'+str(path.relative_to(ROOT)))
    for path in sorted((ROOT/'rag').glob('*')):
        if path.is_file() and path.suffix in ['.py','.md']:add(path,'atlas-viet/'+str(path.relative_to(ROOT)))
    for name in ['run.py','launch.command','launch.bat','.env.example','README.md']:add(ROOT/name,'atlas-viet/'+name)
    add(ROOT/'.rag/index.json','atlas-viet/.rag/index.json')
    add(DATA_ROOT/'data-catalog.json','data-catalog.json')
    catalog=json.loads((DATA_ROOT/'data-catalog.json').read_text())
    for dataset in catalog['datasets']:
        for key in ['seed_json','sqlite','readme','sources_csv','build_script']:
            path=dataset['paths'][key];add(DATA_ROOT/path,path)
    for name in ['09-embeddings.md','03-text-generation.md','10-openai-deepseek.md']:
        path='docs/thucchien-user-guide/markdown/'+name;add(DATA_ROOT/path,path)
    files[PREFIX+'BAT-DAU.txt']='''ATLAS VIỆT — WEB + CHATBOT RAG

1. Giải nén toàn bộ atlas-viet-rag, giữ nguyên cấu trúc.
2. Cần Python 3.10 trở lên; không cần cài thêm thư viện Python.
3. Trong atlas-viet/, sao chép .env.example thành .env, điền key BTC.
4. macOS/Linux: python3 run.py. Windows: python run.py hoặc launch.bat.
5. Mở http://127.0.0.1:4322/. Giữ terminal đang chạy.

Gói có web, 4 database và 142 vector embedding thật. Không có API key.
Cần Internet và key hợp lệ để hỏi chatbot. Xem atlas-viet/rag/README.md.
Đây là bản local, chưa phải cấu hình triển khai công khai.
'''.encode()
    for key in [os.environ.get('THUCCHIEN_API_KEY'),os.environ.get('AITC_API_KEY')]:
        if key and len(key)>8:
            for name,content in files.items():
                if key.encode() in content:raise ValueError(f'Credential found in package: {name}')
    release=ROOT/'release';release.mkdir(exist_ok=True);target=release/'atlas-viet-rag.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,content in files.items():
            info=zipfile.ZipInfo(name);info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(0o755 if name.endswith('launch.command') else 0o644)<<16
            archive.writestr(info,content)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        assert not any(name.endswith('/.env') for name in archive.namelist())
    print(json.dumps({'archive':str(target),'files':len(files),'bytes':target.stat().st_size},ensure_ascii=False))
if __name__=='__main__':main()
