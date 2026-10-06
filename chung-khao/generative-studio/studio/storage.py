import json
import re
import shutil
import sqlite3
import uuid
import zipfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def now():
    return datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat(timespec='seconds')


def slug(value):
    return re.sub(r'[^\w-]+', '-', value, flags=re.UNICODE).strip('-')[:60] or 'project'


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.db = self.root / 'studio.sqlite'
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY, name TEXT, created TEXT);
                CREATE TABLE IF NOT EXISTS runs(
                    id TEXT PRIMARY KEY, project TEXT, kind TEXT, model TEXT, prompt TEXT,
                    status TEXT, created TEXT, updated TEXT, parent TEXT, title TEXT,
                    favorite INTEGER DEFAULT 0, tags TEXT DEFAULT '', remote_id TEXT DEFAULT '',
                    cost REAL, error TEXT DEFAULT '');
            ''')

    def connect(self):
        db = sqlite3.connect(self.db, timeout=30)
        db.row_factory = sqlite3.Row
        return db

    def projects(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute('SELECT * FROM projects ORDER BY created DESC')]

    def create_project(self, name):
        name = name.strip()
        if not name:
            raise ValueError('Nhập tên project.')
        pid = slug(name) + '-' + uuid.uuid4().hex[:8]
        with self.connect() as db:
            db.execute('INSERT INTO projects VALUES(?,?,?)', (pid, name, now()))
        for d in ('inputs', 'runs', 'exports'):
            (self.root / 'projects' / pid / d).mkdir(parents=True)
        return pid

    def project_dir(self, pid):
        with self.connect() as db:
            if not db.execute('SELECT 1 FROM projects WHERE id=?', (pid,)).fetchone():
                raise ValueError('Chọn một project hợp lệ.')
        return self.root / 'projects' / pid

    def create_run(self, pid, kind, model, prompt, request, parent=None):
        self.project_dir(pid)
        if parent and self.get(parent)['project'] != pid:
            raise ValueError('Phiên bản gốc phải thuộc project đang mở.')
        rid = datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + kind + '_' + uuid.uuid4().hex[:8]
        t = now()
        with self.connect() as db:
            db.execute('INSERT INTO runs(id,project,kind,model,prompt,status,created,updated,parent,title) VALUES(?,?,?,?,?,?,?,?,?,?)',
                       (rid, pid, kind, model, prompt, 'running', t, t, parent, prompt[:70] or kind))
        self.directory(rid).mkdir(parents=True)
        self.write_json(rid, 'request.json', request)
        self.update(rid)
        return rid

    def get(self, rid):
        with self.connect() as db:
            row = db.execute('SELECT * FROM runs WHERE id=?', (rid,)).fetchone()
        if not row:
            raise ValueError('Không tìm thấy lần tạo này.')
        return dict(row)

    def recover_interrupted(self):
        """A restarted server must not silently repeat an interrupted POST."""
        with self.connect() as db:
            ids = [r['id'] for r in db.execute("SELECT id FROM runs WHERE status='running'")]
        for rid in ids:
            self.directory(rid).mkdir(parents=True, exist_ok=True)
            self.update(rid, status='uncertain',
                        error='Ứng dụng dừng khi yêu cầu đang chạy. Kiểm tra kết quả tại BTC trước khi tạo lại.')
        return ids

    def directory(self, rid):
        r = self.get(rid)
        return self.root / 'projects' / r['project'] / 'runs' / rid

    def update(self, rid, **fields):
        allowed = {'status', 'remote_id', 'cost', 'error', 'title', 'favorite', 'tags'}
        if not fields.keys() <= allowed:
            raise ValueError('Invalid run field')
        fields['updated'] = now()
        with self.connect() as db:
            db.execute('UPDATE runs SET ' + ','.join(f'{k}=?' for k in fields) + ' WHERE id=?', (*fields.values(), rid))
        self.write_json(rid, 'metadata.json', self.get(rid))

    def write_json(self, rid, filename, value):
        dest = self.directory(rid) / filename
        tmp = dest.with_name(dest.name + '.' + uuid.uuid4().hex + '.tmp')
        tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
        tmp.replace(dest)

    def list_runs(self, pid, kind='all', query='', favorites=False):
        self.project_dir(pid)
        with self.connect() as db:
            rows = [dict(r) for r in db.execute('SELECT * FROM runs WHERE project=? ORDER BY created DESC,id DESC', (pid,))]
        q = query.casefold().strip()
        return [r for r in rows if (kind == 'all' or r['kind'] == kind) and
                (not favorites or r['favorite']) and
                (not q or q in ' '.join(str(r[k]) for k in ('title', 'prompt', 'tags', 'model')).casefold())]

    def files(self, rid):
        return sorted(p for p in self.directory(rid).iterdir() if p.name.startswith('output'))

    def copy_input(self, rid, path):
        if not path:
            return None
        src = Path(path)
        # Only call with upload paths or stored output paths, never a user-entered path.
        if not src.is_file():
            raise ValueError('File đầu vào không tồn tại.')
        dest = self.directory(rid) / ('input' + src.suffix.lower())
        shutil.copyfile(src, dest)
        return dest

    def save_text_revision(self, rid, text):
        r = self.get(rid)
        child = self.create_run(r['project'], 'text', 'local-edit', r['prompt'], {'text': text}, rid)
        (self.directory(child) / 'output.txt').write_text(text, encoding='utf-8')
        self.update(child, status='completed')
        return child

    def export(self, pid, rid=None):
        pd = self.project_dir(pid)
        target = pd / 'exports' / ((rid or pid) + '-' + uuid.uuid4().hex[:8] + '.zip')
        sources = [self.directory(rid)] if rid else [pd / 'runs', pd / 'inputs']
        if rid and self.get(rid)['project'] != pid:
            raise ValueError('Output không thuộc project.')
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
            for source in sources:
                for p in source.rglob('*'):
                    if p.is_file():
                        z.write(p, p.relative_to(pd))
        return str(target)
