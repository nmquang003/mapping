"""Copy completed local AI assets into the deployable static website.

Run after generation: python3 scripts/sync_ai_images.py. No API calls or keys.
Only existing WebP files are published; unfinished jobs never create broken URLs.
"""
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
assets = ROOT / 'dist/assets'
regions = {}
for slug in ('ninh-binh', 'ha-noi', 'quang-ninh', 'lao-cai'):
    folder = ROOT.parent / (slug + '-data')
    seed_path = folder / 'seed.json'
    if not seed_path.exists():
        continue
    seed = json.loads(seed_path.read_text(encoding='utf-8'))
    sources = {s['id']: s for s in seed['sources']}
    plan_path = folder / 'images/generation-plan.json'
    if not plan_path.exists():
        continue
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    images = []
    for job in plan['jobs']:
        output = job.get('delivery_output')
        if not output:
            continue
        file = folder / 'images' / output
        if not file.is_file() or not file.stat().st_size:
            continue
        target = assets / 'ai' / slug / (job['id'] + '.webp')
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != file.read_bytes():
            shutil.copyfile(file, target)
        place = next((p for p in seed['places'] if p['id'] == job['place_id']), None)
        if not place:
            raise ValueError('Unknown place: ' + job['place_id'])
        images.append(dict(id=job['id'], placeId=job['place_id'], name=job['name'],
                           src=str(target.relative_to(ROOT / 'dist')), alt=job['alt'],
                           caption='Minh họa do AI tạo; không phải ảnh tư liệu.',
                           model=plan['model'], summary=place['summary'],
                           sources=[dict(title=sources[i]['title'], url=sources[i]['url'])
                                    for i in job['source_ids']],
                           visualStatus='pending_visual_review'))
    regions[slug] = dict(name=seed['scope']['province_name'], images=images)
manifest = assets / 'ai-images.json'
temporary = manifest.with_suffix('.json.tmp')
temporary.write_text(json.dumps(dict(regions=regions), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
temporary.replace(manifest)
print('Synced ' + str(sum(len(r['images']) for r in regions.values())) + ' AI images: ' +
      ', '.join(slug + '=' + str(len(r['images'])) for slug, r in regions.items()))
