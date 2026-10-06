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
 {id:'quang-ninh',photoId:'ha-long',name:'Quảng Ninh',province:10,provinceName:'Quảng Ninh',number:'03',tag:'Kỳ quan giữa biển trời',subtitle:'Một thế giới núi đá, sóng nước và làng chài.',coords:[107.083,20.95],callout:[88,14],
  description:'Khám phá Quảng Ninh qua cảnh quan Vịnh Hạ Long, không gian Yên Tử, đảo Cô Tô và những câu chuyện về đời sống địa phương.',
  headline:'Nơi núi đá gặp những con sóng',geography:'Phạm vi sổ tay là thành phố Quảng Ninh theo mốc hành chính từ 01/09/2026. Bản đồ hiển thị toàn tỉnh; nội dung bước đầu giới thiệu một số địa danh tiêu biểu, từ Hạ Long đến Yên Tử và Cô Tô. Các mục khác sẽ được bổ sung sau.',
  culture:'Đời sống ven biển, văn hóa làng chài và ẩm thực hải sản là những chủ đề sẽ được biên soạn. Nội dung về chả mực và nghề biển sẽ được bổ sung cùng nguồn tham khảo.',topics:['Cảnh quan vịnh','Không gian hang động','Văn hóa cộng đồng ven biển','Chả mực và hải sản'],
  history:[['Đất & nước','Câu chuyện hình thành cảnh quan','Phần này sẽ bổ sung thông tin địa chất đã được kiểm chứng, với minh họa và nguồn dẫn.'],['Con người & di sản','Đời sống bên bờ vịnh','Bổ sung tư liệu về cộng đồng, hoạt động bảo tồn và văn hóa địa phương.']],
  source:'https://vietnam.travel/places-to-go/northern-vietnam/ha-long',tour:sourceTravel,
  places:[['vinh-ha-long','Vịnh Hạ Long',107.107,20.875,'Cảnh quan','Khám phá không gian biển và những đảo đá vôi qua bản đồ.'],['yen-tu','Yên Tử',106.717,21.157,'Văn hóa – Lịch sử','Không gian để tìm hiểu cảnh quan, di tích và văn hóa Phật giáo địa phương.'],['co-to','Đảo Cô Tô',107.765,20.971,'Đảo & biển','Một điểm đến để khám phá cảnh quan đảo và đời sống ven biển.'],['bao-tang','Bảo tàng Quảng Ninh',107.101,20.95,'Văn hóa','Nơi bắt đầu tìm hiểu thiên nhiên, lịch sử và con người địa phương.']]},
 {id:'lao-cai',photoId:'sa-pa',name:'Lào Cai',province:4,provinceName:'Lào Cai',number:'04',tag:'Miền mây & sắc bản',subtitle:'Theo triền núi, gặp những câu chuyện bản làng.',coords:[103.844,22.336],callout:[-72,-18],
  description:'Khám phá Lào Cai qua cảnh quan Sa Pa, Bắc Hà, Mù Cang Chải và những nét văn hóa đa dạng của cộng đồng địa phương.',
  headline:'Một hành trình giữa núi, mây và bản làng',geography:'Phạm vi sổ tay là tỉnh Lào Cai theo ranh giới trên bản đồ 34 tỉnh/thành phố. Nội dung bước đầu giới thiệu Sa Pa, Bắc Hà và Mù Cang Chải; các địa danh và chủ đề khác sẽ được bổ sung sau.',
  culture:'Các câu chuyện văn hóa cần được thể hiện theo từng cộng đồng và có nguồn rõ ràng. Trang này sẽ bổ sung nội dung về nghề dệt, sinh hoạt bản làng và ẩm thực, tôn trọng sự đa dạng địa phương.',topics:['Cảnh quan núi và thung lũng','Ruộng bậc thang','Nghề thủ công địa phương','Văn hóa các cộng đồng'],
  history:[['Bản làng','Những câu chuyện địa phương','Bổ sung tư liệu về cộng đồng và các địa danh; phân biệt rõ lịch sử được ghi nhận với truyền kể.'],['Lào Cai hôm nay','Cảnh quan và đời sống','Bổ sung thông tin về bảo tồn văn hóa, thiên nhiên và sự thay đổi của không gian địa phương.']],
  source:'https://vietnam.travel/places-to-go/northern-vietnam/sapa',tour:null,
  places:[['fansipan','Fansipan',103.775,22.303,'Núi cao','Một địa danh gắn với cảnh quan núi Hoàng Liên Sơn.'],['bac-ha','Bắc Hà',104.291,22.539,'Văn hóa','Khám phá không gian chợ và đời sống của các cộng đồng địa phương.'],['muong-hoa','Thung lũng Mường Hoa',103.878,22.298,'Thung lũng','Không gian cảnh quan và bản làng để tìm hiểu vùng Sa Pa.'],['mu-cang-chai','Mù Cang Chải',104.089,21.851,'Ruộng bậc thang','Một điểm khám phá cảnh quan ruộng bậc thang và đời sống vùng cao.']]}
];
const tabs = [['tong-quan','Địa lý – Tổng quan'],['dia-danh','Địa danh'],['du-lich','Du lịch online'],['lich-su','Lịch sử'],['van-hoa','Văn hóa – Ẩm thực'],['nguon','Nguồn tham khảo']];
// Scene order matches AirPano tour_hi.xml; startscene uses a zero-based index.
const onlineTours = {
 'ha-noi':{slug:'hanoi-vietnam',title:'Hà Nội trong góc nhìn 360°',scope:'Hồ Hoàn Kiếm và những góc nhìn trên cao của trung tâm Hà Nội.',scenes:['Hồ Hoàn Kiếm','Tháp Rùa trên hồ Hoàn Kiếm','Hà Nội từ trên cao','Hà Nội lúc chiều tối','Hà Nội về đêm']},
 'quang-ninh':{slug:'halong-bay-vietnam',title:'Một hành trình quanh Vịnh Hạ Long',scope:'Tour giới thiệu khu vực Vịnh Hạ Long, thuộc Quảng Ninh.',scenes:['Bình minh trên Vịnh Hạ Long','Những đảo đá trên vịnh','Đảo Cống Đỏ từ độ cao 120 m','Đảo Cống Đỏ từ độ cao 70 m','Bên trong hang động','Làng chài Cống Đầm từ độ cao 100 m','Làng chài Cống Đầm từ độ cao 30 m','Cảng Hạ Long','Quanh đảo Cống Đỏ']}
};
let tourLoadTimer;
const legacyIds = {'ha-long':'quang-ninh','sa-pa':'lao-cai'};
const photoId = d => d.photoId || d.id;
const scopeLabel = 'Ninh Bình, Hà Nội, Quảng Ninh và Lào Cai';
const destinationById = id => destinations.find(d => d.id === id);
let geo, credits = [], activeLocalPlace, previousDestination, toastTimer;
let saved = [];
try { const value = JSON.parse(localStorage.getItem('atlas-viet-saved') || '[]'); if (Array.isArray(value)) saved = [...new Set(value.map(id => legacyIds[id] || id).filter(id => destinationById(id)))]; localStorage.setItem('atlas-viet-saved',JSON.stringify(saved)); } catch {}
const main = $('#main');
const dialog = $('#destination-dialog');
const infoDialog = $('#info-dialog');
function notify(message) { const toast=$('#toast'); toast.textContent=message; toast.hidden=false; clearTimeout(toastTimer); toastTimer=setTimeout(()=>toast.hidden=true,4200); }
function updateSavedCount() { $('#saved-count').textContent=saved.length; }
function toggleSaved(id) {
 const had=saved.includes(id); saved=had?saved.filter(v=>v!==id):[...saved,id];
 try { localStorage.setItem('atlas-viet-saved',JSON.stringify(saved)); } catch { notify('Không thể lưu lâu dài trên trình duyệt này. Sổ tay vẫn dùng được trong phiên hiện tại.'); }
 updateSavedCount(); updateSaveButton(id);
 notify(had?'Đã bỏ địa phương khỏi sổ tay.':'Đã lưu địa phương vào sổ tay của bạn.');
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
function destinationCard(d) { return `<button class="destination-card" data-open="${d.id}" data-card="${d.id}" aria-label="Khám phá ${d.name}"><img src="assets/${photoId(d)}.jpg" alt="${photoDescription(photoId(d))}" width="76" height="58"><span class="card-copy"><strong>${d.name}</strong><small>${d.tag}</small></span><span class="card-arrow">${icon('arrow')}</span></button>`; }
function photoDescription(id) { return {'ninh-binh':'Cảnh quan Tràng An với núi đá và thuyền trên sông','ha-noi':'Tháp Rùa giữa Hồ Hoàn Kiếm','ha-long':'Toàn cảnh vịnh với những đảo đá','sa-pa':'Ruộng bậc thang ở Sa Pa'}[id]; }
function homeView() {
 previousDestination=null;
 main.innerHTML=`<div class="atlas-layout"><section class="intro" aria-labelledby="home-title"><span class="eyebrow">ĐI QUA ĐỊA DANH · CHẠM VÀO TRI THỨC</span><h1 id="home-title">Mỗi miền đất,<br> một <em>câu chuyện.</em></h1><p class="intro-description">Mở bản đồ, chọn một miền đất. Cùng khám phá địa lý, lịch sử và những nét văn hóa làm nên bản sắc Việt Nam.</p><div class="intro-rule">Bốn tỉnh/thành phố, một hành trình</div><div class="destination-list">${destinations.map(destinationCard).join('')}</div><p class="list-caption">${icon('pin')} Chọn trên bản đồ hoặc trong danh sách để bắt đầu</p></section><section class="map-panel" aria-label="Bản đồ khám phá Việt Nam"><div class="map-topbar"><span class="map-title">${icon('map')} BẢN ĐỒ VIỆT NAM</span><button id="focus-north">${icon('focus')} Khám phá 4 tỉnh/thành</button></div><div class="map-viewport"><svg id="country-map" class="country-svg" viewBox="0 0 820 820" aria-label="Bản đồ 34 tỉnh thành Việt Nam" role="group">${provincePaths()}<text class="map-region-label" x="210" y="196">MIỀN BẮC</text><text class="map-region-label" x="337" y="423">MIỀN TRUNG</text><text class="map-region-label" x="215" y="710">MIỀN NAM</text><text class="sea-label" x="450" y="490" transform="rotate(-15 450 490)">Biển Đông</text>${islandLabels()}${destinations.map(countryMarker).join('')}</svg></div><div class="compass-decoration">BẮC<svg viewBox="0 0 32 48" aria-hidden="true"><path d="m16 5 7 26-7-7-7 7Z" fill="#667d60"/><path d="m16 5 7 26-7-7Z" fill="#c79a45"/><path d="M16 26v16" stroke="#667d60"/></svg></div><div class="map-controls" aria-label="Điều khiển bản đồ"><button data-zoom="in" aria-label="Phóng to">+</button><button data-zoom="out" aria-label="Thu nhỏ">−</button><button data-zoom="reset" aria-label="Hiện toàn bộ bản đồ">${icon('focus')}</button></div><div class="map-legend"><span><i class="legend-dot"></i> Có trong sổ tay</span><span><i class="legend-dot muted"></i> Chưa có nội dung</span></div><button class="map-attribution" data-sources>Ranh giới tham khảo · Xem nguồn ↗</button><div id="map-tooltip" class="map-tooltip" hidden></div></section></div><div class="scope-strip">${icon('info')}<span><strong>Phạm vi sổ tay:</strong> ${scopeLabel}.</span><span class="scope-divider"></span><span class="boundary-note">Nội dung ngắn dành cho bản mẫu · Sẽ tiếp tục bổ sung</span></div>`;
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
 const province=geo.features.find(f=>f.properties.atlasId===d.province);
 const [x,y,w,h]=boundsFor([province],d.places.map(p=>[p[2],p[3]]));
 return [x-w*.18,y-h*.18,w*1.36,h*1.36];
}
function localMap(d) {
 const box=localViewBox(d),scale=Math.max(box[2]/(innerWidth<760?310:540),box[3]/(innerWidth<760?290:440));const dot=5*scale;const font=11*scale;
 const offsets={'ha-noi':[[20,28],[-22,22],[-20,-20],[24,-20]],'ninh-binh':[[-38,3],[25,32],[39,-11],[-30,-28]],'quang-ninh':[[25,30],[23,-20],[25,-10],[18,8]],'lao-cai':[[18,-15],[-22,-5],[20,18],[23,15]]};
 return `<svg viewBox="${box.join(' ')}" role="group" aria-label="Bản đồ các địa danh tại ${d.name}">${provincePaths(true,d.province)}${d.places.map((p,i)=>{const [x,y]=project([p[2],p[3]]),[dx,dy]=offsets[d.id][i]; const distributed=true; const side=d.id==="ha-noi"?[true,false,false,true][i]:d.id==="quang-ninh"?[false,false,true,true][i]:[false,true,true,false][i]; const targetX=distributed?box[0]+box[2]*(side?.92:.08):x+dx*scale; const targetY=["quang-ninh","lao-cai"].includes(d.id)?Math.max(box[1]+box[3]*.12,Math.min(box[1]+box[3]*.88,y+dy*scale)):box[1]+box[3]*[.66,.82,.4,.23][i]; const anchor=distributed?(side?"end":"start"):(dx<0?"end":"start");return `<g class="local-marker${i===0?' is-active':''}" data-place="${p[0]}" role="button" tabindex="0" aria-label="${p[1]}"><line x1="${x}" y1="${y}" x2="${targetX}" y2="${targetY-3*scale}" stroke="#748e63" stroke-width="${scale*.6}"/><circle cx="${x}" cy="${y}" r="${dot}"/><text x="${targetX}" y="${targetY}" style="font-size:${font}px;stroke-width:${4*scale}px" text-anchor="${anchor}">${p[1]}</text></g>`;}).join('')}</svg>`;
}
function openDestination(id) {
 const d=destinationById(id);if(!d)return;
 activeLocalPlace=d.places[0][0];
 $('#dialog-content').innerHTML=`<div class="dialog-header"><div><span class="eyebrow">${d.provinceName} · BẢN ĐỒ KHÁM PHÁ</span><h2 id="destination-title">${d.name} <span class="muted">/</span> ${d.tag}</h2></div><button class="icon-button" data-close-destination aria-label="Đóng bản đồ địa phương">×</button></div><div class="dialog-grid"><div class="local-map-panel">${localMap(d)}<div class="local-map-caption">Vị trí minh họa gần đúng · Chọn dấu mốc để khám phá · Đang đối chiếu tọa độ</div></div><div class="dialog-sidebar"><span class="eyebrow">BẮT ĐẦU HÀNH TRÌNH</span><p>${d.description}</p><div class="local-place-list">${d.places.map((p,i)=>`<button class="place-list-button${i===0?' is-active':''}" data-place="${p[0]}"><span class="number">0${i+1}</span><strong>${p[1]}</strong>${icon('chevron')}</button>`).join('')}</div><div class="selected-place" id="selected-place"><span class="eyebrow">${d.places[0][4]}</span><h3>${d.places[0][1]}</h3><p>${d.places[0][5]}</p></div><a id="detail-link" class="primary-button" href="#/dia-phuong/${d.id}?tab=dia-danh&diem=${activeLocalPlace}">Tìm hiểu chi tiết ${icon('arrow')}</a></div></div>`;
 $('#dialog-content').dataset.destination=id;
 if(!dialog.open)dialog.showModal();
 $$('[data-place]',dialog).forEach(el=>el.addEventListener('click',()=>selectLocalPlace(d,el.dataset.place)));
 $('[data-close-destination]',dialog).onclick=()=>dialog.close();
 $('#detail-link').onclick=()=>dialog.close();
}
function selectLocalPlace(d,id) {
 const p=d.places.find(p=>p[0]===id);if(!p)return;activeLocalPlace=id;
 $$('[data-place]',dialog).forEach(el=>el.classList.toggle('is-active',el.dataset.place===id));
 $('#selected-place').innerHTML=`<span class="eyebrow">${p[4]}</span><h3>${p[1]}</h3><p>${p[5]}</p>`;
 $('#detail-link').href=`#/dia-phuong/${d.id}?tab=dia-danh&diem=${id}`;
}
function creditFor(d) { return credits.find(c=>c.id===photoId(d)); }
function photoCredit(d) { const c=creditFor(d);return c?`Ảnh thực tế dùng tạm · <a href="${c.source}" target="_blank" rel="noopener noreferrer">${escapeHTML(c.author)} / Wikimedia Commons</a> · <a href="${c.licenseUrl}" target="_blank" rel="noopener noreferrer">${c.license}</a> · Thu nhỏ, cắt khung hiển thị`:'Ảnh giao diện tạm thời · Chưa phải hình minh họa AI'; }
function detailView(id,params) {
 const d=destinationById(id);if(!d){notFound();return;}
 const tab=tabs.some(([t])=>t===params.get('tab'))?params.get('tab'):'tong-quan';
 const changed=previousDestination!==id;previousDestination=id;
 main.innerHTML=`<div class="detail-shell"><div class="breadcrumb"><a href="#/">${icon('back')} Bản đồ Việt Nam</a><span>/</span><span>${d.name}</span></div><section class="detail-hero" aria-labelledby="detail-title"><img src="assets/${photoId(d)}.jpg" alt="${photoDescription(photoId(d))}"><div class="detail-hero-content"><span class="eyebrow">TỈNH/THÀNH PHỐ ${d.number} · ${d.tag}</span><h1 id="detail-title">${d.name}</h1><p>${d.subtitle} ${d.description}</p></div></section><p class="photo-caption">${photoCredit(d)}</p><div class="detail-actions"><p>${icon('pin')} Phạm vi: ${['ha-noi','quang-ninh'].includes(d.id)?'thành phố':'tỉnh'} ${d.name}<br>Nội dung bản mẫu · Đang biên soạn</p><button class="secondary-button" data-save="${d.id}" aria-pressed="${saved.includes(d.id)}">${icon(saved.includes(d.id)?'check':'bookmark')}${saved.includes(d.id)?'Đã lưu vào sổ tay':'Lưu vào sổ tay'}</button></div><div class="detail-tabs" role="tablist" aria-label="Nội dung sổ tay ${d.name}">${tabs.map(([key,label])=>`<button role="tab" id="tab-${key}" aria-selected="${key===tab}" aria-controls="tab-content" tabindex="${key===tab?0:-1}" data-tab="${key}" data-destination="${d.id}">${label}</button>`).join('')}</div><section class="tab-content" id="tab-content" role="tabpanel" aria-labelledby="tab-${tab}" tabindex="0">${tabView(d,tab)}</section></div>`;
 if(changed)window.scrollTo({top:0,behavior:'instant'});
 if(params.get('diem')){const p=$(`[data-place-card="${params.get('diem')}"]`);if(p){p.style.borderColor='#8ea387';p.style.background='#eef0e5';}}
}
function tabView(d,tab) {
 if(tab==='du-lich')return onlineTourView(d);
 if(tab==='dia-danh')return `<div class="section-heading"><h2>Những nơi để bắt đầu</h2><span>04 địa danh · Đang biên soạn</span></div><div class="place-grid">${d.places.map((p,i)=>`<article class="place-card" data-place-card="${p[0]}"><span class="place-index">0${i+1}</span><span class="eyebrow">${p[4]}</span><h3>${p[1]}</h3><p>${p[5]} Nội dung chi tiết sẽ được bổ sung cùng nguồn tham khảo.</p><span class="place-meta">${icon('pin')} Tọa độ tham khảo · Chưa đối chiếu</span><button class="secondary-button" data-open="${d.id}" data-open-place="${p[0]}">${icon('map')} Xem trên bản đồ</button><button class="secondary-button" data-ask-atlas="${p[1]}" data-chat-province="${d.id}">✧ Hỏi Atlas về địa danh này</button></article>`).join('')}</div><p style="margin-top:22px"><a class="secondary-button" href="#/dia-phuong/${d.id}?tab=du-lich">Khám phá Du lịch online ${icon('arrow')}</a></p>`;
 if(tab==='lich-su')return `<div class="section-heading"><h2>Dấu xưa, chuyện nay</h2><span>Khung nội dung dự kiến</span></div><div class="timeline">${d.history.map(h=>`<article class="timeline-item"><span class="eyebrow">${h[0]}</span><h3>${h[1]}</h3><p>${h[2]}</p></article>`).join('')}</div><span class="draft-badge">Mốc thời gian đang được đối chiếu tài liệu</span>`;
 if(tab==='van-hoa')return `<div class="editorial-grid"><div class="editorial-copy"><span class="eyebrow">VĂN HÓA · CON NGƯỜI · HƯƠNG VỊ</span><h2>Bản sắc trong những điều gần gũi</h2><p>${d.culture}</p><span class="draft-badge">Nội dung đang biên soạn</span></div><aside class="editorial-aside"><h3>Chủ đề sẽ khám phá</h3><ul>${d.topics.map(t=>`<li>${t}</li>`).join('')}</ul></aside></div>`;
 if(tab==='nguon')return `<div class="section-heading"><h2>Nguồn & sự minh bạch</h2><span>Cập nhật bản mẫu: 06/10/2026</span></div><p class="muted">Các liên kết dưới đây là nguồn để tiếp tục biên soạn. Bản mẫu chưa xác minh từng nhận định và tọa độ; chưa dùng cho câu trả lời AI.</p><div class="source-item"><strong>Thông tin điểm đến — Vietnam.travel</strong><p><a href="${d.source}" target="_blank" rel="noopener noreferrer">Trang giới thiệu ${d.photoId==='ha-long'?'Hạ Long (Quảng Ninh)':d.photoId==='sa-pa'?'Sa Pa (Lào Cai)':d.name} ↗</a> · Cổng thông tin du lịch quốc gia</p></div>${onlineTours[d.id]?`<div class="source-item"><strong>Tour du lịch online — AirPano</strong><p><a href="https://www.airpano.com/360photo/${onlineTours[d.id].slug}/" target="_blank" rel="noopener noreferrer">${onlineTours[d.id].title} ↗</a> · Courtesy of www.AirPano.com</p><p>Tour được nhúng từ AirPano và cần Internet. Danh sách cảnh dựa trên cấu hình nguồn; các tên cảnh được chuyển sang tiếng Việt.</p></div>`:''}<div class="source-item"><strong>Ảnh thực tế dùng tạm</strong><p>${photoCredit(d)}</p><p>Chưa phải ảnh do AI tạo; sẽ bổ sung minh họa theo yêu cầu của đề thi.</p></div><div class="source-item"><strong>Dữ liệu ranh giới bản đồ</strong><p><a href="https://github.com/thanglequoc/vietnamese-provinces-database" target="_blank" rel="noopener noreferrer">Vietnamese Provinces Database ↗</a> · Bản chụp GIS tháng 3/2026, có giản lược đường biên để hiển thị. Đây là nguồn cộng đồng, cần đối chiếu bản đồ chính thức trước khi nộp.</p></div>`;
 return `<div class="editorial-grid"><div class="editorial-copy"><span class="eyebrow">ĐỊA LÝ & TỔNG QUAN</span><h2>${d.headline}</h2><p>${d.geography}</p><p>${d.description}</p><button class="secondary-button" data-open="${d.id}">${icon('map')} Mở bản đồ địa phương</button></div><aside class="editorial-aside"><span class="eyebrow">TRONG SỔ TAY NÀY</span><h3>Bắt đầu từ bốn địa danh</h3><ul>${d.places.map(p=>`<li>${p[1]}</li>`).join('')}</ul><span class="draft-badge">Nội dung đang biên soạn</span></aside></div>`;
}
function onlineTourView(d) {
 const tour=onlineTours[d.id];
 if(!tour)return `<div class="tour-empty"><span class="eyebrow">DU LỊCH ONLINE · 360°</span><h2>${d.id==='ninh-binh'?'Một hành trình đang được chuẩn bị':'Hẹn một chuyến khám phá mới'}</h2><p>${d.id==='ninh-binh'?'Tour 360° Ninh Bình đang được bổ sung. Bạn có thể tiếp tục khám phá các địa danh trên bản đồ trong lúc chờ.':'Chưa có tour 360° cho Lào Cai trong sổ tay này. Những hành trình mới sẽ được bổ sung khi có dữ liệu phù hợp.'}</p><span class="draft-badge">${d.id==='ninh-binh'?'Dữ liệu 360° đang được bổ sung':'Chưa có tour 360°'}</span><a class="secondary-button" href="#/dia-phuong/${d.id}?tab=dia-danh">${icon('map')} Khám phá địa danh</a></div>`;
 return `<div class="tour-section" data-tour="${d.id}" data-tour-scene="0"><div class="section-heading"><h2>${tour.title}</h2><span>${String(tour.scenes.length).padStart(2,'0')} cảnh · AirPano</span></div><p class="tour-intro">${tour.scope} Chọn một cảnh khởi đầu, rồi kéo để nhìn quanh và khám phá tiếp bên trong tour.</p><div class="tour-stage" id="tour-stage"><div class="tour-poster" id="tour-poster"><img src="assets/${photoId(d)}.jpg" alt="" class="tour-cover"><div class="tour-poster-content"><span class="tour-label">MỞ MỘT GÓC NHÌN MỚI</span><h3 id="tour-start-title">${tour.scenes[0]}</h3><p>Một chuyến đi ngay trên màn hình của bạn.</p><button class="primary-button" data-tour-start>${icon('arrow')} Bắt đầu khám phá</button><small>Cần kết nối Internet · Tour có âm thanh</small></div></div></div><div class="tour-toolbar"><p id="tour-status" role="status" aria-live="polite">Tour sẽ được tải khi bạn chọn “Bắt đầu khám phá”.</p><div id="tour-controls" hidden><button class="secondary-button" data-tour-retry>Thử lại</button><button class="secondary-button" data-tour-fullscreen>${icon('focus')} Toàn màn hình</button><button class="secondary-button" data-tour-stop>Dừng tour</button></div></div><div class="tour-scenes-heading"><h3>Chọn cảnh khởi đầu</h3><span>Bạn có thể chuyển cảnh tiếp trong tour.</span></div><div class="tour-scenes" aria-label="Cảnh khởi đầu của tour">${tour.scenes.map((title,index)=>`<button class="tour-scene" data-tour-select="${index}" aria-pressed="${index===0}"><span class="tour-scene-number">${String(index+1).padStart(2,'0')}</span><span>${title}</span>${icon('arrow')}</button>`).join('')}</div><div class="tour-credit"><p>Courtesy of <a href="https://www.airpano.com/" target="_blank" rel="noopener noreferrer">www.AirPano.com</a> · Trải nghiệm 360° do AirPano cung cấp.</p><a id="tour-source" href="https://www.airpano.com/360photo/${tour.slug}/?startscene=0" target="_blank" rel="noopener noreferrer">Mở tour trên AirPano ${icon('external')}</a></div></div>`;
}
function startOnlineTour() {
 const section=$('[data-tour]');if(!section)return;
 const tour=onlineTours[section.dataset.tour];if(!tour)return;
 clearTimeout(tourLoadTimer);
 $('#tour-frame')?.remove();
 const frame=document.createElement('iframe');
 frame.id='tour-frame';frame.title=`Tour 360° AirPano — ${tour.scenes[Number(section.dataset.tourScene)]}`;
 frame.allow='fullscreen; autoplay; gyroscope; accelerometer';frame.allowFullscreen=true;
 frame.referrerPolicy='strict-origin-when-cross-origin';
 const status=$('#tour-status');
 const fallback=()=>{if(frame.isConnected)status.textContent='Tour có thể đang tải chậm. Bạn có thể thử lại hoặc mở trực tiếp trên AirPano.';};
 frame.addEventListener('load',()=>{clearTimeout(tourLoadTimer);if(frame.isConnected)status.textContent='Khung AirPano đã mở. Nếu chưa thấy cảnh 360°, hãy thử lại hoặc mở tour trên AirPano.';});
 frame.addEventListener('error',()=>{clearTimeout(tourLoadTimer);fallback();});
 frame.src=`https://www.airpano.com/embed.php?3D=${tour.slug}&startscene=${section.dataset.tourScene}`;
 $('#tour-poster').hidden=true;$('#tour-controls').hidden=false;
 status.textContent='Đang mở tour AirPano…';$('#tour-stage').append(frame);
 tourLoadTimer=setTimeout(fallback,15000);
}
function selectTourScene(index) {
 const section=$('[data-tour]');if(!section)return;
 const tour=onlineTours[section.dataset.tour];if(!Number.isInteger(index)||!tour.scenes[index])return;
 section.dataset.tourScene=String(index);
 $$('[data-tour-select]',section).forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.tourSelect)===index)));
 $('#tour-start-title').textContent=tour.scenes[index];
 $('#tour-source').href=`https://www.airpano.com/360photo/${tour.slug}/?startscene=${index}`;
 if($('#tour-frame'))startOnlineTour();
}
function stopOnlineTour() {
 clearTimeout(tourLoadTimer);$('#tour-frame')?.remove();
 $('#tour-poster').hidden=false;$('#tour-controls').hidden=true;
 $('#tour-status').textContent='Tour đã dừng. Bạn có thể chọn cảnh khác và bắt đầu lại.';
 $('[data-tour-start]').focus();
}
function openInfo(title,content) { $('#info-content').innerHTML=`<span class="eyebrow">ATLAS VIỆT · SỔ TAY ĐIỆN TỬ</span><h2 id="info-title">${title}</h2>${content}`;if(!infoDialog.open)infoDialog.showModal(); }
function showSources() { openInfo('Nguồn dữ liệu & ghi chú',`<p>Bản mẫu giới thiệu bốn tỉnh/thành phố: ${scopeLabel}. Nội dung ngắn và tọa độ địa danh đang được biên soạn, đối chiếu.</p><div class="source-item"><strong>Bản đồ tham khảo</strong><p><a href="https://github.com/thanglequoc/vietnamese-provinces-database" target="_blank" rel="noopener noreferrer">Vietnamese Provinces Database</a> · Snapshot geojson_11Mar2026; đường biên giản lược để hiển thị. Nguồn gốc dữ liệu: sapnhap.bando.com.vn. Cần đối chiếu <a href="https://vnsdi.mae.gov.vn/bandohanhchinh/" target="_blank" rel="noopener noreferrer">bản đồ hành chính chính thức</a> trước khi nộp.</p><p>Mã phiên bản: ${escapeHTML(geo.source.revision.slice(0,12))}. Không sử dụng cho mục đích đo đạc hoặc địa chính.</p><p>Hình học tham khảo quần đảo Hoàng Sa và Trường Sa: Nguyễn Duy Liêm / <a href="https://github.com/nguyenduy1133/Free-GIS-Data" target="_blank" rel="noopener noreferrer">Free-GIS-Data</a>. Bản đồ không biểu diễn đường biên biển.</p></div><div class="source-item"><strong>Ảnh thực tế dùng tạm cho giao diện</strong><p>Ảnh được thu nhỏ và cắt khung hiển thị; giữ giấy phép của từng ảnh. Chưa phải hình minh họa AI.</p>${credits.map(c=>`<p><a href="${c.source}" target="_blank" rel="noopener noreferrer">${destinationById(legacyIds[c.id] || c.id).name}: ${escapeHTML(c.author)} / Wikimedia Commons</a> · <a class="license" href="${c.licenseUrl}" target="_blank" rel="noopener noreferrer">${c.license}</a></p>`).join('')}</div><div class="source-item"><strong>Chatbot và hình minh họa AI</strong><p>Chatbot RAG đã kết nối API BTC và kho tư liệu bốn địa phương, kèm dẫn nguồn. Hình minh họa AI sẽ được bổ sung sau.</p></div>`); }
function showSaved() { openInfo('Sổ tay của tôi',saved.length?`<p>Những miền đất bạn muốn tìm hiểu thêm. Danh sách lưu trên trình duyệt này.</p><div class="saved-list">${saved.map(id=>{const d=destinationById(id);return `<div class="saved-item"><img src="assets/${photoId(d)}.jpg" alt=""><a href="#/dia-phuong/${id}" data-close-info>${d.name}</a><button class="remove-saved" data-remove-saved="${id}" aria-label="Bỏ lưu ${d.name}">Bỏ lưu</button></div>`;}).join('')}</div>`:`<div class="empty-saved">${icon('bookmark')}<p>Sổ tay của bạn đang chờ những câu chuyện đầu tiên.</p><p>Mở trang một tỉnh/thành phố rồi chọn “Lưu vào sổ tay”.</p><button class="primary-button" data-close-info>Bắt đầu khám phá ${icon('arrow')}</button></div>`); }
function notFound() { main.innerHTML=`<div class="error-box"><span class="eyebrow">NGOÀI PHẠM VI SỔ TAY</span><h2>Chưa có câu chuyện ở đây</h2><p>Sổ tay hiện có ${scopeLabel}.</p><a class="primary-button" href="#/">Trở về bản đồ ${icon('arrow')}</a></div>`; }
function render() {
 if(!geo)return;
 clearTimeout(tourLoadTimer);
 const [path,query='']=(location.hash.slice(1)||'/').split('?');
 if(path==='/'||path===''){document.title='Atlas Việt — Mỗi miền đất, một câu chuyện';homeView();}
 else {const match=path.match(/^\/dia-phuong\/([a-z-]+)\/?$/);if(match){const canonical=legacyIds[match[1]];if(canonical){location.replace('#/dia-phuong/'+canonical+(query?'?'+query:''));return;}detailView(match[1],new URLSearchParams(query));const d=destinationById(match[1]);document.title=d?d.name+' — Atlas Việt':'Ngoài phạm vi — Atlas Việt';}else notFound();}
 $('.nav-explore').classList.toggle('active',path==='/');
}
document.addEventListener('click',event=>{
 const target=event.target.closest('button,a,[data-open],[data-province]');if(!target)return;
 if(target.dataset.open){openDestination(target.dataset.open);if(target.dataset.openPlace)selectLocalPlace(destinationById(target.dataset.open),target.dataset.openPlace);}
 if(target.dataset.province){const d=destinations.find(d=>d.province===Number(target.dataset.province));if(d)openDestination(d.id);else notify(target.dataset.name+' chưa nằm trong phạm vi sổ tay.');}
 if(target.dataset.save)toggleSaved(target.dataset.save);
 if(target.dataset.tab){location.hash=`/dia-phuong/${target.dataset.destination}?tab=${target.dataset.tab}`;}
 if(target.hasAttribute('data-tour-start')||target.hasAttribute('data-tour-retry'))startOnlineTour();
 if(target.hasAttribute('data-tour-select'))selectTourScene(Number(target.dataset.tourSelect));
 if(target.hasAttribute('data-tour-stop'))stopOnlineTour();
 if(target.hasAttribute('data-tour-fullscreen')){const stage=$('#tour-stage');if(stage?.requestFullscreen)stage.requestFullscreen().catch(()=>notify('Không thể mở toàn màn hình. Bạn vẫn có thể xem tour trong khung hiện tại.'));else notify('Trình duyệt này chưa hỗ trợ toàn màn hình.');}
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
$('#about-nav').onclick=()=>openInfo('Mỗi miền đất, một câu chuyện',`<p>Atlas Việt là bản mẫu sổ tay điện tử Dư địa chí dành cho người muốn tìm hiểu địa lý, lịch sử và văn hóa qua bản đồ tương tác.</p><p><strong>Phạm vi:</strong> ${scopeLabel}.</p><p>Phiên bản này hoàn thiện luồng khám phá. Chatbot RAG sử dụng API Ban tổ chức để tìm tư liệu và trả lời có nguồn. Nội dung trang chi tiết và hình minh họa AI sẽ tiếp tục được bổ sung.</p><p>Thông tin được biên soạn cần có nguồn dẫn, mốc đối chiếu và sự tôn trọng văn hóa địa phương. Những mục chưa xác minh phải được đánh dấu rõ.</p><button class="secondary-button" data-sources>Xem nguồn dữ liệu ${icon('arrow')}</button>`);
$('#chat-toggle').onclick=()=>{const panel=$('#chat-panel');panel.hidden=!panel.hidden;$('#chat-toggle').setAttribute('aria-expanded',String(!panel.hidden));};
$('#chat-close').onclick=()=>{$('#chat-panel').hidden=true;$('#chat-toggle').setAttribute('aria-expanded','false');$('#chat-toggle').focus();};

window.addEventListener('hashchange',render);
updateSavedCount();
try {
 const responses=await Promise.all([fetch('assets/vietnam-provinces.geojson'),fetch('assets/credits.json')]);
 if(responses.some(r=>!r.ok))throw new Error('Không thể tải dữ liệu bản đồ.');
 [geo,credits]=await Promise.all(responses.map(r=>r.json()));render();
}catch(error){main.innerHTML=`<div class="error-box"><h2>Bản đồ chưa tải được</h2><p>${escapeHTML(error.message)}</p><p>Hãy mở website qua máy chủ HTTP và tải lại trang.</p><button class="primary-button" onclick="location.reload()">Thử lại</button></div>`;}
