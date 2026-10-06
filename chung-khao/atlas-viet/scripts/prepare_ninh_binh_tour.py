"""Fetch verified panorama JPEGs only and package a local Ninh Binh tour.
Never downloads or executes the source player, iframe, or JavaScript.
Requires Pillow. Keeps source images in data/; publishes resized JPEGs.
"""
import concurrent.futures
import hashlib
import json
import ssl
import time
import urllib.request
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'data/360-tours'
OUTPUT=ROOT/'dist/assets/360/ninh-binh'
SOURCE='https://vietnam.travel/sites/default/files/360Tour/NinhBinh/'
CONTEXT=ssl.create_default_context(cafile='/etc/ssl/cert.pem')
metadata=json.loads((ARCHIVE/'ninh-binh/tour.json').read_text())

def prepare(scene):
    original=ARCHIVE/scene['images'][0]['path']
    original.parent.mkdir(parents=True,exist_ok=True)
    if not original.is_file():
        url=SOURCE+'media/'+original.name
        for attempt in range(3):
            try:
                request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
                with urllib.request.urlopen(request,context=CONTEXT,timeout=30) as response:
                    if response.headers.get_content_type()!='image/jpeg':
                        raise ValueError('Expected JPEG panorama')
                    data=response.read()
                from io import BytesIO
                with Image.open(BytesIO(data)) as image:image.verify()
                original.write_bytes(data)
                break
            except Exception:
                if attempt==2:raise
                time.sleep(1)
    with Image.open(original) as image:
        image=image.convert('RGB')
        if image.width!=image.height*2:raise ValueError('Expected 2:1 equirectangular image')
        for quality,width in [('hi',4096),('mobile',2048)]:
            target=OUTPUT/quality/(scene['id']+'.jpg');target.parent.mkdir(parents=True,exist_ok=True)
            image.resize((width,width//2),Image.Resampling.LANCZOS).save(target,quality=90,optimize=True)
    hotspots=[]
    for adjacent in scene['adjacent_scenes']:
        destination=adjacent['panorama']
        destination=destination.get('id') if isinstance(destination,dict) else destination.removeprefix('this.')
        hotspots.append({'linkedscene':destination,'yaw':adjacent['yaw'],'pitch':0})
    print('Prepared:',scene['title'],flush=True)
    return {'id':scene['id'],'projection':'equirectangular',
            'panorama':{quality:f'ninh-binh/{quality}/{scene["id"]}.jpg' for quality in ['hi','mobile']},
            'view':{'yaw':0,'pitch':0,'hfov':95},'hotspots':hotspots,
            'source_sha256':hashlib.sha256(original.read_bytes()).hexdigest()}

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    scenes=list(pool.map(prepare,metadata['scenes']))
(ROOT/'dist/assets/360/ninh-binh.json').write_text(json.dumps({'scenes':scenes},ensure_ascii=False,indent=2)+'\n')
print('Published metadata for',len(scenes),'Ninh Binh scenes.')
