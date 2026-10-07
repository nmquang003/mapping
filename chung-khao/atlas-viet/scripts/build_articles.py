"""Build sourced Vietnamese reading material from the four local seed datasets.

No network calls. Run again after editing the source datasets.
"""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEADS = {
    'ninh-binh': ('Ninh Bình: non nước và ký ức cố đô', 'Một dòng sông len giữa núi đá, một ngôi đền lưu dấu kinh đô, một khu rừng mở ra thế giới tự nhiên: những địa danh tuyển chọn của Ninh Bình cho thấy cảnh quan và lịch sử luôn có thể được đọc cùng nhau.'),
    'ha-noi': ('Hà Nội: đọc thành phố qua những lớp thời gian', 'Từ không gian hồ Hoàn Kiếm đến phố nghề, từ Văn Miếu đến Hoàng thành Thăng Long, Hà Nội gợi mở nhiều cách tìm hiểu một thành phố. Những công trình và sinh hoạt thường ngày nối câu chuyện di sản với nhịp sống đô thị.'),
    'quang-ninh': ('Quảng Ninh: từ biển đảo đến núi rừng Yên Tử', 'Quảng Ninh không chỉ có cảnh quan vịnh. Bên cạnh đảo đá, bãi biển và bờ đá là không gian kiến trúc tôn giáo ở Yên Tử và những câu chuyện được lưu giữ tại bảo tàng địa phương. Sổ tay kết nối các điểm đến ấy thành một hành trình đọc cảnh quan và văn hóa.'),
    'lao-cai': ('Lào Cai: những câu chuyện giữa núi cao và mặt hồ', 'Sa Pa và Fansipan mở ra góc nhìn về núi cao; Mù Cang Chải gắn với ruộng bậc thang; hồ Thác Bà và Ngòi Tu đưa người đọc đến cảnh quan hồ và đời sống cộng đồng. Mỗi địa danh là một lát cắt, giúp cảm nhận sự đa dạng của vùng đất này.'),
}
# Edited prose preserves the scope and citations of each corresponding seed section.
PROSE = {
 'ha-noi': {
  0: 'Hà Nội có thể được khám phá qua những không gian rất khác nhau: di tích hoàng thành, nơi ghi dấu truyền thống học tập, phố nghề, hồ nước và bảo tàng. Tám địa danh trong sổ tay kết nối những lát cắt ấy, từ Hồ Hoàn Kiếm và phố cổ đến Văn Miếu – Quốc Tử Giám, Hoàng thành Thăng Long và các công trình văn hóa của thủ đô.',
  3: 'Nhiều tên phố bắt đầu bằng Hàng gợi lại hoạt động nghề và buôn bán: Hàng Bạc, Hàng Mã, Hàng Đường. Đọc tên phố là một cách tiếp cận ký ức đô thị. Ở một không gian khác, Bảo tàng Dân tộc học Việt Nam giới thiệu đời sống văn hóa của các cộng đồng dân tộc trên cả nước. Lăng Chủ tịch Hồ Chí Minh là nơi tưởng niệm, đòi hỏi cách ứng xử trang nghiêm khi tham quan.',
  4: 'Trong các tuyến đi bộ được nguồn du lịch giới thiệu, phở và cà phê trứng là những hương vị có thể gặp khi khám phá Hà Nội; phở cuốn và phở chiên phồng cũng xuất hiện trong trải nghiệm ẩm thực đô thị. Những tên món này giúp mở rộng câu chuyện từ di tích sang đời sống thường ngày. Sổ tay chưa có dữ liệu xác nhận về công thức, giá món hay từng cơ sở phục vụ.',
  5: 'Một hành trình tìm hiểu Hà Nội có thể đi theo chủ đề: lịch sử ở Hoàng thành Thăng Long, truyền thống giáo dục ở Văn Miếu – Quốc Tử Giám, nghề và thương mại ở phố cổ, hoặc văn hóa cộng đồng tại bảo tàng. Các tuyến đi bộ trong nguồn là gợi ý đọc không gian thành phố; lối vào, lịch hoạt động và điều kiện thực tế cần được kiểm tra trước chuyến đi.'
 },
 'quang-ninh': {
  0: 'Từ Vịnh Hạ Long đến Cô Tô, Quan Lạn và Yên Tử, Quảng Ninh mở ra hai không gian nổi bật: biển đảo và núi rừng. Bảo tàng – Thư viện Quảng Ninh bổ sung một điểm dừng để tìm hiểu di sản địa phương. Phạm vi hành chính trong kho tư liệu được ghi theo Nghị quyết 36/2026/QH16, hiệu lực từ ngày 01/09/2026; những bài du lịch cũ vẫn mang tên tỉnh theo thời điểm xuất bản.',
  3: 'Ở Yên Tử, chùa, am và tháp tạo thành một không gian kiến trúc gắn với sinh hoạt Phật giáo. Quan Lạn có cụm đình, đền, chùa, cho thấy hành trình biển đảo cũng có thể là hành trình tìm hiểu di sản văn hóa. Bảo tàng – Thư viện Quảng Ninh giữ vai trò lưu giữ và giới thiệu di sản địa phương. Hoạt động hành hương được tiếp cận như sinh hoạt tín ngưỡng của cộng đồng.',
  4: 'Bài giới thiệu Cô Tô nhắc đến mực, hàu, bề bề và sá sùng, gợi mở câu chuyện ẩm thực gắn với biển. Đây là các nguyên liệu được nguồn du lịch giới thiệu, không phải danh sách những món chỉ có ở Quảng Ninh. Việc chọn món, tìm cơ sở phục vụ và tham khảo giá cần thêm thông tin tại thời điểm chuyến đi.'
 },
 'lao-cai': {
  0: 'Các địa danh trong sổ tay Lào Cai trải từ Sa Pa, Fansipan và Bắc Hà đến Mù Cang Chải, Khau Phạ, hồ Thác Bà và Ngòi Tu. Phạm vi này theo sắp xếp năm 2025, gồm Lào Cai và Yên Bái trước đây. Vì vậy, tên Yên Bái trong những bài du lịch cũ cần được đọc theo thời điểm của nguồn, thay vì coi là một địa phương nằm ngoài phạm vi bài viết.',
  2: 'Câu chuyện lịch sử trong phần tư liệu hiện có đi từ sự thay đổi phạm vi hành chính năm 2025 đến mối liên hệ giữa hồ Thác Bà và công trình thủy điện. Bên cạnh đó, ruộng bậc thang được đọc như một cảnh quan nông nghiệp gắn với sinh kế. Những lát cắt này chưa đủ để lập niên biểu lịch sử toàn tỉnh hoặc xác định niên đại từng làng.',
  3: 'Ở Mù Cang Chải, nguồn du lịch giới thiệu nghề dệt của người Mông. Tại Ngòi Tu bên hồ Thác Bà, câu chuyện lại gắn với nhà sàn, nghề đan và sinh hoạt của cộng đồng Dao. Những mô tả ấy cho thấy sự đa dạng của đời sống địa phương; mỗi nét văn hóa cần được hiểu trong cộng đồng và không gian cụ thể mà nguồn đề cập.',
  4: 'Cơm lam và món gà nấu măng chua được bài giới thiệu hồ Thác Bà nhắc đến trong trải nghiệm địa phương. Tên món giúp người đọc hình dung một phần hương vị của chuyến đi, nhưng chưa cung cấp công thức, thực đơn, giá hay địa chỉ phục vụ. Phần ẩm thực Sa Pa và Bắc Hà cần thêm nguồn chuyên biệt để kể sâu hơn.'
 }
}
parser = argparse.ArgumentParser()
parser.add_argument('--committed-seeds', action='store_true', help='Use Git HEAD datasets while unrelated dataset edits are in progress')
args = parser.parse_args()
editorial = json.loads((ROOT / 'content/regional-overviews.json').read_text())
regions = {}
for slug, (title, lead) in LEADS.items():
    seed_path = ROOT.parent / f'{slug}-data/seed.json'
    raw = subprocess.check_output(['git', 'show', f'HEAD:chung-khao/{slug}-data/seed.json'], cwd=ROOT) if args.committed_seeds else seed_path.read_text()
    seed = json.loads(raw)
    sources = {s['id']: s for s in seed['sources']}
    sections = [dict(item) for item in seed['overview_sections']]
    for index, text in PROSE.get(slug, {}).items():
        sections[index]['text'] = text
    overview = editorial['regions'][slug]
    sources.update({s['id']: s for s in overview['sources']})
    for index, item in [(0, dict(text=overview['summary'], source_ids=overview['source_ids'])),
                        (1, overview['sections'][1]), (2, overview['sections'][2]), (3, overview['sections'][3])]:
        sections[index].update(item)
    for item in [overview, *overview['sections'], *overview['representatives']]:
        for source_id in item['source_ids']:
            assert source_id in sources, (slug, source_id)
    places = []
    for place in seed['places']:
        facts = [f for f in seed['facts'] if f.get('entity_id') == place['id'] and f.get('status') in ('source_checked', 'dated_reference')]
        places.append({**place, 'facts': facts})
    for item in [*sections, *places, *(f for p in places for f in p['facts'])]:
        for source_id in item['source_ids']:
            assert source_id in sources, (slug, source_id)
    regions[slug] = dict(name=seed['scope']['province_name'], title=title, lead=overview['lead'], overview={k:v for k,v in overview.items() if k!='sources'}, overviewReviewedOn=editorial['reviewed_on'],
                         researchedOn=max(seed['researched_on'], editorial['reviewed_on']), sections=sections,
                         places=places, sources=sources)
output = ROOT / 'dist/assets/articles.json'
output.write_text(json.dumps({'regions': regions}, ensure_ascii=False, indent=2) + '\n')
print(f'Built {len(regions)} regional articles and {sum(len(r["places"]) for r in regions.values())} place profiles')
