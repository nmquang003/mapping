"""Fetch pinned public GIS data and attributed photos for the atlas prototype."""
import concurrent.futures
import hashlib
import json
import math
from pathlib import Path
import subprocess
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'dist' / 'assets'
ASSETS.mkdir(parents=True, exist_ok=True)

def fetch(url, target):
    if target.exists() and target.stat().st_size > 0:
        return
    subprocess.run(['curl', '-fsSL', '--retry', '3', '--retry-all-errors', '--connect-timeout', '15', '--max-time', '60', url, '-o', str(target)], check=True)

def simplify(points, epsilon=.0018):
    if len(points) < 5:
        return points
    a, b = points[0], points[-1]
    dx, dy = b[0]-a[0], b[1]-a[1]
    length = dx*dx+dy*dy
    best, index = 0, 0
    for i, p in enumerate(points[1:-1], 1):
        t = max(0, min(1, ((p[0]-a[0])*dx+(p[1]-a[1])*dy)/length)) if length else 0
        distance = (p[0]-a[0]-t*dx)**2+(p[1]-a[1]-t*dy)**2
        if distance > best:
            best, index = distance, i
    if best > epsilon*epsilon:
        return simplify(points[:index+1], epsilon)[:-1]+simplify(points[index:], epsilon)
    return [a, b]

tree_path = ROOT / 'data' / 'gis-tree.json'
fetch('https://api.github.com/repos/thanglequoc/vietnamese-provinces-database/git/trees/master?recursive=1', tree_path)
tree = json.loads(tree_path.read_text())
revision = tree['sha']
paths = sorted(t['path'] for t in tree['tree'] if 'geojson_11Mar2026/' in t['path'] and t['path'].endswith('/province.geojson'))
names = ['Hà Nội','Cao Bằng','Tuyên Quang','Lào Cai','Điện Biên','Lai Châu','Sơn La','Thái Nguyên','Lạng Sơn','Quảng Ninh','Phú Thọ','Bắc Ninh','Hải Phòng','Hưng Yên','Ninh Bình','Thanh Hóa','Nghệ An','Hà Tĩnh','Quảng Trị','Huế','Đà Nẵng','Quảng Ngãi','Khánh Hòa','Gia Lai','Đắk Lắk','Lâm Đồng','Tây Ninh','Đồng Nai','TP. Hồ Chí Minh','Vĩnh Long','Đồng Tháp','An Giang','Cần Thơ','Cà Mau']

def province(path):
    filename = path.split('/')[-2]+'.geojson'
    target = ROOT / 'data' / filename
    fetch('https://raw.githubusercontent.com/thanglequoc/vietnamese-provinces-database/'+revision+'/'+quote(path), target)
    batch = json.loads(target.read_text())['features']
    number = int(path.split('/')[-2].split('_')[0])
    for feature in batch:
        feature['properties']['name'] = names[number-1]
        feature['properties']['atlasId'] = number
    return batch

features = []
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for batch in pool.map(province, paths):
        features.extend(batch)

for feature in features:
    geom = feature['geometry']
    polygons = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    # Preserve all polygon components, including islands. Simplify only long rings.
    geom['type'] = 'MultiPolygon'
    def valid_ring(ring):
        reduced = simplify(ring) if len(ring)>20 else ring
        return reduced if len(reduced)>=4 else ring
    geom['coordinates'] = [[[ [round(p[0], 5), round(p[1], 5)] for p in valid_ring(ring)] for ring in poly] for poly in polygons]
    feature.pop('bbox', None)

# Only offshore components are taken from this source; keep the 34-province
# mainland snapshot above. Its README explicitly permits public use with credit.
island_revision = 'ccb9f4ae992418bfeefd06da1eb42d0249632176'
island_path = 'Vietnam Administrative Divisions (Pre-2025) - Đơn vị hành chính Việt Nam (Trước 2025)/Provinces_included_Paracel_SpratlyIslands.geojson'
island_target = ROOT / 'data' / 'offshore-reference.geojson'
fetch('https://raw.githubusercontent.com/nguyenduy1133/Free-GIS-Data/'+island_revision+'/'+quote(island_path), island_target)
for offshore in json.loads(island_target.read_text())['features']:
    note = offshore['properties'].get('Note') or ''
    province_id = 21 if 'Hoang Sa' in note else 23 if 'Truong Sa' in note else None
    if province_id:
        target = next(f for f in features if f['properties']['atlasId'] == province_id)
        for poly in offshore['geometry']['coordinates']:
            target['geometry']['coordinates'].append([[[round(p[0],5),round(p[1],5)] for p in ring] for ring in poly])

output = {'type':'FeatureCollection', 'source':{'repository':'https://github.com/thanglequoc/vietnamese-provinces-database', 'revision':revision, 'snapshot':'geojson_11Mar2026', 'upstream':'https://sapnhap.bando.com.vn', 'offshoreRepository':'https://github.com/nguyenduy1133/Free-GIS-Data','offshoreRevision':island_revision,'note':'Dữ liệu tham khảo cộng đồng; ranh giới giản lược để hiển thị. Đối chiếu nguồn chính thức trước khi nộp.'}, 'features':features}
(ASSETS/'vietnam-provinces.geojson').write_text(json.dumps(output, ensure_ascii=False, separators=(',',':')))
fetch('https://raw.githubusercontent.com/thanglequoc/vietnamese-provinces-database/'+revision+'/LICENSE', ROOT/'data'/'GIS-REPOSITORY-LICENSE.txt')

photos = [
 ('ninh-binh','Trang An - 05.jpg','Benjamin Smith','CC BY-SA 4.0'),
 ('ha-noi','Hoan Kiem Lake photo.jpg','Tranhuutukkt','CC BY-SA 4.0'),
 ('ha-long','Halong Bay panorama.jpg','Isderion','CC BY-SA 3.0 DE'),
 ('sa-pa','Rice terraces in Sapa, Vietnam.jpg','Eerin25','CC0 1.0'),
]
credits=[]
for slug, filename, author, license_name in photos:
    normalized = filename.replace(' ', '_')
    digest = hashlib.md5(normalized.encode()).hexdigest()
    image_url = 'https://upload.wikimedia.org/wikipedia/commons/'+digest[0]+'/'+digest[:2]+'/'+quote(normalized)
    target=ASSETS/(slug+'.jpg')
    fetch(image_url, target)
    subprocess.run(['sips','-Z','1600',str(target)],check=True,stdout=subprocess.DEVNULL)
    license_url = 'https://creativecommons.org/publicdomain/zero/1.0/' if license_name == 'CC0 1.0' else 'https://creativecommons.org/licenses/by-sa/3.0/de/' if 'DE' in license_name else 'https://creativecommons.org/licenses/by-sa/4.0/'
    credits.append({'id':slug,'file':'assets/'+slug+'.jpg','author':author,'license':license_name,'source':'https://commons.wikimedia.org/wiki/File:'+quote(normalized),'licenseUrl':license_url,'changes':'Thu nhỏ tối đa 1600px; cắt khung bằng CSS. Ảnh thực tế dùng tạm cho bản mẫu, chưa phải minh họa AI.'})
(ASSETS/'credits.json').write_text(json.dumps(credits,ensure_ascii=False,indent=2))
print('Prepared', len(features), 'province features and',len(credits),'photos. Revision:',revision)
