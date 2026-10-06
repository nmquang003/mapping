const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const icons = {
 arrow:'<path d="M4 12h16m-6-6 6 6-6 6"/>', back:'<path d="M20 12H4m6-6-6 6 6 6"/>',
 pin:'<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2.4"/>',
 map:'<path d="m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2ZM9 3v16m6-14v16"/>',
 book:'<path d="M12 5C8 2 3 3 3 3v16s5-1 9 2c4-3 9-2 9-2V3s-5-1-9 2Zm0 0v16"/>',
 bookmark:'<path d="M6 3h12v18l-6-4-6 4Z"/>', check:'<path d="m5 12 4 4L19 6"/>',
 chevron:'<path d="m9 5 7 7-7 7"/>', focus:'<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5"/><circle cx="12" cy="12" r="3"/>',
 info:'<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v1"/>', external:'<path d="M14 3h7v7m0-7L10 14M10 3H3v18h18v-7"/>'
};
const icon = name => `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">${icons[name] || icons.pin}</svg>`;
const sourceTravel = 'https://vietnam.travel/vietnam-virtual-tours';
const destinations = [
 {id:'ninh-binh',name:'Ninh Bình',province:15,provinceName:'Ninh Bình',number:'01',tag:'Non nước & dấu xưa',subtitle:'Giữa miền di sản, nghe non nước kể chuyện.',coords:[105.974,20.25],callout:[-49,35],
  description:'Khám phá cảnh quan núi đá vôi, những tuyến sông uốn lượn và dấu tích cố đô qua các địa danh của Ninh Bình.',
  headline:'Một miền non nước, nhiều lớp ký ức',geography:'Bản mẫu tập trung vào khu vực Tràng An, Tam Cốc, Hang Múa và cố đô Hoa Lư. Bản đồ nền hiển thị ranh giới tỉnh; phạm vi nội dung hiện chỉ gồm các điểm đến được liệt kê.',
  culture:'Hành trình văn hóa có thể bắt đầu từ không gian lễ hội, nghề thủ công và bữa ăn địa phương. Những câu chuyện về cơm cháy, món dê và sinh hoạt cộng đồng sẽ được biên soạn có nguồn ở bản tiếp theo.',topics:['Cảnh quan núi đá vôi','Không gian cố đô Hoa Lư','Lễ hội và sinh hoạt cộng đồng','Ẩm thực địa phương'],
  history:[['Dấu tích cố đô','Hoa Lư trong dòng lịch sử','Phần này sẽ giới thiệu vai trò của Hoa Lư và các di tích liên quan, kèm mốc thời gian được đối chiếu tài liệu.'],['Di sản & hiện tại','Một cảnh quan đang được gìn giữ','Bổ sung câu chuyện bảo tồn, cộng đồng địa phương và mối liên hệ giữa cảnh quan tự nhiên với di sản văn hóa.']],
  source:'https://vietnam.travel/places-to-go/northern-vietnam/ninh-binh',tour:sourceTravel,
  places:[['trang-an','Tràng An',105.922,20.252,'Cảnh quan','Một hành trình qua sông nước, hang động và những dãy núi đá vôi.'],['tam-coc','Tam Cốc',105.936,20.215,'Sông nước','Tìm hiểu cảnh quan dòng sông và đồng ruộng giữa những dãy núi.'],['hang-mua','Hang Múa',105.938,20.23,'Điểm ngắm cảnh','Một điểm khám phá cảnh quan quanh khu vực Tam Cốc.'],['hoa-lu','Cố đô Hoa Lư',105.905,20.284,'Lịch sử','Không gian di tích để bắt đầu tìm hiểu câu chuyện về cố đô.']]},
 {id:'ha-noi',name:'Hà Nội',province:1,provinceName:'Hà Nội',number:'02',tag:'Ngàn năm văn hiến',subtitle:'Những lớp thời gian giữa nhịp sống phố phường.',coords:[105.854,21.028],callout:[39,-22],
  description:'Một hành trình qua hồ nước, phố cổ và các di tích để tìm hiểu lịch sử, văn hóa và đời sống của Hà Nội.',
  headline:'Đọc thành phố qua những lớp thời gian',geography:'Sổ tay giới thiệu một nhóm địa danh ở khu vực trung tâm Hà Nội. Vị trí trên bản đồ giúp bạn liên kết các điểm đến với không gian thành phố.',
  culture:'Văn hóa Hà Nội hiện diện trong nếp sống phố phường, nghề truyền thống và ẩm thực. Phở, bún chả và những không gian sinh hoạt quanh hồ là các chủ đề dự kiến được bổ sung.',topics:['Không gian hồ và phố','Di sản Thăng Long','Đời sống đô thị','Phở, bún chả và ẩm thực'],
  history:[['Thăng Long','Dấu tích một kinh đô','Nội dung sẽ liên kết các mốc lịch sử với di tích Hoàng thành Thăng Long và tài liệu tham khảo.'],['Đời sống phố phường','Ký ức trong thành phố','Bổ sung các câu chuyện về phố cổ, nghề truyền thống và sự thay đổi của không gian đô thị.']],
  source:'https://vietnam.travel/places-to-go/northern-vietnam/ha-noi',tour:'https://vietnam.travel/things-to-do/vietnam-360-degrees',
  places:[['ho-hoan-kiem','Hồ Hoàn Kiếm',105.852,21.028,'Cảnh quan','Hồ nước và không gian sinh hoạt quen thuộc ở trung tâm Hà Nội.'],['van-mieu','Văn Miếu – Quốc Tử Giám',105.836,21.028,'Văn hóa','Một địa danh để khám phá truyền thống học tập và kiến trúc.'],['hoang-thanh','Hoàng thành Thăng Long',105.84,21.035,'Lịch sử','Không gian di tích gợi mở những lớp lịch sử của Thăng Long.'],['pho-co','Phố cổ Hà Nội',105.853,21.035,'Đời sống','Những tuyến phố để tìm hiểu đời sống, nghề và văn hóa đô thị.']]},
 {id:'ha-long',name:'Hạ Long',province:10,provinceName:'Quảng Ninh',number:'03',tag:'Kỳ quan giữa biển trời',subtitle:'Một thế giới núi đá, sóng nước và làng chài.',coords:[107.083,20.95],callout:[88,14],
  description:'Từ cảnh quan vịnh đến đời sống ven biển, khám phá Hạ Long qua những địa danh tiêu biểu và câu chuyện địa phương.',
  headline:'Nơi núi đá gặp những con sóng',geography:'Phạm vi bản mẫu là khu vực Hạ Long và một số địa danh trên vịnh. Ranh giới Quảng Ninh trên bản đồ giúp định hướng; sổ tay chưa bao phủ toàn bộ tỉnh.',
  culture:'Đời sống ven biển, văn hóa làng chài và ẩm thực hải sản là những chủ đề sẽ được biên soạn. Nội dung về chả mực và nghề biển sẽ được bổ sung cùng nguồn tham khảo.',topics:['Cảnh quan vịnh','Không gian hang động','Văn hóa cộng đồng ven biển','Chả mực và hải sản'],
  history:[['Đất & nước','Câu chuyện hình thành cảnh quan','Phần này sẽ bổ sung thông tin địa chất đã được kiểm chứng, với minh họa và nguồn dẫn.'],['Con người & di sản','Đời sống bên bờ vịnh','Bổ sung tư liệu về cộng đồng, hoạt động bảo tồn và văn hóa địa phương.']],
  source:'https://vietnam.travel/places-to-go/northern-vietnam/ha-long',tour:sourceTravel,
  places:[['vinh-ha-long','Vịnh Hạ Long',107.107,20.875,'Cảnh quan','Khám phá không gian biển và những đảo đá vôi qua bản đồ.'],['hang-sung-sot','Hang Sửng Sốt',107.19,20.843,'Hang động','Một điểm đến để tìm hiểu cảnh quan hang động trên vịnh.'],['ti-top','Đảo Ti Tốp',107.181,20.858,'Đảo & biển','Không gian đảo và một góc nhìn ra cảnh quan vịnh.'],['bao-tang','Bảo tàng Quảng Ninh',107.101,20.95,'Văn hóa','Nơi bắt đầu tìm hiểu thiên nhiên, lịch sử và con người địa phương.']]},
 {id:'sa-pa',name:'Sa Pa',province:4,provinceName:'Lào Cai',number:'04',tag:'Miền mây & sắc bản',subtitle:'Theo triền núi, gặp những câu chuyện bản làng.',coords:[103.844,22.336],callout:[-72,-18],
  description:'Khám phá cảnh quan núi cao, thung lũng và những nét văn hóa cộng đồng qua một số địa danh ở Sa Pa.',
  headline:'Một hành trình giữa núi, mây và bản làng',geography:'Phạm vi nội dung tập trung vào khu vực Sa Pa và các địa danh được chọn. Bản đồ sử dụng ranh giới Lào Cai để định hướng và dấu vị trí riêng cho Sa Pa.',
  culture:'Các câu chuyện văn hóa cần được thể hiện theo từng cộng đồng và có nguồn rõ ràng. Trang này sẽ bổ sung nội dung về nghề dệt, sinh hoạt bản làng và ẩm thực, tôn trọng sự đa dạng địa phương.',topics:['Cảnh quan núi và thung lũng','Ruộng bậc thang','Nghề thủ công địa phương','Văn hóa các cộng đồng'],
  history:[['Bản làng','Những câu chuyện địa phương','Bổ sung tư liệu về cộng đồng và các địa danh; phân biệt rõ lịch sử được ghi nhận với truyền kể.'],['Sa Pa hôm nay','Cảnh quan và đời sống','Bổ sung thông tin về bảo tồn văn hóa, thiên nhiên và sự thay đổi của không gian địa phương.']],
  source:'https://vietnam.travel/places-to-go/northern-vietnam/sapa',tour:null,
  places:[['fansipan','Fansipan',103.775,22.303,'Núi cao','Một địa danh gắn với cảnh quan núi Hoàng Liên Sơn.'],['cat-cat','Bản Cát Cát',103.832,22.331,'Bản làng','Điểm khám phá đời sống và nghề thủ công địa phương.'],['muong-hoa','Thung lũng Mường Hoa',103.878,22.298,'Thung lũng','Không gian cảnh quan và bản làng để tìm hiểu vùng Sa Pa.'],['nha-tho','Nhà thờ đá Sa Pa',103.842,22.336,'Kiến trúc','Một dấu mốc kiến trúc trong khu vực trung tâm Sa Pa.']]}
];
const tabs = [['tong-quan','Địa lý – Tổng quan'],['dia-danh','Địa danh'],['bo-anh','Bộ ảnh AI'],['lich-su','Lịch sử'],['van-hoa','Văn hóa – Ẩm thực'],['nguon','Nguồn tham khảo']];
const destinationById = id => destinations.find(d => d.id === id);
let geo, credits = [], activeLocalPlace, previousDestination, toastTimer;
let aiRegions = {};
const mediaRegion = d => ({'ha-long':'quang-ninh','sa-pa':'lao-cai'}[d.id] || d.id);
const imagesFor = d => aiRegions[mediaRegion(d)]?.images || [];
const placeAliases = {'van-mieu':'van-mieu-quoc-tu-giam','hoang-thanh':'hoang-thanh-thang-long','pho-co':'pho-co-ha-noi','bao-tang':'bao-tang-quang-ninh'};
const imageForPlace = (d,id) => imagesFor(d).find(image=>image.id===id || image.placeId===(placeAliases[id] || id));
function heroImage(d) {
 const preferred={'ha-noi':'ho-hoan-kiem','ha-long':'vinh-ha-long','sa-pa':'sa-pa','ninh-binh':'trang-an'}[d.id];
 return imageForPlace(d,preferred) || imagesFor(d)[0];
}
function heroAttributes(d) {
 const image=heroImage(d);
 return `src="${escapeHTML(image?.src || `assets/${d.id}.jpg`)}" alt="${escapeHTML(image?.alt || photoDescription(d.id))}"`;
}
function placeImage(d,id,compact=false) {
 const image=imageForPlace(d,id);
 return image?`<figure class="place-illustration${compact?' compact':''}"><button type="button" data-ai-image="${escapeHTML(image.id)}" data-ai-destination="${d.id}" aria-label="Xem ảnh lớn ${escapeHTML(image.name)}"><img src="${escapeHTML(image.src)}" alt="${escapeHTML(image.alt)}" width="1536" height="864" loading="lazy" decoding="async"></button><figcaption>Minh họa do AI tạo</figcaption></figure>`:'';
}
function selectedPlaceView(d,p) { return `${placeImage(d,p[0],true)}<span class="eyebrow">${p[4]}</span><h3>${p[1]}</h3><p>${p[5]}</p>`; }
function galleryView(d) {
 const images=imagesFor(d), region=aiRegions[mediaRegion(d)];
 return `<div class="section-heading"><h2>Bộ ảnh ${escapeHTML(region?.name || d.provinceName)}</h2><span>${images.length} hình minh họa</span></div><p class="gallery-intro">Khám phá các địa danh qua hình minh họa do AI tạo. Chọn một ảnh để xem lớn và đọc giới thiệu. Ảnh không phải tư liệu hay bản đồ dẫn đường.</p>${images.length?`<div class="ai-gallery">${images.map(image=>`<figure class="gallery-item"><button type="button" data-ai-image="${escapeHTML(image.id)}" data-ai-destination="${d.id}" aria-label="Xem ảnh lớn ${escapeHTML(image.name)}"><img src="${escapeHTML(image.src)}" alt="${escapeHTML(image.alt)}" width="1536" height="864" loading="lazy" decoding="async"><span class="gallery-expand" aria-hidden="true">${icon('focus')}</span></button><figcaption><strong>${escapeHTML(image.name)}</strong><span>Minh họa do AI tạo</span></figcaption></figure>`).join('')}</div>`:`<div class="gallery-empty"><h3>Bộ ảnh đang được chuẩn bị</h3><p>Sổ tay sẽ bổ sung hình minh họa cho các địa danh tại ${escapeHTML(d.provinceName)}.</p></div>`}`;
}
function openImage(d,id) {
 const image=imagesFor(d).find(image=>image.id===id);if(!image)return;
 // A map dialog can already be open: the native dialog stack restores focus on close.
 openInfo(escapeHTML(image.name),`<figure class="image-full"><img src="${escapeHTML(image.src)}" alt="${escapeHTML(image.alt)}" width="1536" height="864"><figcaption>${escapeHTML(image.caption)}</figcaption></figure><p>${escapeHTML(image.summary)}</p><div class="source-item"><strong>Nguồn giới thiệu địa danh</strong>${image.sources.map(source=>`<p><a href="${escapeHTML(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(source.title)} ↗</a></p>`).join('')}<p>Nguồn hỗ trợ nội dung giới thiệu; hình minh họa không xác nhận từng chi tiết kiến trúc hoặc cảnh quan.</p></div>`);
 infoDialog.classList.add('image-viewer');
}
let saved = [];
try { const value = JSON.parse(localStorage.getItem('atlas-viet-saved') || '[]'); if (Array.isArray(value)) saved = value.filter(id => destinationById(id)); } catch {}
const main = $('#main');
const dialog = $('#destination-dialog');
const infoDialog = $('#info-dialog');
function notify(message) { const toast=$('#toast'); toast.textContent=message; toast.hidden=false; clearTimeout(toastTimer); toastTimer=setTimeout(()=>toast.hidden=true,4200); }
function updateSavedCount() { $('#saved-count').textContent=saved.length; }
function toggleSaved(id) {
 const had=saved.includes(id); saved=had?saved.filter(v=>v!==id):[...saved,id];
 try { localStorage.setItem('atlas-viet-saved',JSON.stringify(saved)); } catch { notify('Không thể lưu lâu dài trên trình duyệt này. Sổ tay vẫn dùng được trong phiên hiện tại.'); }
 updateSavedCount(); updateSaveButton(id);
 notify(had?'Đã bỏ điểm đến khỏi sổ tay.':'Đã lưu điểm đến vào sổ tay của bạn.');
}
function updateSaveButton(id) { const button=$('[data-save="'+id+'"]'); if(button) { button.innerHTML=icon(saved.includes(id)?'check':'bookmark')+(saved.includes(id)?'Đã lưu vào sổ tay':'Lưu vào sổ tay'); button.setAttribute('aria-pressed',String(saved.includes(id))); } }
function project([lon,lat]) { return [(lon-101)*46*Math.cos(16*Math.PI/180),(24.5-lat)*46]; }
function polygons(feature) { return feature.geometry.type==='MultiPolygon'?feature.geometry.coordinates:[feature.geometry.coordinates]; }
function pathFor(feature) { return polygons(feature).map(poly=>poly.map(ring=>ring.map((p,i)=>{const [x,y]=project(p);return (i?'L':'M')+x.toFixed(2)+','+y.toFixed(2);}).join('')+'Z').join('')).join(''); }
function boundsFor(features, coordinates=[]) {
 let points=coordinates.map(project);
 features.forEach(feature=>polygons(feature).forEach(poly=>poly.forEach(ring=>points.push(...ring.map(project)))));
 if(!points.length) return [0,0,700,780];
 const xs=points.map(p=>p[0]),ys=points.map(p=>p[1]);const x=Math.min(...xs),y=Math.min(...ys),right=Math.max(...xs),bottom=Math.max(...ys);
 return [x,y,right-x,bottom-y];
}
function scopeDestination(feature) { return destinations.find(d=>d.province===feature.properties.atlasId); }
function provincePaths(local=false, selected) { return geo.features.map(f=>`<path d="${pathFor(f)}" class="${local?'local-province'+(f.properties.atlasId===selected?' selected':''):'province'+(scopeDestination(f)?' in-scope':'')}" ${local?'':`data-province="${f.properties.atlasId}" data-name="${escapeHTML(f.properties.name)}"`} fill-rule="evenodd"><title>${escapeHTML(f.properties.name)}</title></path>`).join(''); }
function countryMarker(d) {
 const [x,y]=project(d.coords),[dx,dy]=d.callout; const textX=x+dx,textY=y+dy;
 return `<g class="marker" role="button" tabindex="0" data-open="${d.id}" aria-label="Khám phá ${d.name}"><line class="marker-line" x1="${x}" y1="${y}" x2="${textX}" y2="${textY-3}"/><circle class="pulse" cx="${x}" cy="${y}" r="12"/><circle class="outer" cx="${x}" cy="${y}" r="6"/><circle class="inner" cx="${x}" cy="${y}" r="2.5"/><text class="marker-label" x="${textX}" y="${textY}" text-anchor="${dx<0?'end':'start'}">${d.name}</text></g>`;
}
function destinationCard(d) { return `<button class="destination-card" data-open="${d.id}" data-card="${d.id}" aria-label="Khám phá ${d.name}"><span class="destination-thumb"><img ${heroAttributes(d)} width="76" height="58">${heroImage(d)?'<span class="thumb-label">Ảnh AI</span>':''}</span><span class="card-copy"><strong>${d.name}</strong><small>${d.tag}</small></span><span class="card-arrow">${icon('arrow')}</span></button>`; }
function photoDescription(id) { return {'ninh-binh':'Cảnh quan Tràng An với núi đá và thuyền trên sông','ha-noi':'Tháp Rùa giữa Hồ Hoàn Kiếm','ha-long':'Toàn cảnh vịnh với những đảo đá','sa-pa':'Ruộng bậc thang ở Sa Pa'}[id]; }
function homeView() {
 previousDestination=null;
 main.innerHTML=`<div class="atlas-layout"><section class="intro" aria-labelledby="home-title"><span class="eyebrow">ĐI QUA ĐỊA DANH · CHẠM VÀO TRI THỨC</span><h1 id="home-title">Mỗi miền đất,<br> một <em>câu chuyện.</em></h1><p class="intro-description">Mở bản đồ, chọn một miền đất. Cùng khám phá địa lý, lịch sử và những nét văn hóa làm nên bản sắc Việt Nam.</p><div class="intro-rule">Bốn điểm đến, một hành trình</div><div class="destination-list">${destinations.map(destinationCard).join('')}</div><p class="list-caption">${icon('pin')} Chọn trên bản đồ hoặc trong danh sách để bắt đầu</p></section><section class="map-panel" aria-label="Bản đồ khám phá Việt Nam"><div class="map-topbar"><span class="map-title">${icon('map')} BẢN ĐỒ VIỆT NAM</span><button id="focus-north">${icon('focus')} Đến 4 điểm khám phá</button></div><div class="map-viewport"><svg id="country-map" class="country-svg" viewBox="0 0 820 820" aria-label="Bản đồ 34 tỉnh thành Việt Nam" role="group">${provincePaths()}<text class="map-region-label" x="210" y="196">MIỀN BẮC</text><text class="map-region-label" x="337" y="423">MIỀN TRUNG</text><text class="map-region-label" x="215" y="710">MIỀN NAM</text><text class="sea-label" x="450" y="490" transform="rotate(-15 450 490)">Biển Đông</text>${islandLabels()}${destinations.map(countryMarker).join('')}</svg></div><div class="compass-decoration">BẮC<svg viewBox="0 0 32 48" aria-hidden="true"><path d="m16 5 7 26-7-7-7 7Z" fill="#667d60"/><path d="m16 5 7 26-7-7Z" fill="#c79a45"/><path d="M16 26v16" stroke="#667d60"/></svg></div><div class="map-controls" aria-label="Điều khiển bản đồ"><button data-zoom="in" aria-label="Phóng to">+</button><button data-zoom="out" aria-label="Thu nhỏ">−</button><button data-zoom="reset" aria-label="Hiện toàn bộ bản đồ">${icon('focus')}</button></div><div class="map-legend"><span><i class="legend-dot"></i> Có trong sổ tay</span><span><i class="legend-dot muted"></i> Chưa có nội dung</span></div><button class="map-attribution" data-sources>Ranh giới tham khảo · Xem nguồn ↗</button><div id="map-tooltip" class="map-tooltip" hidden></div></section></div><div class="scope-strip">${icon('info')}<span><strong>Phạm vi sổ tay:</strong> Hà Nội, Ninh Bình, khu vực Hạ Long và Sa Pa.</span><span class="scope-divider"></span><span class="boundary-note">Nội dung ngắn dành cho bản mẫu · Sẽ tiếp tục bổ sung</span></div>`;
 initializeCountryMap();
}
function islandLabels() {
 const hs=project([112.0,16.6]),ts=project([114.7,10.5]);
 return `<text class="island-label" x="${hs[0]}" y="${hs[1]}">Quần đảo Hoàng Sa</text><text class="island-label" x="${ts[0]}" y="${ts[1]}">Quần đảo Trường Sa</text>`;
}
function initializeCountryMap() {
 const svg=$('#country-map'), viewport=$('.map-viewport'), tooltip=$('#map-tooltip');
 const bounds=boundsFor(geo.features); const base=[bounds[0]-70,bounds[1]-45,Math.max(bounds[2]+110,680),bounds[3]+85];
 let box=[...base], drag=null, dragged=false;
 const setBox=()=>svg.setAttribute('viewBox',box.join(' '));setBox();
 function zoom(factor,center) { const max=base[2]*1.4,min=base[2]/6;let newW=Math.max(min,Math.min(max,box[2]*factor));let ratio=newW/box[2];let point=center||[box[0]+box[2]/2,box[1]+box[3]/2];box=[point[0]+(box[0]-point[0])*ratio,point[1]+(box[1]-point[1])*ratio,newW,box[3]*ratio];setBox();tooltip.hidden=true; }
 $('#focus-north').onclick=()=>{const points=destinations.map(d=>project(d.coords));const minX=Math.min(...points.map(p=>p[0])),maxX=Math.max(...points.map(p=>p[0]));const minY=Math.min(...points.map(p=>p[1])),maxY=Math.max(...points.map(p=>p[1]));box=[minX-110,minY-65,maxX-minX+245,maxY-minY+190];setBox();};
 $$('[data-zoom]').forEach(button=>button.onclick=()=>{if(button.dataset.zoom==='reset'){box=[...base];setBox();}else zoom(button.dataset.zoom==='in'?.8:1.25);});
 function svgPoint(event) { const p=new DOMPoint(event.clientX,event.clientY);return p.matrixTransform(svg.getScreenCTM().inverse()); }
 viewport.addEventListener('wheel',event=>{event.preventDefault();const p=svgPoint(event);zoom(event.deltaY<0?.9:1.1,[p.x,p.y]);},{passive:false});
 viewport.addEventListener('pointerdown',event=>{if(event.button!==0)return;drag={x:event.clientX,y:event.clientY,box:[...box]};dragged=false;});
 viewport.addEventListener('pointermove',event=>{
  if(drag){const dx=event.clientX-drag.x,dy=event.clientY-drag.y;if(Math.hypot(dx,dy)>5)dragged=true;if(dragged){const scale=svg.getScreenCTM().a;box=[drag.box[0]-dx/scale,drag.box[1]-dy/scale,drag.box[2],drag.box[3]];setBox();tooltip.hidden=true;}return;}
  const province=event.target.closest('[data-province]');
  if(province){const rect=$('.map-panel').getBoundingClientRect();tooltip.textContent=province.dataset.name+(destinations.some(d=>d.province===Number(province.dataset.province))?' · Chọn để khám phá':' · Chưa có trong sổ tay');tooltip.hidden=false;tooltip.style.left=Math.min(event.clientX-rect.left+12,rect.width-220)+'px';tooltip.style.top=(event.clientY-rect.top+13)+'px';}else tooltip.hidden=true;
 });
 viewport.addEventListener('pointerup',()=>drag=null);
 viewport.addEventListener('pointercancel',()=>drag=null);
 viewport.addEventListener('pointerleave',()=>{tooltip.hidden=true;drag=null;});
 viewport.addEventListener('click',event=>{if(dragged){event.stopPropagation();dragged=false;}},true);
 $$('[data-open]',svg).forEach(marker=>{marker.addEventListener('mouseenter',()=>{const d=destinationById(marker.dataset.open);$$(`[data-card="${d.id}"]`).forEach(c=>c.classList.add('map-hover'));});marker.addEventListener('mouseleave',()=>$$('.map-hover').forEach(c=>c.classList.remove('map-hover')));});
}
function localViewBox(d) {
 if(d.id==='ha-noi'||d.id==='sa-pa'||d.id==='ha-long'){
  const coords=d.places.map(p=>[p[2],p[3]]);let [x,y,w,h]=boundsFor([],coords);const minimum=d.id==='ha-noi'?2.8:d.id==='sa-pa'?6:9;w=Math.max(w,minimum);h=Math.max(h,minimum*.75);return [x-w*.35,y-h*.35,w*1.75,h*1.75];
 }
 const province=geo.features.find(f=>f.properties.atlasId===d.province);const [x,y,w,h]=boundsFor([province]);return [x-w*.12,y-h*.15,w*1.24,h*1.3];
}
function localMap(d) {
 const box=localViewBox(d),scale=box[2]/(innerWidth<760?310:540);const dot=5*scale;const font=11*scale;
 const offsets={'ha-noi':[[20,28],[-22,22],[-20,-20],[24,-20]],'ninh-binh':[[-38,3],[25,32],[39,-11],[-30,-28]],'ha-long':[[25,30],[23,26],[25,-22],[18,-15]],'sa-pa':[[18,20],[-22,24],[20,20],[23,-22]]};
 return `<svg viewBox="${box.join(' ')}" role="group" aria-label="Bản đồ các địa danh tại ${d.name}">${provincePaths(true,d.province)}${d.places.map((p,i)=>{const [x,y]=project([p[2],p[3]]),[dx,dy]=offsets[d.id][i]; const distributed=d.id!=="ninh-binh"||innerWidth<760; const side=d.id==="ha-noi"?[true,false,false,true][i]:[false,true,true,false][i]; const targetX=distributed?box[0]+box[2]*(side?.92:.08):x+dx*scale; const targetY=distributed?box[1]+box[3]*[.66,.82,.4,.23][i]:y+dy*scale; const anchor=distributed?(side?"end":"start"):(dx<0?"end":"start");return `<g class="local-marker${i===0?' is-active':''}" data-place="${p[0]}" role="button" tabindex="0" aria-label="${p[1]}"><line x1="${x}" y1="${y}" x2="${targetX}" y2="${targetY-3*scale}" stroke="#748e63" stroke-width="${scale*.6}"/><circle cx="${x}" cy="${y}" r="${dot}"/><text x="${targetX}" y="${targetY}" style="font-size:${font}px;stroke-width:${4*scale}px" text-anchor="${anchor}">${p[1]}</text></g>`;}).join('')}</svg>`;
}
function openDestination(id) {
 const d=destinationById(id);if(!d)return;
 activeLocalPlace=d.places[0][0];
 $('#dialog-content').innerHTML=`<div class="dialog-header"><div><span class="eyebrow">${d.provinceName} · BẢN ĐỒ KHÁM PHÁ</span><h2 id="destination-title">${d.name} <span class="muted">/</span> ${d.tag}</h2></div><button class="icon-button" data-close-destination aria-label="Đóng bản đồ địa phương">×</button></div><div class="dialog-grid"><div class="local-map-panel">${localMap(d)}<div class="local-map-caption">Vị trí minh họa gần đúng · Chọn dấu mốc để khám phá · Đang đối chiếu tọa độ</div></div><div class="dialog-sidebar"><span class="eyebrow">BẮT ĐẦU HÀNH TRÌNH</span><p>${d.description}</p><div class="local-place-list">${d.places.map((p,i)=>`<button class="place-list-button${i===0?' is-active':''}" data-place="${p[0]}"><span class="number">0${i+1}</span><strong>${p[1]}</strong>${icon('chevron')}</button>`).join('')}</div><div class="selected-place" id="selected-place">${selectedPlaceView(d,d.places[0])}</div><a id="detail-link" class="primary-button" href="#/dia-phuong/${d.id}?tab=dia-danh&diem=${activeLocalPlace}">Tìm hiểu chi tiết ${icon('arrow')}</a></div></div>`;
 $('#dialog-content').dataset.destination=id;
 if(!dialog.open)dialog.showModal();
 $$('[data-place]',dialog).forEach(el=>el.addEventListener('click',()=>selectLocalPlace(d,el.dataset.place)));
 $('[data-close-destination]',dialog).onclick=()=>dialog.close();
 $('#detail-link').onclick=()=>dialog.close();
}
function selectLocalPlace(d,id) {
 const p=d.places.find(p=>p[0]===id);if(!p)return;activeLocalPlace=id;
 $$('[data-place]',dialog).forEach(el=>el.classList.toggle('is-active',el.dataset.place===id));
 $('#selected-place').innerHTML=selectedPlaceView(d,p);
 $('#detail-link').href=`#/dia-phuong/${d.id}?tab=dia-danh&diem=${id}`;
}
function creditFor(d) { return credits.find(c=>c.id===d.id); }
function photoCredit(d) { const image=heroImage(d);if(image)return `${escapeHTML(image.name)} · Minh họa do AI tạo bằng API Ban tổ chức · Không phải ảnh tư liệu`; const c=creditFor(d);return c?`Ảnh thực tế dùng tạm · <a href="${c.source}" target="_blank" rel="noopener noreferrer">${escapeHTML(c.author)} / Wikimedia Commons</a> · <a href="${c.licenseUrl}" target="_blank" rel="noopener noreferrer">${c.license}</a> · Thu nhỏ, cắt khung hiển thị`:'Ảnh giao diện tạm thời · Chưa phải hình minh họa AI'; }
function detailView(id,params) {
 const d=destinationById(id);if(!d){notFound();return;}
 const tab=tabs.some(([t])=>t===params.get('tab'))?params.get('tab'):'tong-quan';
 const changed=previousDestination!==id;previousDestination=id;
 main.innerHTML=`<div class="detail-shell"><div class="breadcrumb"><a href="#/">${icon('back')} Bản đồ Việt Nam</a><span>/</span><span>${d.name}</span></div><section class="detail-hero" aria-labelledby="detail-title"><img ${heroAttributes(d)}><div class="detail-hero-content"><span class="eyebrow">ĐIỂM ĐẾN ${d.number} · ${d.tag}</span><h1 id="detail-title">${d.name}</h1><p>${d.subtitle} ${d.description}</p></div></section><p class="photo-caption">${photoCredit(d)}</p><div class="detail-actions"><p>${icon('pin')} ${d.id==='ha-long'?'Phạm vi: khu vực Hạ Long':d.id==='sa-pa'?'Phạm vi: khu vực Sa Pa':'Phạm vi: các địa danh đã chọn ở '+d.name}<br>Nội dung bản mẫu · Đang biên soạn</p><button class="secondary-button" data-save="${d.id}" aria-pressed="${saved.includes(d.id)}">${icon(saved.includes(d.id)?'check':'bookmark')}${saved.includes(d.id)?'Đã lưu vào sổ tay':'Lưu vào sổ tay'}</button></div><div class="detail-tabs" role="tablist" aria-label="Nội dung sổ tay ${d.name}">${tabs.map(([key,label])=>`<button role="tab" id="tab-${key}" aria-selected="${key===tab}" aria-controls="tab-content" tabindex="${key===tab?0:-1}" data-tab="${key}" data-destination="${d.id}">${label}</button>`).join('')}</div><section class="tab-content" id="tab-content" role="tabpanel" aria-labelledby="tab-${tab}" tabindex="0">${tabView(d,tab)}</section></div>`;
 if(changed)window.scrollTo({top:0,behavior:'instant'});
 if(params.get('diem')){const p=$(`[data-place-card="${params.get('diem')}"]`);if(p){p.style.borderColor='#8ea387';p.style.background='#eef0e5';}}
}
function tabView(d,tab) {
 if(tab==='bo-anh')return galleryView(d);
 if(tab==='dia-danh')return `<div class="section-heading"><h2>Những nơi để bắt đầu</h2><span>04 địa danh · Đang biên soạn</span></div><div class="place-grid">${d.places.map((p,i)=>`<article class="place-card" data-place-card="${p[0]}">${placeImage(d,p[0])}<span class="place-index">0${i+1}</span><span class="eyebrow">${p[4]}</span><h3>${p[1]}</h3><p>${p[5]} Nội dung chi tiết sẽ được bổ sung cùng nguồn tham khảo.</p><span class="place-meta">${icon('pin')} Tọa độ tham khảo · Chưa đối chiếu</span><button class="secondary-button" data-open="${d.id}" data-open-place="${p[0]}">${icon('map')} Xem trên bản đồ</button></article>`).join('')}</div>${d.tour?`<p style="margin-top:22px"><a class="secondary-button" href="${d.tour}" target="_blank" rel="noopener noreferrer">Khám phá tour 360° trên Vietnam.travel ${icon('external')}</a></p>`:''}`;
 if(tab==='lich-su')return `<div class="section-heading"><h2>Dấu xưa, chuyện nay</h2><span>Khung nội dung dự kiến</span></div><div class="timeline">${d.history.map(h=>`<article class="timeline-item"><span class="eyebrow">${h[0]}</span><h3>${h[1]}</h3><p>${h[2]}</p></article>`).join('')}</div><span class="draft-badge">Mốc thời gian đang được đối chiếu tài liệu</span>`;
 if(tab==='van-hoa')return `<div class="editorial-grid"><div class="editorial-copy"><span class="eyebrow">VĂN HÓA · CON NGƯỜI · HƯƠNG VỊ</span><h2>Bản sắc trong những điều gần gũi</h2><p>${d.culture}</p><span class="draft-badge">Nội dung đang biên soạn</span></div><aside class="editorial-aside"><h3>Chủ đề sẽ khám phá</h3><ul>${d.topics.map(t=>`<li>${t}</li>`).join('')}</ul></aside></div>`;
 if(tab==='nguon')return `<div class="section-heading"><h2>Nguồn & sự minh bạch</h2><span>Cập nhật bản mẫu: 06/10/2026</span></div><p class="muted">Các liên kết dưới đây là nguồn để tiếp tục biên soạn. Bản mẫu chưa xác minh từng nhận định và tọa độ; chưa dùng cho câu trả lời AI.</p><div class="source-item"><strong>Thông tin điểm đến — Vietnam.travel</strong><p><a href="${d.source}" target="_blank" rel="noopener noreferrer">Trang giới thiệu ${d.name} ↗</a> · Cổng thông tin du lịch quốc gia</p></div><div class="source-item"><strong>Ảnh và hình minh họa</strong><p>${photoCredit(d)}</p><p>${imagesFor(d).length} ảnh AI trong bộ ảnh ${escapeHTML(d.provinceName)}. Các ảnh được gắn nhãn minh họa; không sử dụng làm bằng chứng lịch sử hoặc địa lý.</p><a class="secondary-button" href="#/dia-phuong/${d.id}?tab=bo-anh">Xem bộ ảnh ${icon('arrow')}</a></div><div class="source-item"><strong>Dữ liệu ranh giới bản đồ</strong><p><a href="https://github.com/thanglequoc/vietnamese-provinces-database" target="_blank" rel="noopener noreferrer">Vietnamese Provinces Database ↗</a> · Bản chụp GIS tháng 3/2026, có giản lược đường biên để hiển thị. Đây là nguồn cộng đồng, cần đối chiếu bản đồ chính thức trước khi nộp.</p></div>`;
 return `<div class="editorial-grid"><div class="editorial-copy"><span class="eyebrow">ĐỊA LÝ & TỔNG QUAN</span><h2>${d.headline}</h2><p>${d.geography}</p><p>${d.description}</p><button class="secondary-button" data-open="${d.id}">${icon('map')} Mở bản đồ địa phương</button></div><aside class="editorial-aside"><span class="eyebrow">TRONG SỔ TAY NÀY</span><h3>Bắt đầu từ bốn địa danh</h3><ul>${d.places.map(p=>`<li>${p[1]}</li>`).join('')}</ul><span class="draft-badge">Nội dung đang biên soạn</span></aside></div>`;
}
function openInfo(title,content) { infoDialog.classList.remove('image-viewer'); $('#info-content').innerHTML=`<span class="eyebrow">ATLAS VIỆT · SỔ TAY ĐIỆN TỬ</span><h2 id="info-title">${title}</h2>${content}`;if(!infoDialog.open)infoDialog.showModal(); }
function showSources() { openInfo('Nguồn dữ liệu & ghi chú',`<p>Bản mẫu giới thiệu bốn điểm đến: Hà Nội, Ninh Bình, Hạ Long và Sa Pa. Nội dung ngắn và tọa độ địa danh đang được biên soạn, đối chiếu.</p><div class="source-item"><strong>Bản đồ tham khảo</strong><p><a href="https://github.com/thanglequoc/vietnamese-provinces-database" target="_blank" rel="noopener noreferrer">Vietnamese Provinces Database</a> · Snapshot geojson_11Mar2026; đường biên giản lược để hiển thị. Nguồn gốc dữ liệu: sapnhap.bando.com.vn. Cần đối chiếu <a href="https://vnsdi.mae.gov.vn/bandohanhchinh/" target="_blank" rel="noopener noreferrer">bản đồ hành chính chính thức</a> trước khi nộp.</p><p>Mã phiên bản: ${escapeHTML(geo.source.revision.slice(0,12))}. Không sử dụng cho mục đích đo đạc hoặc địa chính.</p><p>Hình học tham khảo quần đảo Hoàng Sa và Trường Sa: Nguyễn Duy Liêm / <a href="https://github.com/nguyenduy1133/Free-GIS-Data" target="_blank" rel="noopener noreferrer">Free-GIS-Data</a>. Bản đồ không biểu diễn đường biên biển.</p></div><div class="source-item"><strong>Ảnh thực tế dùng tạm cho giao diện</strong><p>Ảnh được thu nhỏ và cắt khung hiển thị; giữ giấy phép của từng ảnh. Chưa phải hình minh họa AI.</p>${credits.map(c=>`<p><a href="${c.source}" target="_blank" rel="noopener noreferrer">${destinationById(c.id).name}: ${escapeHTML(c.author)} / Wikimedia Commons</a> · <a class="license" href="${c.licenseUrl}" target="_blank" rel="noopener noreferrer">${c.license}</a></p>`).join('')}</div><div class="source-item"><strong>Hình minh họa AI</strong><p>${Object.values(aiRegions).reduce((sum,region)=>sum+region.images.length,0)} ảnh được tạo bằng API Ban tổ chức. Bộ ảnh mở rộng tới các địa danh tuyển chọn tại Quảng Ninh và Lào Cai, bên cạnh khu vực Hạ Long và Sa Pa trên bản đồ. Các ảnh có nhãn minh họa, không phải ảnh tư liệu.</p></div><div class="source-item"><strong>Chatbot</strong><p>Chưa kết nối API chatbot. Không có câu trả lời AI giả lập.</p></div>`); }
function showSaved() { openInfo('Sổ tay của tôi',saved.length?`<p>Những miền đất bạn muốn tìm hiểu thêm. Danh sách lưu trên trình duyệt này.</p><div class="saved-list">${saved.map(id=>{const d=destinationById(id);return `<div class="saved-item"><img ${heroAttributes(d)}><a href="#/dia-phuong/${id}" data-close-info>${d.name}</a><button class="remove-saved" data-remove-saved="${id}" aria-label="Bỏ lưu ${d.name}">Bỏ lưu</button></div>`;}).join('')}</div>`:`<div class="empty-saved">${icon('bookmark')}<p>Sổ tay của bạn đang chờ những câu chuyện đầu tiên.</p><p>Mở trang một điểm đến rồi chọn “Lưu vào sổ tay”.</p><button class="primary-button" data-close-info>Bắt đầu khám phá ${icon('arrow')}</button></div>`); }
function notFound() { main.innerHTML=`<div class="error-box"><span class="eyebrow">NGOÀI PHẠM VI SỔ TAY</span><h2>Chưa có câu chuyện ở đây</h2><p>Sổ tay hiện có Hà Nội, Ninh Bình, Hạ Long và Sa Pa.</p><a class="primary-button" href="#/">Trở về bản đồ ${icon('arrow')}</a></div>`; }
function render() {
 if(!geo)return;
 const [path,query='']=(location.hash.slice(1)||'/').split('?');
 if(path==='/'||path===''){document.title='Atlas Việt — Mỗi miền đất, một câu chuyện';homeView();}
 else {const match=path.match(/^\/dia-phuong\/([a-z-]+)\/?$/);if(match){detailView(match[1],new URLSearchParams(query));const d=destinationById(match[1]);document.title=d?d.name+' — Atlas Việt':'Ngoài phạm vi — Atlas Việt';}else notFound();}
 $('.nav-explore').classList.toggle('active',path==='/');
}
document.addEventListener('click',event=>{
 const target=event.target.closest('button,a,[data-open],[data-province]');if(!target)return;
 if(target.dataset.open){openDestination(target.dataset.open);if(target.dataset.openPlace)selectLocalPlace(destinationById(target.dataset.open),target.dataset.openPlace);}
 if(target.dataset.province){const d=destinations.find(d=>d.province===Number(target.dataset.province));if(d)openDestination(d.id);else notify(target.dataset.name+' chưa nằm trong phạm vi sổ tay.');}
 if(target.dataset.aiImage)openImage(destinationById(target.dataset.aiDestination),target.dataset.aiImage);
 if(target.dataset.save)toggleSaved(target.dataset.save);
 if(target.dataset.tab){location.hash=`/dia-phuong/${target.dataset.destination}?tab=${target.dataset.tab}`;}
 if(target.hasAttribute('data-close-info'))infoDialog.close();
 if(target.hasAttribute('data-sources'))showSources();
 if(target.dataset.removeSaved){toggleSaved(target.dataset.removeSaved);showSaved();}
});
document.addEventListener('keydown',event=>{
 const target=event.target;
 if((event.key==='Enter'||event.key===' ')&&target.matches('g[role=button]')){event.preventDefault();target.dispatchEvent(new MouseEvent('click',{bubbles:true}));}
 if(target.matches('[role=tab]')&&['ArrowLeft','ArrowRight','Home','End'].includes(event.key)){
  event.preventDefault();const buttons=$$('[role=tab]');const index=buttons.indexOf(target);const next=event.key==='Home'?0:event.key==='End'?buttons.length-1:(index+(event.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length;buttons[next].click();setTimeout(()=>$$('[role=tab]')[next]?.focus(),0);
 }
});
dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});
infoDialog.addEventListener('click',event=>{if(event.target===infoDialog){const r=infoDialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)infoDialog.close();}});
$('#saved-nav').onclick=showSaved;
$('#sources-footer').onclick=showSources;
$('#about-nav').onclick=()=>openInfo('Mỗi miền đất, một câu chuyện',`<p>Atlas Việt là bản mẫu sổ tay điện tử Dư địa chí dành cho người muốn tìm hiểu địa lý, lịch sử và văn hóa qua bản đồ tương tác.</p><p><strong>Phạm vi:</strong> Hà Nội, Ninh Bình, khu vực Hạ Long và Sa Pa.</p><p>Phiên bản này hoàn thiện luồng khám phá. Hình minh họa AI đã có trong các bộ ảnh địa phương. Nội dung chi tiết và chatbot sử dụng API Ban tổ chức sẽ được bổ sung sau.</p><p>Thông tin được biên soạn cần có nguồn dẫn, mốc đối chiếu và sự tôn trọng văn hóa địa phương. Những mục chưa xác minh phải được đánh dấu rõ.</p><button class="secondary-button" data-sources>Xem nguồn dữ liệu ${icon('arrow')}</button>`);
$('#chat-toggle').onclick=()=>{const panel=$('#chat-panel');panel.hidden=!panel.hidden;$('#chat-toggle').setAttribute('aria-expanded',String(!panel.hidden));};
$('#chat-close').onclick=()=>{$('#chat-panel').hidden=true;$('#chat-toggle').setAttribute('aria-expanded','false');$('#chat-toggle').focus();};
$('#chat-destinations').innerHTML=destinations.map(d=>`<button data-open="${d.id}">${d.name} ↗</button>`).join('');
window.addEventListener('hashchange',render);
updateSavedCount();
try {
 const responses=await Promise.all([fetch('assets/vietnam-provinces.geojson'),fetch('assets/credits.json')]);
 if(responses.some(r=>!r.ok))throw new Error('Không thể tải dữ liệu bản đồ.');
 [geo,credits]=await Promise.all(responses.map(r=>r.json()));
 try { const media=await fetch('assets/ai-images.json',{cache:'no-store'});if(media.ok)aiRegions=(await media.json()).regions || {}; } catch { /* Preserve the map and attributed photos when the optional media index is unavailable. */ }
 render();
}catch(error){main.innerHTML=`<div class="error-box"><h2>Bản đồ chưa tải được</h2><p>${escapeHTML(error.message)}</p><p>Hãy mở website qua máy chủ HTTP và tải lại trang.</p><button class="primary-button" onclick="location.reload()">Thử lại</button></div>`;}
