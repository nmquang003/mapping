"""Package the checked SQLite datasets for serverless, outside public dist."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT.parent
catalog = source/'data-catalog.json'
if catalog.is_file():
    target = ROOT/'data'
    target.mkdir(exist_ok=True)
    shutil.copy2(catalog, target/'data-catalog.json')
    for dataset in json.loads(catalog.read_text())['datasets']:
        relative = Path(dataset['paths']['sqlite'])
        destination = target/relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source/relative, destination)
if not (ROOT/'data/data-catalog.json').is_file():
    raise SystemExit('Missing private dataset package for Vercel.')
print('Packaged four source datasets for Atlas API.')
