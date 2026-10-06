"""Read only Atlas configuration from local dotenv files, without exposing secrets."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'THUCCHIEN_API_KEY', 'AITC_API_KEY', 'AITC_BASE_URL', 'OPENROUTER_API_KEY',
           'ATLAS_PROVIDER', 'ATLAS_EMBEDDING_MODEL', 'ATLAS_CHAT_MODEL',
           'ATLAS_OPENROUTER_CHAT_MODEL', 'ATLAS_MIN_SIMILARITY'}


def load_env(paths=None):
    # Explicit process environment wins, then app-local .env, then repository .env.
    for path in paths if paths is not None else (ROOT/'.env', ROOT.parents[1]/'.env'):
        if not path.is_file():
            continue
        for raw in path.read_text(encoding='utf-8-sig').splitlines():
            line = raw.strip()
            if line.startswith('export '):
                line = line[7:].strip()
            key, sep, value = line.partition('=')
            key, value = key.strip(), value.strip()
            if not sep or key not in ALLOWED:
                continue
            if len(value) > 1 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            else:
                value = value.split(' #', 1)[0].rstrip()
            if value:
                os.environ.setdefault(key, value)
