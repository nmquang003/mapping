"""Download Sa Pa's public JPEG tiles and rebuild local cubemaps.
Only reads XML metadata and images; never executes the source player's code.
Requires Pillow and curl (TLS verification remains enabled).
"""
import concurrent.futures
import hashlib
import json
import math
import subprocess
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import urljoin
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT/'data/360-tours/sa-pa'
OUTPUT = ROOT/'dist/assets/360/sa-pa'
SOURCE = 'https://3d.vrtour.vn/tour/sapa/thi-tran-sapadata/'
TOUR = 'https://3d.vrtour.vn/tour/sapa/thi-xa-sapa.html'
FACES = {'front':'f', 'right':'r', 'back':'b', 'left':'l', 'up':'u', 'down':'d'}


def fetch(relative):
    if relative.startswith('/') or '..' in Path(relative).parts or '://' in relative:
        raise ValueError('Unexpected source path')
    target = ARCHIVE/relative
    if not target.is_file():
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix+'.part')
        subprocess.run(['curl', '--fail', '--silent', '--show-error', '--retry', '3',
            '--max-time', '30', urljoin(SOURCE, relative), '-o', str(temporary)], check=True)
        if target.suffix == '.jpg':
            with Image.open(temporary) as image:
                if image.format != 'JPEG':
                    raise ValueError('Expected JPEG tile')
                image.verify()
        temporary.replace(target)
    return target


def main():
    metadata = ET.parse(fetch('thi-tran-sapa_vr.xml')).getroot()
    messages = ET.parse(fetch('thi-tran-sapa_messages_en.xml')).getroot()
    labels = {e.get('name'): ''.join(e.itertext()) for e in messages.iter() if e.get('name')}
    source_scenes = metadata.findall('scene')
    ids = {scene.get('name') for scene in source_scenes}
    raw_titles = [labels['en_'+scene.get('titleid')].replace('Sapa', 'Sa Pa').replace('Sunplaza', 'Sun Plaza') for scene in source_scenes]
    counts, seen = Counter(raw_titles), Counter()
    scenes = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for scene, title in zip(source_scenes, raw_titles, strict=True):
            scene_id = scene.get('name')
            seen[title] += 1
            if counts[title] > 1:
                title += f' – góc {seen[title]}'
            image = scene.find('image')
            level = min((l for l in image.findall('level') if int(l.get('tiledimagewidth')) >= 2048),
                        key=lambda l: int(l.get('tiledimagewidth')))
            width = int(level.get('tiledimagewidth'))
            tile_size = int(image.get('tilesize'))
            side = math.ceil(width/tile_size)
            variants = {'hi': {}, 'mobile': {}}
            hashes = {}
            for face_name, face in FACES.items():
                pattern = level.find(face_name).get('url')
                jobs = [(v, u, pattern.replace('%v', str(v)).replace('%u', str(u)))
                        for v in range(side) for u in range(side)]
                tiles = list(pool.map(fetch, [path for _, _, path in jobs]))
                canvas = Image.new('RGB', (width, width))
                digest = hashlib.sha256()
                for (v, u, _), path in zip(jobs, tiles, strict=True):
                    digest.update(path.read_bytes())
                    with Image.open(path) as tile:
                        expected = (min(tile_size, width-u*tile_size), min(tile_size, width-v*tile_size))
                        if tile.size != expected:
                            raise ValueError(f'Unexpected tile dimensions: {path.name}: {tile.size}')
                        canvas.paste(tile.convert('RGB'), (u*tile_size, v*tile_size))
                hashes[face] = digest.hexdigest()
                for quality, size in [('hi', 2048), ('mobile', 1024)]:
                    relative = f'sa-pa/{quality}/{scene_id}/{face}.jpg'
                    destination = ROOT/'dist/assets/360'/relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    canvas.resize((size, size), Image.Resampling.LANCZOS).save(destination, quality=88, optimize=True)
                    variants[quality][face] = relative
            view = scene.find('view')
            hotspots = [{'linkedscene':h.get('linktarget'), 'ath':float(h.get('ath')), 'atv':float(h.get('atv'))}
                        for h in scene.findall('hotspot') if h.get('linktarget') in ids]
            scenes.append({'id':scene_id, 'title':title, 'view':{
                'hlookat':float(view.get('hlookat')), 'vlookat':float(view.get('vlookat')),
                'fov':95, 'fovmin':45, 'fovmax':120}, 'hotspots':hotspots,
                'variants':variants, 'source_face_sha256':hashes})
            print('Prepared:', title, flush=True)
    (ROOT/'dist/assets/360/sa-pa.json').write_text(json.dumps({
        'source':{'provider':'VRTour', 'url':TOUR}, 'scenes':scenes},ensure_ascii=False,indent=2)+'\n')
    print('Published',len(scenes),'Sa Pa scenes.',flush=True)


if __name__ == '__main__':
    main()
