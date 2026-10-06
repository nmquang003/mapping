"""Prepare prompts and generate local tourism illustrations using the BTC gateway.

Run with UI_testing/.venv/bin/python; credentials stay in memory. No automatic
retry of image POSTs: a timeout can still represent a charged generation.
"""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
import mimetypes
from pathlib import Path
import shlex
import threading

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
API = 'https://api.thucchien.ai/images/generations'
MODEL = 'gpt-image-2.5-sunburst'
COMMON = '''Use case: photorealistic-natural.
Asset type: Vietnamese local geography handbook website illustration.
Create a new, polished travel image of the named Vietnamese destination. Natural colors, realistic materials and vegetation, restrained contrast, fine detail, believable light and scale. Contemporary setting. One continuous scene, not a collage. Horizontal landscape canvas, 1536x1024, with the main subject fully inside the central 1536x864 safe area for a 16:9 crop. No text, lettering, captions, logos, watermark, border, invented monuments, fantasy scenery, exaggerated HDR or neon lighting. Respect the local religious and cultural setting. Do not invent historical scenes, ceremonies or costumes. This image will be labeled externally as an AI illustration, not documentary photography or evidence of exact geographic or architectural details.'''

SCENES = {
 'quang-ninh': {
  'vinh-ha-long': 'Vinh Ha Long, Quang Ninh, Vietnam. A wide view across calm emerald sea with irregular steep limestone islands covered in natural foliage. Layered karst silhouettes fading into light atmospheric haze, one modest sightseeing boat far away for scale. Soft morning sun, believable reflections. Sea islands, not an inland river or terraced fields. Do not add temples on islands or a crowded skyline.',
  'vinh-bai-tu-long': 'Bai Tu Long Bay, Quang Ninh, Vietnam. A quiet seascape of natural limestone islands and green coastal hills, pale turquoise water and a clear soft sky, seen from a plausible shoreline viewpoint. Modest composition with no fabricated landmark identity, no exact aerial map, no resorts or invented buildings. Emphasize sea, rocky islands and calm atmosphere.',
  'co-to': 'Co To archipelago, Quang Ninh, Vietnam. A coastal view inspired by Hong Van beach: clean pale sand, gently curving shoreline, turquoise waves and natural coastal trees. Eye-level wide composition in warm morning light, no grand hotels or tropical fantasy palms everywhere. Do not combine several named beaches into one impossible panorama.',
  'thanh-lan': 'Thanh Lan island in the Co To area, Quang Ninh, Vietnam. A natural rocky shoreline with green island vegetation, small waves and layered blue sea. Low coastal viewpoint, soft late-afternoon light, realistic weathered rocks and forest texture. No invented religious buildings, volcanoes or recognizable landmarks from other provinces.',
  'quan-lan': 'Quan Lan island, Bai Tu Long Bay, Quang Ninh, Vietnam. An inviting broad coastal beach, gentle blue-green sea, natural low coastal vegetation and a softly receding shoreline. Quiet morning light, detailed sand and small waves. A scenic illustration, not an exact map of Minh Chau or Son Hao; no invented temple in the water and no skyscrapers.',
  'yen-tu': 'Yen Tu, Quang Ninh, Vietnam. A respectful view of Hoa Yen Buddhist pagoda in a green mountain setting, a modest traditional Vietnamese temple exterior with low curved tiled roofs, weathered stone courtyard and mature trees. Soft mist in distant wooded mountain slopes, gentle morning light. Keep the architecture modest and plausible; do not invent an imperial palace, giant statue, theatrical ceremony or combine every Yen Tu temple into one view.',
  'bao-tang-quang-ninh': 'Quang Ninh Museum and Library, Vietnam. Architectural travel illustration of the museum exterior: a restrained modern black-glass rectangular volume, reflective dark facade, broad clean forecourt, trees and natural sky. Wide three-quarter view, straight verticals, soft daylight. No text on the facade, no invented extra towers, no crowds and no display of fabricated museum artifacts.'
 },
 'ha-noi': {
  'ho-hoan-kiem': 'Ho Hoan Kiem, Hanoi, Vietnam. View over the lake toward the red wooden The Huc bridge leading to Ngoc Son temple amid trees. Recognizable modest bridge proportions, red railing and green water, soft morning light and subtle city background. No legend characters, dragons, boats beneath a giant bridge or invented pagodas in the lake; keep distant buildings unobtrusive.',
  'pho-co-ha-noi': 'Hanoi Old Quarter, Vietnam. Eye-level street view of a narrow old commercial street with modest weathered shop houses, aged plaster, small balconies and everyday storefronts. A few ordinary pedestrians and bicycles, candid respectful daily life in warm morning light. No legible shop signs, no invented festival, no exotic costumes or uniform Chinese lantern decoration.',
  'van-mieu-quoc-tu-giam': 'Van Mieu - Quoc Tu Giam, Hanoi, Vietnam. Focus on Khue Van Cac: the modest red wooden pavilion with circular openings above white masonry supports, traditional tiled roof and tranquil courtyard greenery. Straight architectural proportions, warm diffuse daylight, aged material texture. Do not depict a huge palace or fabricate readable inscriptions and examination ceremonies.',
  'hoang-thanh-thang-long': 'Imperial Citadel of Thang Long, Hanoi, Vietnam. View of the present-day Doan Mon gate, weathered masonry with arched entrances and a modest traditional pavilion above, open green grounds and mature trees. Wide frontal architectural composition with straight verticals and soft morning light. Existing heritage site, not a reconstruction of a medieval royal palace. No emperors, soldiers, invented grand walls or readable plaques.',
  'lang-chu-tich-ho-chi-minh': 'Ho Chi Minh Mausoleum, Hanoi, Vietnam. Respectful exterior view of the low monumental grey stone mausoleum, simple rectilinear tiers and square columns, broad quiet plaza and green lawns. Balanced wide frontal framing, dignified natural daylight. No readable inscriptions, no political slogans, no invented ceremony and no interior, body or tomb imagery.',
  'nha-hat-lon-ha-noi': 'Hanoi Opera House, Vietnam. Three-quarter exterior view of the pale yellow and cream neoclassical theatre, columns, balanced facade, historic roofline and broad forecourt. Elegant but realistic scale, restrained morning light, a few small ordinary pedestrians. Keep the actual building character rather than creating a generic European palace. No readable signs or staged performance outside.',
  'bao-tang-dan-toc-hoc': 'Vietnam Museum of Ethnology, Hanoi, Vietnam. A tranquil outdoor architectural exhibition setting with a traditional timber stilt house, a tall steep thatched roof, visible wood supports and trees. Focus on construction materials and human scale rather than invented artifacts. Illustrative selection from a museum environment, not a claim of exact current exhibition layout. No people dressed in invented ethnic costumes, no ritual reenactment, no readable signs.',
  'nha-tho-lon-ha-noi': 'St Joseph Cathedral, Hanoi, Vietnam. Respectful exterior architectural view with two square towers, a central rose window, weathered grey facade and Gothic arched openings. Plausible courtyard viewpoint, straight verticals, natural soft daylight and a few ordinary visitors at a distance. No invented extra spires, no European alpine backdrop, no religious ceremony or readable signage.'
 },
 'lao-cai': {
  'sa-pa': 'Sa Pa, Lao Cai, Vietnam. A wide valley panorama with layered cultivated rice terraces below green mountain slopes, light cloud and distant mist. Plausible mountain viewpoint, small rural houses only far away, warm soft morning light, natural greens. No European ski resort, fantasy floating clouds, invented pagodas or vast golden fields on flat plains.',
  'fansipan': 'Fansipan mountain near Sa Pa, Lao Cai, Vietnam. A wide mountain summit landscape with rugged rocky foreground, layered high ridges and clouds below the distant horizon. Quiet natural sunrise light, believable vegetation and rock texture. Focus on mountain scenery; no invented summit monument, readable height marker, glass bridge or unsafe tourists on edges.',
  'cho-bac-ha': 'Bac Ha market, Lao Cai, Vietnam. Respectful eye-level market scene of local people buying vegetables and everyday produce at modest stalls, natural daylight, realistic faces and ordinary daily activity. Any patterned clothing should be understated and natural, never invented ceremonial regalia. No staged ethnic spectacle, caricatures, sacred objects, tourist posing or readable signs. Keep vendors and shoppers realistically scaled.',
  'mu-cang-chai': 'Mu Cang Chai, in present-day Lao Cai, Vietnam. A broad view of sculpted rice terraces winding around rounded mountain slopes, inspired by Mam Xoi and La Pan Tan agricultural landscapes. Green and golden rice during an intentionally seasonal ripe-rice illustration, realistic field edges, distant mountains and soft afternoon light. No exact map claim, no flat lowland fields, oceans, temples or fantasy geometry.',
  'khau-pha': 'Khau Pha mountain pass in the Mu Cang Chai - Tu Le area, present-day Lao Cai, Vietnam. Scenic view from a plausible safe overlook, curving mountain road at a distance, terraced valley and green ridges, soft light with restrained haze. Focus on landscape, not precise navigation. No invented glass bridges, spectacular impossible bends or paragliding festival.',
  'ho-thac-ba': 'Thac Ba Lake in present-day Lao Cai, Vietnam, formerly Yen Bai. Wide lake landscape of tranquil blue-green water, scattered small green islands and layered low hills. One modest passenger boat far away, natural morning light, detailed ripples and wooded shore. A scenic illustration rather than exact map or island count; no tall ocean karst columns, giant dam in foreground or luxury floating city.',
  'ngoi-tu': 'Ngoi Tu community village near Thac Ba Lake, present-day Lao Cai, Vietnam. Respectful tranquil village illustration featuring modest timber stilt houses, natural vegetation, a rural footpath and a subtle lake glimpse. Soft morning light, believable timber and woven textures. No staged ceremony, sacred symbols, invented ethnic costume, poverty spectacle or modern resort. Do not claim an exact current village layout.'
 }
}


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)


def prepare(selected_regions=None):
    selected_regions = selected_regions or list(SCENES)
    jobs = []
    groups = []
    for region, scenes in SCENES.items():
        if region not in selected_regions:
            continue
        folder = ROOT / (region + '-data') / 'images'
        data = json.loads((folder.parent / 'seed.json').read_text())
        places = {p['id']: p for p in data['places']}
        region_jobs = []
        for place_id, scene in scenes.items():
            p = places[place_id]
            prompt = COMMON + '\n\nScene: ' + scene
            prompt_path = folder / 'prompts' / (place_id + '.txt')
            prompt_path.parent.mkdir(parents=True, exist_ok=True)
            prompt_path.write_text(prompt + '\n', encoding='utf-8')
            job = dict(region=region, id=place_id, place_id=place_id, name=p['name'],
                       source_ids=p['source_ids'], prompt=prompt,
                       prompt_file=str(prompt_path.relative_to(folder)),
                       raw_output='output/imagegen/' + place_id + '.png',
                       delivery_output='generated/' + place_id + '.webp',
                       alt='Minh họa do AI tạo về ' + p['name'],
                       caption='Minh họa do AI tạo; không phải ảnh tư liệu.',
                       visual_status='pending_visual_review')
            region_jobs.append(job)
        plan = dict(status='prepared',provider=API,model=MODEL,request_size='1536x1024',
                    quality='high',delivery_size='1536x864',credential_variable='GATEWAY_KEY',
                    note='Không có ảnh tham chiếu. Cần kiểm tra hình ảnh trước khi công bố như mô tả kiến trúc; không dùng làm bằng chứng lịch sử hoặc địa lý.',jobs=region_jobs)
        save_json(folder / 'generation-plan.json', plan)
        lines = ['# Ảnh minh họa ' + data['scope']['province_name'], '',
                 'Tạo qua API Ban tổ chức; model `' + MODEL + '`. Không lưu key trong thư mục này.', '',
                 'Ảnh không có tham chiếu tư liệu, cần kiểm tra trước khi xuất bản. Gắn caption “Minh họa do AI tạo; không phải ảnh tư liệu”.', '',
                 '## Tệp', '', '- `prompts/`: prompt đầy đủ từng địa danh.',
                 '- `output/imagegen/`: ảnh gốc PNG.', '- `generated/`: bản WebP 1536×864 dùng cho web.',
                 '- `manifest.json`: kết quả sinh ảnh, đường dẫn, alt và liên kết place_id.',
                 '- `contact-sheet.jpg`: bảng xem nhanh ảnh đã tạo.', '', '## Prompt', '']
        for job in region_jobs:
            lines += ['### ' + job['name'], '', '[' + job['id'] + '.txt](' + job['prompt_file'] + ')', '',
                      'Nguồn nội dung: ' + ', '.join(job['source_ids']) + ' trong database địa phương. Chi tiết hình ảnh là minh họa, chưa xác minh từng cấu kiện kiến trúc.', '']
        (folder/'README.md').write_text('\n'.join(lines),encoding='utf-8')
        groups.append(region_jobs)
    if 'ninh-binh' in selected_regions:
        folder = ROOT / 'ninh-binh-data/images'
        plan = json.loads((folder / 'generation-plan.json').read_text(encoding='utf-8'))
        region_jobs = []
        for original in plan['jobs']:
            job = dict(original, region='ninh-binh',
                       prompt=(folder / original['prompt_file']).read_text(encoding='utf-8'),
                       caption='Minh họa do AI tạo; không phải ảnh tư liệu.',
                       visual_status='pending_visual_review')
            reference = folder / job['reference']
            if not reference.is_file():
                raise FileNotFoundError('Thiếu ảnh tham chiếu: ' + str(reference))
            with Image.open(reference) as image:
                image.verify()
            region_jobs.append(job)
        groups.append(region_jobs)
    # Round-robin ensures the first three requests cover all three regions.
    for i in range(max(map(len,groups))):
        jobs.extend(group[i] for group in groups if i < len(group))
    return jobs


def read_key(env_file):
    # Parse only GATEWAY_KEY. Do not source a shell or evaluate .env contents.
    for line in env_file.read_text(encoding='utf-8').splitlines():
        stripped=line.strip()
        if stripped.startswith('export '):
            stripped=stripped[7:].lstrip()
        key,separator,value=stripped.partition('=')
        if separator and key.strip()=='GATEWAY_KEY':
            tokens=shlex.split(value,comments=True,posix=True)
            if len(tokens)==1 and tokens[0]:
                return tokens[0]
    raise ValueError('Không tìm thấy GATEWAY_KEY hợp lệ trong .env; không in nội dung file.')


def generate(job, key, stop):
    folder=ROOT/(job['region']+'-data')/'images'
    raw_path=folder/job['raw_output']
    delivery=folder/job['delivery_output']
    record={k:v for k,v in job.items() if k!='prompt'}
    endpoint='https://api.thucchien.ai/images/edits' if job.get('reference') else API
    record.update(model=MODEL,created_on=timestamp(),endpoint=endpoint)
    if raw_path.exists():
        with Image.open(raw_path) as im:
            im.verify()
        record['status']='existing'
    elif stop.is_set():
        record['status']='not_sent'
        return record
    else:
        print('START '+job['region']+'/'+job['id'],flush=True)
        try:
            payload={'model':MODEL,'prompt':job['prompt'],'n':1,'size':'1536x1024','quality':'high'}
            options=dict(headers={'Authorization':'Bearer '+key},timeout=(20,600))
            if job.get('reference'):
                reference=folder/job['reference']
                options['data']={k:str(v) for k,v in payload.items()}
                options['files']=[('image[]',(reference.name,reference.read_bytes(),
                                   mimetypes.guess_type(reference.name)[0] or 'image/jpeg'))]
            else:
                options['json']=payload
            response=requests.post(endpoint,**options)
        except requests.RequestException as exc:
            stop.set()
            record.update(status='connection_error',error_type=type(exc).__name__,
                note='Không tự gửi lại. Nếu lỗi xảy ra sau khi gửi, yêu cầu có thể đã được API xử lý.')
            print('CONNECTION_ERROR '+job['region']+'/'+job['id'],flush=True)
            return record
        if not response.ok:
            detail=response.text.replace(key,'[REDACTED]')[:1200]
            record.update(status='api_error',http_status=response.status_code,error=detail)
            if response.status_code in (401,403,429):
                stop.set()
            print('API_ERROR '+job['region']+'/'+job['id']+' HTTP '+str(response.status_code),flush=True)
            return record
        try:
            payload=response.json()
            raw=base64.b64decode(payload['data'][0]['b64_json'],validate=True)
            with Image.open(BytesIO(raw)) as im:
                im.verify()
            raw_path.parent.mkdir(parents=True,exist_ok=True)
            # Keep provider bytes intact; actual format is recorded below.
            raw_path.write_bytes(raw)
            record.update(status='generated',revised_prompt=payload['data'][0].get('revised_prompt'),
                          cost_usd=response.headers.get('x-litellm-response-cost'))
        except (ValueError,KeyError,IndexError,TypeError,OSError) as exc:
            record.update(status='response_error',error_type=type(exc).__name__,
                          note='Không tự gửi lại yêu cầu đã thành công tại API.')
            print('RESPONSE_ERROR '+job['region']+'/'+job['id'],flush=True)
            return record
    with Image.open(raw_path) as im:
        record['raw_dimensions']=list(im.size)
        record['raw_format']=im.format
        web=ImageOps.fit(im.convert('RGB'),(1536,864),method=Image.Resampling.LANCZOS,centering=(0.5,0.5))
        delivery.parent.mkdir(parents=True,exist_ok=True)
        web.save(delivery,'WEBP',quality=90,method=6)
    record['sha256']=hashlib.sha256(raw_path.read_bytes()).hexdigest()
    print('DONE '+job['region']+'/'+job['id'],flush=True)
    return record


def manifest(records):
    for region in sorted({record['region'] for record in records.values()}):
        folder=ROOT/(region+'-data')/'images'
        local=[r for r in records.values() if r['region']==region]
        save_json(folder/'manifest.json',dict(provider='https://api.thucchien.ai',model=MODEL,updated_on=timestamp(),
            label='Minh họa do AI tạo; không phải ảnh tư liệu.',jobs=local))


def contact_sheets(records):
    font_path='/System/Library/Fonts/Supplemental/Arial.ttf'
    font=ImageFont.truetype(font_path,20) if Path(font_path).exists() else ImageFont.load_default()
    for region in sorted({record['region'] for record in records.values()}):
        folder=ROOT/(region+'-data')/'images'
        available=[r for r in records.values() if r['region']==region and r['status'] in ('generated','existing')]
        if not available:
            continue
        sheet=Image.new('RGB',(1200,270*((len(available)+2)//3)),(245,242,234))
        draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(available):
            with Image.open(folder/r['delivery_output']) as im:
                thumb=ImageOps.fit(im.convert('RGB'),(390,219))
            x=(i%3)*400+5;y=(i//3)*270+5
            sheet.paste(thumb,(x,y))
            draw.text((x,y+225),r['name'],font=font,fill=(35,35,35))
        sheet.save(folder/'contact-sheet.jpg',quality=92)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare-only',action='store_true')
    parser.add_argument('--workers',type=int,default=3,choices=range(1,7))
    parser.add_argument('--env-file',type=Path,default=ROOT.parent/'.env')
    parser.add_argument('--regions',nargs='+',choices=['ninh-binh',*SCENES],default=list(SCENES),
                        help='Chỉ tạo ảnh cho các địa phương được chọn; Ninh Bình dùng ảnh tham chiếu đã chuẩn bị.')
    args=parser.parse_args()
    selected=list(dict.fromkeys(args.regions))
    jobs=prepare(selected)
    print('Prepared '+str(len(jobs))+' prompts for '+', '.join(selected)+'.',flush=True)
    if args.prepare_only:
        return 0
    key=read_key(args.env_file)
    records={}
    for region in selected:
        previous=ROOT/(region+'-data')/'images/manifest.json'
        if previous.exists():
            records.update({r['region']+'/'+r['id']:r for r in json.loads(previous.read_text())['jobs']})
    stop=threading.Event()
    # Submit only up to workers at a time, so a connection/auth failure stops
    # the rest of the paid batch before it is sent.
    pending=iter(jobs)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures={}
        for _ in range(args.workers):
            job=next(pending,None)
            if job:
                futures[pool.submit(generate,job,key,stop)]=job
        while futures:
            future=next(as_completed(futures))
            job=futures.pop(future)
            try:
                record=future.result()
            except Exception as exc:
                stop.set()
                record={k:v for k,v in job.items() if k!='prompt'}
                record.update(status='local_error',error_type=type(exc).__name__)
            records[job['region']+'/'+job['id']]=record
            manifest(records)
            if not stop.is_set():
                following=next(pending,None)
                if following:
                    futures[pool.submit(generate,following,key,stop)]=following
    contact_sheets(records)
    expected={job['region']+'/'+job['id'] for job in jobs}
    successful=sum(r['status'] in ('generated','existing') for k,r in records.items() if k in expected)
    print(f'Result: {successful}/{len(jobs)} images available. Credentials were not written to outputs.',flush=True)
    return 0 if successful==len(jobs) else 1


if __name__=='__main__':
    raise SystemExit(main())
