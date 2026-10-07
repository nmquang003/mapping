import { installMotion, dismissDialog } from './motion.js';
import { createLocalTour } from './local-tour.js';
import { narrationView, createNarration } from './tour-narration.js';
import { articleView, animateReading } from './articles.js';
import { createProvinceHints } from './province-hints.js';
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
 {id:'ninh-binh',name:'Ninh Bình',province:15,provinceName:'Ninh Bình',number:'01',tag:'Non nước & dấu xưa',subtitle:'Giữa miền di sản, nghe non nước kể chuyện.',coords:[105.974,20.25],callout:[-12,20],
  description:'Khám phá cảnh quan núi đá vôi, những tuyến sông uốn lượn và dấu tích cố đô qua các địa danh của Ninh Bình.',
  headline:'Một miền non nước, nhiều lớp ký ức',geography:'Bản mẫu tập trung vào khu vực Tràng An, Tam Cốc, Hang Múa và cố đô Hoa Lư. Bản đồ nền hiển thị ranh giới tỉnh; phạm vi nội dung hiện chỉ gồm các điểm đến được liệt kê.',
  culture:'Hành trình văn hóa có thể bắt đầu từ không gian lễ hội, nghề thủ công và bữa ăn địa phương. Những câu chuyện về cơm cháy, món dê và sinh hoạt cộng đồng sẽ được biên soạn có nguồn ở bản tiếp theo.',topics:['Cảnh quan núi đá vôi','Không gian cố đô Hoa Lư','Lễ hội và sinh hoạt cộng đồng','Ẩm thực địa phương'],
  history:[['Dấu tích cố đô','Hoa Lư trong dòng lịch sử','Phần này sẽ giới thiệu vai trò của Hoa Lư và các di tích liên quan, kèm mốc thời gian được đối chiếu tài liệu.'],['Di sản & hiện tại','Một cảnh quan đang được gìn giữ','Bổ sung câu chuyện bảo tồn, cộng đồng địa phương và mối liên hệ giữa cảnh quan tự nhiên với di sản văn hóa.']],
  source:'https://vietnam.travel/places-to-go/northern-vietnam/ninh-binh',tour:sourceTravel,
  places:[['trang-an','Tràng An',105.922,20.252,'Cảnh quan','Một hành trình qua sông nước, hang động và những dãy núi đá vôi.'],['tam-coc','Tam Cốc',105.936,20.215,'Sông nước','Tìm hiểu cảnh quan dòng sông và đồng ruộng giữa những dãy núi.'],['hang-mua','Hang Múa',105.938,20.23,'Điểm ngắm cảnh','Một điểm khám phá cảnh quan quanh khu vực Tam Cốc.'],['hoa-lu','Cố đô Hoa Lư',105.905,20.284,'Lịch sử','Không gian di tích để bắt đầu tìm hiểu câu chuyện về cố đô.']]},
 {id:'ha-noi',name:'Hà Nội',province:1,provinceName:'Hà Nội',number:'02',tag:'Ngàn năm văn hiến',subtitle:'Những lớp thời gian giữa nhịp sống phố phường.',coords:[105.854,21.028],callout:[-12,-12],
  description:'Một hành trình qua hồ nước, phố cổ và các di tích để tìm hiểu lịch sử, văn hóa và đời sống của Hà Nội.',
  headline:'Đọc thành phố qua những lớp thời gian',geography:'Sổ tay giới thiệu một nhóm địa danh ở khu vực trung tâm Hà Nội. Vị trí trên bản đồ giúp bạn liên kết các điểm đến với không gian thành phố.',
  culture:'Văn hóa Hà Nội hiện diện trong nếp sống phố phường, nghề truyền thống và ẩm thực. Phở, bún chả và những không gian sinh hoạt quanh hồ là các chủ đề dự kiến được bổ sung.',topics:['Không gian hồ và phố','Di sản Thăng Long','Đời sống đô thị','Phở, bún chả và ẩm thực'],
  history:[['Thăng Long','Dấu tích một kinh đô','Nội dung sẽ liên kết các mốc lịch sử với di tích Hoàng thành Thăng Long và tài liệu tham khảo.'],['Đời sống phố phường','Ký ức trong thành phố','Bổ sung các câu chuyện về phố cổ, nghề truyền thống và sự thay đổi của không gian đô thị.']],
  source:'https://vietnam.travel/places-to-go/northern-vietnam/ha-noi',tour:'https://vietnam.travel/things-to-do/vietnam-360-degrees',
  places:[['ho-hoan-kiem','Hồ Hoàn Kiếm',105.852,21.028,'Cảnh quan','Hồ nước và không gian sinh hoạt quen thuộc ở trung tâm Hà Nội.'],['van-mieu','Văn Miếu – Quốc Tử Giám',105.836,21.028,'Văn hóa','Một địa danh để khám phá truyền thống học tập và kiến trúc.'],['hoang-thanh','Hoàng thành Thăng Long',105.84,21.035,'Lịch sử','Không gian di tích gợi mở những lớp lịch sử của Thăng Long.'],['pho-co','Phố cổ Hà Nội',105.853,21.035,'Đời sống','Những tuyến phố để tìm hiểu đời sống, nghề và văn hóa đô thị.']]},
 {id:'quang-ninh',photoId:'ha-long',name:'Quảng Ninh',province:10,provinceName:'Quảng Ninh',number:'03',tag:'Kỳ quan giữa biển trời',subtitle:'Một thế giới núi đá, sóng nước và làng chài.',coords:[107.083,20.95],callout:[14,5],
  description:'Khám phá Quảng Ninh qua cảnh quan Vịnh Hạ Long, không gian Yên Tử, đảo Cô Tô và những câu chuyện về đời sống địa phương.',
  headline:'Nơi núi đá gặp những con sóng',geography:'Phạm vi sổ tay là thành phố Quảng Ninh theo mốc hành chính từ 01/09/2026. Bản đồ hiển thị toàn tỉnh; nội dung bước đầu giới thiệu một số địa danh tiêu biểu, từ Hạ Long đến Yên Tử và Cô Tô. Các mục khác sẽ được bổ sung sau.',
  culture:'Đời sống ven biển, văn hóa làng chài và ẩm thực hải sản là những chủ đề sẽ được biên soạn. Nội dung về chả mực và nghề biển sẽ được bổ sung cùng nguồn tham khảo.',topics:['Cảnh quan vịnh','Không gian hang động','Văn hóa cộng đồng ven biển','Chả mực và hải sản'],
  history:[['Đất & nước','Câu chuyện hình thành cảnh quan','Phần này sẽ bổ sung thông tin địa chất đã được kiểm chứng, với minh họa và nguồn dẫn.'],['Con người & di sản','Đời sống bên bờ vịnh','Bổ sung tư liệu về cộng đồng, hoạt động bảo tồn và văn hóa địa phương.']],
  source:'https://vietnam.travel/places-to-go/northern-vietnam/ha-long',tour:sourceTravel,
  places:[['vinh-ha-long','Vịnh Hạ Long',107.107,20.875,'Cảnh quan','Khám phá không gian biển và những đảo đá vôi qua bản đồ.'],['yen-tu','Yên Tử',106.717,21.157,'Văn hóa – Lịch sử','Không gian để tìm hiểu cảnh quan, di tích và văn hóa Phật giáo địa phương.'],['co-to','Đảo Cô Tô',107.765,20.971,'Đảo & biển','Một điểm đến để khám phá cảnh quan đảo và đời sống ven biển.'],['bao-tang','Bảo tàng Quảng Ninh',107.101,20.95,'Văn hóa','Nơi bắt đầu tìm hiểu thiên nhiên, lịch sử và con người địa phương.']]},
 {id:'lao-cai',photoId:'sa-pa',name:'Lào Cai',province:4,provinceName:'Lào Cai',number:'04',tag:'Miền mây & sắc bản',subtitle:'Theo triền núi, gặp những câu chuyện bản làng.',coords:[103.844,22.336],callout:[-12,-12],
  description:'Khám phá Lào Cai qua cảnh quan Sa Pa, Bắc Hà, Mù Cang Chải và những nét văn hóa đa dạng của cộng đồng địa phương.',
  headline:'Một hành trình giữa núi, mây và bản làng',geography:'Phạm vi sổ tay là tỉnh Lào Cai theo ranh giới trên bản đồ 34 tỉnh/thành phố. Nội dung bước đầu giới thiệu Sa Pa, Bắc Hà và Mù Cang Chải; các địa danh và chủ đề khác sẽ được bổ sung sau.',
  culture:'Các câu chuyện văn hóa cần được thể hiện theo từng cộng đồng và có nguồn rõ ràng. Trang này sẽ bổ sung nội dung về nghề dệt, sinh hoạt bản làng và ẩm thực, tôn trọng sự đa dạng địa phương.',topics:['Cảnh quan núi và thung lũng','Ruộng bậc thang','Nghề thủ công địa phương','Văn hóa các cộng đồng'],
  history:[['Bản làng','Những câu chuyện địa phương','Bổ sung tư liệu về cộng đồng và các địa danh; phân biệt rõ lịch sử được ghi nhận với truyền kể.'],['Lào Cai hôm nay','Cảnh quan và đời sống','Bổ sung thông tin về bảo tồn văn hóa, thiên nhiên và sự thay đổi của không gian địa phương.']],
  source:'https://vietnam.travel/places-to-go/northern-vietnam/sapa',tour:null,
  places:[['fansipan','Fansipan',103.775,22.303,'Núi cao','Một địa danh gắn với cảnh quan núi Hoàng Liên Sơn.'],['bac-ha','Bắc Hà',104.291,22.539,'Văn hóa','Khám phá không gian chợ và đời sống của các cộng đồng địa phương.'],['muong-hoa','Thung lũng Mường Hoa',103.878,22.298,'Thung lũng','Không gian cảnh quan và bản làng để tìm hiểu vùng Sa Pa.'],['mu-cang-chai','Mù Cang Chải',104.089,21.851,'Ruộng bậc thang','Một điểm khám phá cảnh quan ruộng bậc thang và đời sống vùng cao.']]}
];
const tabs = [['dia-danh','Địa danh'],['bo-anh','Bộ ảnh AI'],['du-lich','Du lịch online'],['lich-su','Lịch sử'],['van-hoa','Văn hóa – Ẩm thực'],['nguon','Nguồn tham khảo']];
// Scene order matches each local tour manifest.
const onlineTours = {
 'lao-cai':{"mediaId":"sa-pa","provider":"VRTour","sourceUrl":"https://3d.vrtour.vn/tour/sapa/thi-xa-sapa.html","title":"Khám phá Sa Pa trong góc nhìn 360°","scope":"Tour tại trung tâm Sa Pa, thuộc Lào Cai: nhà thờ đá, quảng trường, hồ Sa Pa, Sun Plaza và chợ Sa Pa.","scenes":["Toàn cảnh - Thị xã Sa Pa – góc 1","Toàn cảnh - Thị xã Sa Pa – góc 2","Toàn cảnh - Thị xã Sa Pa – góc 3","Toàn cảnh - Thị xã Sa Pa – góc 4","Toàn cảnh - Thị xã Sa Pa – góc 5","Toàn cảnh - Hồ Sa Pa","Toàn cảnh - Quảng trường trung tâm","Quảng trường trung tâm – góc 1","Nhà thờ đá","Quảng trường trung tâm – góc 2","Quảng trường trung tâm – góc 3","Sun Plaza","Vườn hoa hồ Sa Pa","Quảng trường hồ Sa Pa","Hồ Sa Pa","Con đường tình yêu – góc 1","Con đường tình yêu – góc 2","Con đường tình yêu – góc 3","Con đường tình yêu – góc 4","Bến xe - Chợ Sa Pa","Chợ Sa Pa – góc 1","Chợ Sa Pa – góc 2"]},
 'ninh-binh':{mediaId:'ninh-binh',provider:'Vietnam.travel',sourceUrl:'https://vietnam.travel/vietnam-virtual-tours',title:'Non nước Ninh Bình trong góc nhìn 360°',scope:'Khám phá Hang Múa, Tam Cốc, Tràng An và chùa Bái Đính.',scenes:['Hang Múa','Tam Cốc từ trên cao','Tam Cốc – sông nước','Tràng An từ trên cao','Đền tại Tràng An','Bái Đính từ trên cao','Chùa Bái Đính','Tam Cốc – góc nhìn khác']},
 'ha-noi':{mediaId:'ha-noi',provider:'AirPano',slug:'hanoi-vietnam',title:'Hà Nội trong góc nhìn 360°',scope:'Hồ Hoàn Kiếm và những góc nhìn trên cao của trung tâm Hà Nội.',scenes:['Hồ Hoàn Kiếm','Tháp Rùa trên hồ Hoàn Kiếm','Hà Nội từ trên cao','Hà Nội lúc chiều tối','Hà Nội về đêm']},
 'quang-ninh':{mediaId:'ha-long',provider:'AirPano',slug:'halong-bay-vietnam',title:'Một hành trình quanh Vịnh Hạ Long',scope:'Tour giới thiệu khu vực Vịnh Hạ Long, thuộc Quảng Ninh.',scenes:['Bình minh trên Vịnh Hạ Long','Những đảo đá trên vịnh','Đảo Cống Đỏ từ độ cao 120 m','Đảo Cống Đỏ từ độ cao 70 m','Bên trong hang động','Làng chài Cống Đầm từ độ cao 100 m','Làng chài Cống Đầm từ độ cao 30 m','Cảng Hạ Long','Quanh đảo Cống Đỏ']}
};
const tourSource=(tour,index=0)=>tour.sourceUrl || `https://www.airpano.com/360photo/${tour.slug}/?startscene=${index}`;
let tourLoadTimer, tourViewer, tourAbort;
let tourGeneration=0;
let tourNarration;
const tourMetadata=new Map();
const legacyIds = {'ha-long':'quang-ninh','sa-pa':'lao-cai'};
const photoId = d => d.photoId || d.id;
const scopeLabel = 'Ninh Bình, Hà Nội, Quảng Ninh và Lào Cai';
const destinationById = id => destinations.find(d => d.id === id);
let geo, credits = [], previousDestination, toastTimer;
let aiRegions = {};
let articleRegions = {};
const mediaRegion = d => ({'ha-long':'quang-ninh','sa-pa':'lao-cai'}[d.id] || d.id);
const imagesFor = d => aiRegions[mediaRegion(d)]?.images || [];
const placeAliases = {'van-mieu':'van-mieu-quoc-tu-giam','hoang-thanh':'hoang-thanh-thang-long','pho-co':'pho-co-ha-noi','bao-tang':'bao-tang-quang-ninh','bac-ha':'cho-bac-ha','tam-coc':'tam-coc-bich-dong'};
const imageForPlace = (d,id) => imagesFor(d).find(image=>image.id===id || image.placeId===(placeAliases[id] || id));
function heroImage(d) {
 const preferred={'ha-noi':'ho-hoan-kiem','quang-ninh':'vinh-ha-long','lao-cai':'sa-pa','ninh-binh':'trang-an'}[d.id];
 return imageForPlace(d,preferred) || imagesFor(d)[0];
}
function heroAttributes(d) {
 const image=heroImage(d);
 return `src="${escapeHTML(image?.src || `assets/${photoId(d)}.jpg`)}" alt="${escapeHTML(image?.alt || photoDescription(photoId(d)))}"`;
}
function placeImage(d,id,compact=false) {
 const image=imageForPlace(d,id);
 if(!image && d.id==='ha-noi' && id==='ho-hoan-kiem'){
  const credit=creditFor(d);
  return `<figure class="place-illustration${compact?' compact':''}"><img src="assets/ha-noi.jpg" alt="${photoDescription('ha-noi')}" width="1536" height="864" loading="lazy" decoding="async"><figcaption>Hồ Hoàn Kiếm · Ảnh thật · <a href="${escapeHTML(credit?.source || '')}" target="_blank" rel="noopener noreferrer">${escapeHTML(credit?.author || 'Wikimedia Commons')} / Wikimedia Commons</a> · ${escapeHTML(credit?.license || '')}</figcaption></figure>`;
 }
 return image?`<figure class="place-illustration${compact?' compact':''}"><button type="button" data-ai-image="${escapeHTML(image.id)}" data-ai-destination="${d.id}" aria-label="Xem ảnh lớn ${escapeHTML(image.name)}"><img src="${escapeHTML(image.src)}" alt="${escapeHTML(image.alt)}" width="1536" height="864" loading="lazy" decoding="async"></button><figcaption>${escapeHTML(image.name)} — ${escapeHTML(image.caption)}</figcaption></figure>`:'';
}
function selectedPlaceView(d,p) { return `${placeImage(d,p[0],true)}<span class="eyebrow">${p[4]}</span><h3>${p[1]}</h3><p>${p[5]}</p>`; }
function galleryView(d) {
 const images=imagesFor(d), region=aiRegions[mediaRegion(d)];
 return `<div class="section-heading"><h2>Bộ ảnh ${escapeHTML(region?.name || d.provinceName)}</h2><span>${images.length} hình minh họa</span></div><p class="gallery-intro">Khám phá các địa danh qua hình minh họa do AI tạo. Chọn một ảnh để xem lớn và đọc giới thiệu. Ảnh không phải tư liệu hay bản đồ dẫn đường.</p>${images.length?`<div class="ai-gallery">${images.map(image=>`<figure class="gallery-item"><button type="button" data-ai-image="${escapeHTML(image.id)}" data-ai-destination="${d.id}" aria-label="Xem ảnh lớn ${escapeHTML(image.name)}"><img src="${escapeHTML(image.src)}" alt="${escapeHTML(image.alt)}" width="1536" height="864" loading="lazy" decoding="async"><span class="gallery-expand" aria-hidden="true">${icon('focus')}</span></button><figcaption><strong>${escapeHTML(image.name)}</strong><span>${escapeHTML(image.caption)}</span></figcaption></figure>`).join('')}</div>`:`<div class="gallery-empty"><h3>Bộ ảnh đang được chuẩn bị</h3><p>Sổ tay sẽ bổ sung hình minh họa cho các địa danh tại ${escapeHTML(d.provinceName)}.</p></div>`}`;
}
function openImage(d,id) {
 const image=imagesFor(d).find(image=>image.id===id);if(!image)return;
 // A map dialog can already be open: the native dialog stack restores focus on close.
 openInfo(escapeHTML(image.name),`<figure class="image-full"><img src="${escapeHTML(image.src)}" alt="${escapeHTML(image.alt)}" width="1536" height="864"><figcaption>${escapeHTML(image.name)} — ${escapeHTML(image.caption)}</figcaption></figure><p>${escapeHTML(image.summary)}</p><div class="source-item"><strong>Nguồn giới thiệu địa danh</strong>${image.sources.map(source=>`<p><a href="${escapeHTML(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(source.title)} ↗</a></p>`).join('')}<p>Nguồn hỗ trợ nội dung giới thiệu; hình minh họa không xác nhận từng chi tiết kiến trúc hoặc cảnh quan.</p></div>`);
 infoDialog.classList.add('image-viewer');
}

const savedKey = 'atlas-viet-saved';
const journalKey = 'atlas-viet-journal';
const seedKey = 'atlas-viet-notebook-seeded-v1';
let saved = [], journal = {}, storageAvailable = true;
const sampleNotes = {
 'ninh-binh': {note:'Muốn đọc thêm về cố đô Hoa Lư, rồi khám phá Tràng An qua tour 360°. Lưu lại Tam Cốc để so sánh cảnh quan sông nước.',visited:false},
 'ha-noi': {note:'Đã đọc câu chuyện Hồ Hoàn Kiếm và Văn Miếu. Lần tới tìm hiểu các lớp lịch sử ở Hoàng thành Thăng Long.',visited:true},
 'lao-cai': {note:'Để dành một buổi tìm hiểu ruộng bậc thang Mù Cang Chải và văn hóa chợ Bắc Hà. Nhớ xem nguồn của từng bài.',visited:false}
};
try {
 const value = JSON.parse(localStorage.getItem(savedKey) || '[]');
 if(Array.isArray(value)) saved = [...new Set(value.map(id=>legacyIds[id] || id).filter(id=>destinationById(id)))];
 const storedJournal = JSON.parse(localStorage.getItem(journalKey) || '{}');
 if(storedJournal && typeof storedJournal==='object' && !Array.isArray(storedJournal)) {
  for(const d of destinations) {
   const entry=storedJournal[d.id];
   if(entry && typeof entry==='object') journal[d.id]={note:typeof entry.note==='string'?entry.note.slice(0,2000):'',visited:entry.visited===true};
  }
 }
 if(!localStorage.getItem(seedKey)) {
  if(!saved.length) {saved=Object.keys(sampleNotes);journal={...journal,...sampleNotes};}
  localStorage.setItem(journalKey,JSON.stringify(journal));
  localStorage.setItem(savedKey,JSON.stringify(saved));
  localStorage.setItem(seedKey,'1');
 }
 localStorage.setItem(savedKey,JSON.stringify(saved));
} catch {storageAvailable=false;}
let notebookSearch='', notebookFilter='all', notebookSort='recent';
const main = $('#main');
const dialog = $('#destination-dialog');
const infoDialog = $('#info-dialog');
function notify(message) { const toast=$('#toast'); toast.textContent=message; toast.hidden=false; clearTimeout(toastTimer); toastTimer=setTimeout(()=>toast.hidden=true,4200); }
function updateSavedCount() { $('#saved-count').textContent=saved.length; }
function persistNotebook() {
 try {localStorage.setItem(savedKey,JSON.stringify(saved));localStorage.setItem(journalKey,JSON.stringify(journal));storageAvailable=true;return true;}
 catch {storageAvailable=false;notify('Không thể lưu lâu dài trên trình duyệt này. Sổ tay vẫn dùng được trong phiên hiện tại.');return false;}
}
function toggleSaved(id) {
 if(!destinationById(id))return;
 const had=saved.includes(id);saved=had?saved.filter(v=>v!==id):[...saved,id];
 if(!had && !journal[id])journal[id]={note:'',visited:false};
 const persisted=persistNotebook();
 updateSavedCount();updateSaveButton(id);
 if(persisted)notify(had?'Đã bỏ địa phương khỏi sổ tay.':'Đã lưu địa phương vào sổ tay của bạn.');
 if(location.hash.startsWith('#/so-tay'))notebookView();
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
function offshoreIslandPaths() {
 // These offshore components belong to the existing Đà Nẵng/Khánh Hòa features.
 // Reuse their geometry; a dark overlay keeps tiny islands visible at overview scale.
 return geo.features.filter(f=>[21,23].includes(f.properties.atlasId)).map(f=>{
  const islands=polygons(f).filter(poly=>poly[0].every(([lon])=>lon>110));
  if(!islands.length)return '';
  return `<path class="offshore-islands" d="${pathFor({geometry:{type:'MultiPolygon',coordinates:islands}})}" fill-rule="evenodd" aria-hidden="true"/>`;
 }).join('');
}
function countryMarker(d) {
 const [x,y]=project(d.coords),[dx,dy]=d.callout; const textX=x+dx,textY=y+dy;
 return `<g class="marker" role="button" tabindex="0" data-open="${d.id}" aria-label="Khám phá ${d.name}"><line class="marker-line" x1="${x}" y1="${y}" x2="${textX}" y2="${textY-3}"/><circle class="pulse" cx="${x}" cy="${y}" r="12"/><circle class="outer" cx="${x}" cy="${y}" r="6"/><circle class="inner" cx="${x}" cy="${y}" r="2.5"/><text class="marker-label" x="${textX}" y="${textY}" text-anchor="${dx<0?'end':'start'}">${d.name}</text></g>`;
}
function destinationCard(d) { return `<button class="destination-card" data-open="${d.id}" data-card="${d.id}" aria-label="Khám phá ${d.name}"><span class="destination-thumb"><img ${heroAttributes(d)} width="76" height="58"></span><span class="card-copy"><strong>${d.name}</strong><small>${d.tag}</small><small class="card-caption">${escapeHTML(heroImage(d)?.name || photoDescription(photoId(d)))} · ${heroImage(d)?'Minh họa do AI tạo':escapeHTML(creditFor(d)?.author || 'Wikimedia Commons')}</small></span><span class="card-arrow">${icon('arrow')}</span></button>`; }
function photoDescription(id) { return {'ninh-binh':'Cảnh quan Tràng An với núi đá và thuyền trên sông','ha-noi':'Tháp Rùa giữa Hồ Hoàn Kiếm','ha-long':'Toàn cảnh vịnh với những đảo đá','sa-pa':'Ruộng bậc thang ở Sa Pa'}[id]; }
function homeView() {
 previousDestination=null;
 main.innerHTML=`<div class="atlas-layout"><section class="intro" aria-labelledby="home-title"><span class="eyebrow">ĐI QUA ĐỊA DANH · CHẠM VÀO TRI THỨC</span><h1 id="home-title">Mỗi miền đất,<br> một <em>câu chuyện.</em></h1><p class="intro-description">Mở bản đồ, chọn một miền đất. Cùng khám phá địa lý, lịch sử và những nét văn hóa làm nên bản sắc Việt Nam.</p><div class="intro-rule">Bốn tỉnh/thành phố, một hành trình</div><div class="destination-list">${destinations.map(destinationCard).join('')}</div><p class="list-caption">${icon('pin')} Chọn trên bản đồ hoặc trong danh sách để bắt đầu</p></section><section class="map-panel" aria-label="Bản đồ khám phá Việt Nam"><div class="map-topbar"><span class="map-title">${icon('map')} BẢN ĐỒ VIỆT NAM</span><button id="focus-north">${icon('focus')} Khám phá 4 tỉnh/thành</button></div><div class="map-viewport"><svg id="country-map" class="country-svg" viewBox="0 0 820 820" aria-label="Bản đồ 34 tỉnh thành Việt Nam" role="group">${provincePaths()}${offshoreIslandPaths()}<text class="map-region-label" x="210" y="196">MIỀN BẮC</text><text class="map-region-label" x="337" y="423">MIỀN TRUNG</text><text class="map-region-label" x="215" y="710">MIỀN NAM</text><text class="sea-label" x="450" y="490" transform="rotate(-15 450 490)">Biển Đông</text>${islandLabels()}${destinations.map(countryMarker).join('')}</svg></div><div class="compass-decoration">BẮC<svg viewBox="0 0 32 48" aria-hidden="true"><path d="m16 5 7 26-7-7-7 7Z" fill="#667d60"/><path d="m16 5 7 26-7-7Z" fill="#c79a45"/><path d="M16 26v16" stroke="#667d60"/></svg></div><div class="map-controls" aria-label="Điều khiển bản đồ"><button data-zoom="in" aria-label="Phóng to">+</button><button data-zoom="out" aria-label="Thu nhỏ">−</button><button data-zoom="reset" aria-label="Hiện toàn bộ bản đồ">${icon('focus')}</button></div><div class="map-legend"><span><i class="legend-dot"></i> Có trong sổ tay</span><span><i class="legend-dot muted"></i> Chưa có nội dung</span></div><button class="map-attribution" data-sources>Ranh giới tham khảo · Xem nguồn ↗</button><div id="map-tooltip" class="map-tooltip" hidden></div></section></div><div class="scope-strip">${icon('info')}<span><strong>Phạm vi sổ tay:</strong> ${scopeLabel}.</span><span class="scope-divider"></span><span class="boundary-note">Nội dung ngắn dành cho bản mẫu · Sẽ tiếp tục bổ sung</span></div>`;
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
 let zoomFrame;
 const setBox=(smooth=false)=>{
  cancelAnimationFrame(zoomFrame);
  if(!smooth || matchMedia('(prefers-reduced-motion: reduce)').matches){svg.setAttribute('viewBox',box.join(' '));return;}
  const from=svg.getAttribute('viewBox').split(/\s+/).map(Number),to=[...box],start=performance.now();
  const tick=now=>{if(!svg.isConnected)return;const t=Math.min(1,(now-start)/320),ease=1-Math.pow(1-t,3);svg.setAttribute('viewBox',to.map((v,i)=>from[i]+(v-from[i])*ease).join(' '));if(t<1)zoomFrame=requestAnimationFrame(tick);};
  zoomFrame=requestAnimationFrame(tick);
 };setBox();
 function zoom(factor,center,smooth=false) { const max=base[2]*1.4,min=base[2]/6;let newW=Math.max(min,Math.min(max,box[2]*factor));let ratio=newW/box[2];let point=center||[box[0]+box[2]/2,box[1]+box[3]/2];box=[point[0]+(box[0]-point[0])*ratio,point[1]+(box[1]-point[1])*ratio,newW,box[3]*ratio];setBox(smooth);tooltip.hidden=true; }
 $('#focus-north').onclick=()=>{const points=destinations.map(d=>project(d.coords));const minX=Math.min(...points.map(p=>p[0])),maxX=Math.max(...points.map(p=>p[0]));const minY=Math.min(...points.map(p=>p[1])),maxY=Math.max(...points.map(p=>p[1]));box=[minX-110,minY-65,maxX-minX+245,maxY-minY+190];setBox(true);};
 // Open the map in the same view as the four-destination shortcut.
 $('#focus-north').click();setBox();
 $$('[data-zoom]').forEach(button=>button.onclick=()=>{if(button.dataset.zoom==='reset'){box=[...base];setBox(true);}else zoom(button.dataset.zoom==='in'?.8:1.25,undefined,true);});
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
 const box=localViewBox(d), mobile=innerWidth<760;
 const minimumWidth=box[3]*(mobile?310/230:480/380);
 if(box[2]<minimumWidth){box[0]-=(minimumWidth-box[2])/2;box[2]=minimumWidth;}
 const scale=Math.max(box[2]/(mobile?310:480),box[3]/(mobile?230:380));
 const places=d.places.map(p=>p[0]==='muong-hoa'?['sa-pa','Sa Pa',...d.coords]:p);
 const markers=places.map((p,i)=>{
  const [x,y]=project([p[2],p[3]]), right=i%2===1;
  const width=box[2]*.43,height=60*scale;
  const cardX=box[0]+box[2]*(right?.55:.02);
  const cardY=box[1]+box[3]*[.08,.29,.54,.75][i];
  const image=imageForPlace(d,p[0]);
  const actualPhoto=!image && d.id==='ha-noi' && p[0]==='ho-hoan-kiem';
  const src=image?.src || (actualPhoto?'assets/ha-noi.jpg':null);
  if(!src)return '';
  const id=placeAliases[p[0]] || p[0];
  const caption=image?'Minh họa do AI tạo':'Ảnh thật · Wikimedia';
  const credit=actualPhoto?creditFor(d):null;
  return `<g class="landmark-marker"><line x1="${x}" y1="${y}" x2="${cardX+(right?0:width)}" y2="${cardY+height/2}" stroke="#627951" stroke-width="${scale}"/><circle cx="${x}" cy="${y}" r="${3*scale}" fill="#a77235" stroke="#faf8f1" stroke-width="${scale}"/><foreignObject x="${cardX}" y="${cardY}" width="${width}" height="${height}"><a xmlns="http://www.w3.org/1999/xhtml" class="landmark-card" data-local-landmark href="#/dia-phuong/${d.id}?tab=dia-danh&diem=${id}" aria-label="Đọc về ${escapeHTML(p[1])}" title="${escapeHTML(p[1])} · ${escapeHTML(image?.caption || credit?.author+' / Wikimedia Commons · '+credit?.license)}" style="--landmark-scale:${scale}px"><img src="${escapeHTML(src)}" alt="${escapeHTML(image?.alt || 'Hồ Hoàn Kiếm — ảnh thật')}"/><span><strong>${escapeHTML(p[1])}</strong><small>${caption}</small></span></a></foreignObject></g>`;
 }).join('');
 return `<svg viewBox="${box.join(' ')}" role="group" aria-label="Bản đồ và các điểm du lịch nổi bật tại ${escapeHTML(d.name)}"><title>Bản đồ ${escapeHTML(d.name)}</title>${provincePaths(true,d.province)}${markers}</svg>`;
}
function openDestination(id) {
 const d=destinationById(id);if(!d)return;
 const region=articleRegions[id];
 const overview=region?.sections[0];
 const image=heroImage(d);
 $('#dialog-content').innerHTML=`<div class="dialog-header"><div><span class="eyebrow">BẢN ĐỒ · SỔ TAY ĐỊA PHƯƠNG</span><h2 id="destination-title">${escapeHTML(d.name)}</h2></div><button class="icon-button" data-close-destination aria-label="Đóng bản đồ địa phương">×</button></div><div class="dialog-grid overview-dialog"><div class="local-map-panel"><span class="eyebrow">${escapeHTML(d.name)} · RANH GIỚI HÀNH CHÍNH</span>${localMap(d)}<div class="local-map-caption">Điểm du lịch ở vị trí tham khảo · Chọn ảnh để đọc về địa danh<br>Ranh giới: Vietnamese Provinces Database</div></div><div class="dialog-sidebar"><span class="eyebrow">TỔNG QUAN ĐỊA PHƯƠNG</span><h3>${escapeHTML(region?.title || d.headline)}</h3>${image?placeImage(d,image.id,true):''}<p>${escapeHTML(overview?.text || d.description)}</p>${overview?`<p class="article-citations">Nguồn: ${overview.source_ids.map(id=>region.sources[id]).filter(Boolean).map(source=>`<a href="${escapeHTML(source.url)}" target="_blank" rel="noopener noreferrer">${escapeHTML(source.title)} ↗</a>`).join(' · ')}</p>`:''}<a id="detail-link" class="primary-button" href="#/dia-phuong/${d.id}?tab=dia-danh">Tìm hiểu chi tiết ${icon('arrow')}</a></div></div>`;
 $('#dialog-content').dataset.destination=id;
 if(!dialog.open)dialog.showModal();
 $('[data-close-destination]',dialog).onclick=()=>dismissDialog(dialog);
 $('#detail-link').onclick=()=>dialog.close();
 $$('[data-local-landmark]',dialog).forEach(link=>link.onclick=()=>dialog.close());
}
function creditFor(d) { return credits.find(c=>c.id===photoId(d)); }
function photoCredit(d) { const image=heroImage(d);if(image)return `${escapeHTML(image.name)} · Minh họa do AI tạo bằng API Ban tổ chức · Không phải ảnh tư liệu`; const c=creditFor(d);return c?`Ảnh thực tế dùng tạm · <a href="${c.source}" target="_blank" rel="noopener noreferrer">${escapeHTML(c.author)} / Wikimedia Commons</a> · <a href="${c.licenseUrl}" target="_blank" rel="noopener noreferrer">${c.license}</a> · Thu nhỏ, cắt khung hiển thị`:'Ảnh giao diện tạm thời · Chưa phải hình minh họa AI'; }
function detailView(id,params) {
 const d=destinationById(id);if(!d){notFound();return;}
 const tab=tabs.some(([t])=>t===params.get('tab'))?params.get('tab'):'dia-danh';
 const changed=previousDestination!==id;previousDestination=id;
 main.innerHTML=`<div class="detail-shell"><div class="breadcrumb"><a href="#/">${icon('back')} Bản đồ Việt Nam</a><span>/</span><span>${d.name}</span></div><section class="detail-hero" aria-labelledby="detail-title"><img ${heroAttributes(d)}><div class="detail-hero-content"><span class="eyebrow">TỈNH/THÀNH PHỐ ${d.number} · ${d.tag}</span><h1 id="detail-title">${d.name}</h1><p>${d.subtitle} ${d.description}</p></div></section><p class="photo-caption">${photoCredit(d)}</p><div class="detail-actions"><p>${icon('pin')} Phạm vi: ${['ha-noi','quang-ninh'].includes(d.id)?'thành phố':'tỉnh'} ${d.name}<br>Bài viết có nguồn · 29 hồ sơ trong sổ tay</p><button class="secondary-button" data-save="${d.id}" aria-pressed="${saved.includes(d.id)}">${icon(saved.includes(d.id)?'check':'bookmark')}${saved.includes(d.id)?'Đã lưu vào sổ tay':'Lưu vào sổ tay'}</button></div><div class="detail-tabs" role="tablist" aria-label="Nội dung sổ tay ${d.name}">${tabs.map(([key,label])=>`<button role="tab" id="tab-${key}" aria-selected="${key===tab}" aria-controls="tab-content" tabindex="${key===tab?0:-1}" data-tab="${key}" data-destination="${d.id}">${label}</button>`).join('')}</div><section class="tab-content" id="tab-content" role="tabpanel" aria-labelledby="tab-${tab}" tabindex="0">${tabView(d,tab)}</section></div>`;
 if(changed)window.scrollTo({top:0,behavior:'instant'});
 animateReading(main);
 if(params.get('diem')){const point=placeAliases[params.get('diem')] || params.get('diem');const p=$(`[data-place-card="${CSS.escape(point)}"]`);if(p){p.style.borderColor='#8ea387';p.style.background='#eef0e5';}}
}
function tabView(d,tab) {
 if(tab==='bo-anh')return galleryView(d);
 if(tab==='du-lich')return onlineTourView(d);
 return articleView(d,tab,articleRegions,placeImage) || '<p>Bài viết chưa tải được. Hãy tải lại trang.</p>';
}
function onlineTourView(d) {
 const tour=onlineTours[d.id];
 if(!tour)return `<div class="tour-empty"><span class="eyebrow">DU LỊCH ONLINE · 360°</span><h2>${d.id==='ninh-binh'?'Một hành trình đang được chuẩn bị':'Hẹn một chuyến khám phá mới'}</h2><p>${d.id==='ninh-binh'?'Tour 360° Ninh Bình đang được bổ sung. Bạn có thể tiếp tục khám phá các địa danh trên bản đồ trong lúc chờ.':'Chưa có tour 360° cho Lào Cai trong sổ tay này. Những hành trình mới sẽ được bổ sung khi có dữ liệu phù hợp.'}</p><span class="draft-badge">${d.id==='ninh-binh'?'Dữ liệu 360° đang được bổ sung':'Chưa có tour 360°'}</span><a class="secondary-button" href="#/dia-phuong/${d.id}?tab=dia-danh">${icon('map')} Khám phá địa danh</a></div>`;
 return `<div class="tour-section" data-tour="${d.id}" data-tour-scene="0"><div class="section-heading"><h2>${tour.title}</h2><span>${String(tour.scenes.length).padStart(2,'0')} cảnh · ${tour.provider}</span></div><p class="tour-intro">${tour.scope} Chọn một cảnh, rồi kéo để nhìn quanh. Dùng nút +/− để phóng to hoặc thu nhỏ.</p><div class="tour-stage" id="tour-stage"><div class="tour-poster" id="tour-poster"><img src="assets/${photoId(d)}.jpg" alt="${photoDescription(photoId(d))}" class="tour-cover"><div class="tour-poster-content"><span class="tour-label">MỞ MỘT GÓC NHÌN MỚI</span><h3 id="tour-start-title">${tour.scenes[0]}</h3><p>Một chuyến đi ngay trên màn hình của bạn.</p><button class="primary-button" data-tour-start>${icon('arrow')} Bắt đầu khám phá</button><small>Ảnh 360° và thuyết minh tiếng Việt · Tải trực tiếp từ website này</small></div></div></div><p class="tour-image-caption">Ảnh bìa: ${escapeHTML(photoDescription(photoId(d)))} · Ảnh thật · ${escapeHTML(creditFor(d)?.author || 'Wikimedia Commons')} / Wikimedia Commons · ${escapeHTML(creditFor(d)?.license || '')}. Ảnh panorama 360°: <span id="panorama-caption">${tour.scenes[0]} · Ảnh thật · ${tour.provider}</span>.</p><div class="tour-toolbar"><p id="tour-status" role="status" aria-live="polite">Tour sẽ được tải khi bạn chọn “Bắt đầu khám phá”.</p><div id="tour-controls" hidden><button class="secondary-button" data-tour-retry>Thử lại</button><button class="secondary-button" data-tour-fullscreen>${icon('focus')} Toàn màn hình</button><button class="secondary-button" data-tour-stop>Dừng tour</button></div></div>${narrationView()}<div class="tour-scenes-heading"><h3>Chọn cảnh khám phá</h3><span>Chọn trong danh sách hoặc bấm điểm chuyển cảnh trên ảnh.</span></div><div class="tour-scenes" aria-label="Các cảnh trong tour">${tour.scenes.map((title,index)=>`<button class="tour-scene" data-tour-select="${index}" aria-pressed="${index===0}"><span class="tour-scene-number">${String(index+1).padStart(2,'0')}</span><span>${title}</span>${icon('arrow')}</button>`).join('')}</div><div class="tour-credit"><p>${tour.provider==='AirPano'?'Courtesy of <a href="https://www.airpano.com/" target="_blank" rel="noopener noreferrer">www.AirPano.com</a>':`Nguồn ảnh: <a href="${escapeHTML(tour.sourceUrl)}" target="_blank" rel="noopener noreferrer">${escapeHTML(tour.provider)} — ${tour.mediaId==='sa-pa'?'Sa Pa 360°':'Ninh Binh in 360'}</a>`} · Nguồn ảnh panorama: ${tour.provider} · Trình xem 360°: Pannellum.</p><a id="tour-source" href="${tourSource(tour)}" target="_blank" rel="noopener noreferrer">Nguồn ảnh gốc ${icon('external')}</a></div></div>`;
}
function playTourNarration() {
 const section=$('[data-tour]');if(!section)return;
 if(!tourNarration)tourNarration=createNarration(section.dataset.tour,section);
 tourNarration.start();
}
function stopTourNarration() {
 tourNarration?.destroy();tourNarration=null;
}
function disposeOnlineTour(keepNarration=false) {
 tourGeneration++;tourAbort?.abort();tourAbort=null;
 clearTimeout(tourLoadTimer);tourViewer?.destroy();tourViewer=null;
 $('#tour-viewer')?.remove();
 if(!keepNarration)stopTourNarration();
}
function updateTourSelection(index) {
 const section=$('[data-tour]');if(!section)return;
 const tour=onlineTours[section.dataset.tour];
 section.dataset.tourScene=String(index);
 $$('[data-tour-select]',section).forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.tourSelect)===index)));
 $('#tour-start-title').textContent=tour.scenes[index];
 if($('#panorama-caption'))$('#panorama-caption').textContent=`${tour.scenes[index]} · Ảnh thật · ${tour.provider}`;
 $('#tour-source').href=tourSource(tour,index);
}
function tourLoading() {
 clearTimeout(tourLoadTimer);$('#tour-status').textContent='Đang tải cảnh 360°…';
 const generation=tourGeneration;
 tourLoadTimer=setTimeout(()=>{if(generation===tourGeneration&&$('#tour-status'))$('#tour-status').textContent='Cảnh đang tải chậm. Bạn có thể chọn Thử lại.';},15000);
}
async function startOnlineTour() {
 const section=$('[data-tour]');if(!section)return;
 const tour=onlineTours[section.dataset.tour];if(!tour)return;
 disposeOnlineTour(true);const generation=tourGeneration;
 const controller=new AbortController();tourAbort=controller;
 $('#tour-poster').hidden=true;$('#tour-controls').hidden=false;tourLoading();
 playTourNarration();
 const mediaId=tour.mediaId;
 try {
  let metadata=tourMetadata.get(mediaId);
  if(!metadata){
   const response=await fetch(`assets/360/${mediaId}.json`,{signal:controller.signal});
   if(!response.ok)throw new Error('Không tải được danh sách cảnh.');
   metadata=await response.json();tourMetadata.set(mediaId,metadata);
  }
  if(generation!==tourGeneration||!section.isConnected)return;
  const container=document.createElement('div');container.id='tour-viewer';
  container.setAttribute('aria-label','Cảnh 360°. Kéo để nhìn quanh, dùng nút cộng và trừ để zoom.');
  $('#tour-stage').append(container);
  const current=()=>generation===tourGeneration&&section.isConnected;
  tourViewer=createLocalTour(container,metadata,tour.scenes,Number(section.dataset.tourScene),{
   change:index=>{if(current()){updateTourSelection(index);tourLoading();}},
   load:()=>{if(current()){clearTimeout(tourLoadTimer);$('#tour-status').textContent=`Đang xem: ${tour.scenes[Number(section.dataset.tourScene)]}. Kéo để nhìn quanh; dùng +/− để zoom.`;}},
   error:()=>{if(current()){clearTimeout(tourLoadTimer);$('#tour-status').textContent='Không tải được cảnh 360°. Hãy chọn Thử lại hoặc một cảnh khác.';}}
  });
 } catch(error) {
  if(generation!==tourGeneration||error.name==='AbortError')return;
  clearTimeout(tourLoadTimer);$('#tour-status').textContent='Không tải được cảnh 360°. Hãy chọn Thử lại.';
 }
}
function selectTourScene(index) {
 const section=$('[data-tour]');if(!section)return;
 const tour=onlineTours[section.dataset.tour];if(!Number.isInteger(index)||!tour.scenes[index])return;
 updateTourSelection(index);
 if(tourViewer){tourLoading();tourViewer.select(index);}
}
function stopOnlineTour() {
 disposeOnlineTour();
 $('#tour-poster').hidden=false;$('#tour-controls').hidden=true;
 $('#tour-status').textContent='Tour đã dừng. Bạn có thể chọn cảnh khác và bắt đầu lại.';
 $('[data-tour-start]').focus();
}
function openInfo(title,content) { infoDialog.classList.remove('image-viewer'); $('#info-content').innerHTML=`<span class="eyebrow">ATLAS VIỆT · SỔ TAY ĐIỆN TỬ</span><h2 id="info-title">${title}</h2>${content}`;if(!infoDialog.open)infoDialog.showModal(); }
function showSources() { openInfo('Nguồn dữ liệu & ghi chú',`<p>Bản mẫu giới thiệu bốn tỉnh/thành phố: ${scopeLabel}. Bài viết và 29 hồ sơ địa danh có dẫn nguồn theo từng phần; vị trí trên bản đồ vẫn là tọa độ tham khảo.</p><div class="source-item"><strong>Bản đồ tham khảo</strong><p><a href="https://github.com/thanglequoc/vietnamese-provinces-database" target="_blank" rel="noopener noreferrer">Vietnamese Provinces Database</a> · Snapshot geojson_11Mar2026; đường biên giản lược để hiển thị. Nguồn gốc dữ liệu: sapnhap.bando.com.vn. Cần đối chiếu <a href="https://vnsdi.mae.gov.vn/bandohanhchinh/" target="_blank" rel="noopener noreferrer">bản đồ hành chính chính thức</a> trước khi nộp.</p><p>Mã phiên bản: ${escapeHTML(geo.source.revision.slice(0,12))}. Không sử dụng cho mục đích đo đạc hoặc địa chính.</p><p>Hình học tham khảo quần đảo Hoàng Sa và Trường Sa: Nguyễn Duy Liêm / <a href="https://github.com/nguyenduy1133/Free-GIS-Data" target="_blank" rel="noopener noreferrer">Free-GIS-Data</a>. Bản đồ không biểu diễn đường biên biển.</p></div><div class="source-item"><strong>Ảnh thực tế dùng tạm cho giao diện</strong><p>Ảnh được thu nhỏ và cắt khung hiển thị; giữ giấy phép của từng ảnh. Chưa phải hình minh họa AI.</p>${credits.map(c=>`<p><a href="${c.source}" target="_blank" rel="noopener noreferrer">${destinationById(legacyIds[c.id] || c.id).name}: ${escapeHTML(c.author)} / Wikimedia Commons</a> · <a class="license" href="${c.licenseUrl}" target="_blank" rel="noopener noreferrer">${c.license}</a></p>`).join('')}</div><div class="source-item"><strong>Hình minh họa AI</strong><p>${Object.values(aiRegions).reduce((sum,region)=>sum+region.images.length,0)} ảnh được tạo bằng API Ban tổ chức cho các địa danh tuyển chọn trong sổ tay. Các ảnh có nhãn minh họa, không phải ảnh tư liệu.</p></div><div class="source-item"><strong>Chatbot</strong><p>Hướng dẫn viên Atlas gợi ý khám phá và trả lời từ kho tư liệu bốn địa phương, có dẫn nguồn. Trạng thái kết nối được hiển thị trong khung trợ lý.</p></div>`); }
function showSaved() {infoDialog.close();dialog.close();if(location.hash==='#/so-tay'){if(geo)render();}else location.hash='/so-tay';}
function notebookCards() {
 const normalized=value=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').toLowerCase();
 let items=[...saved].reverse().map(destinationById).filter(d=>{
  const entry=journal[d.id] || {};
  return (notebookFilter==='all' || (notebookFilter==='visited'?entry.visited:!entry.visited)) && normalized(d.name+' '+(entry.note || '')).includes(normalized(notebookSearch));
 });
 if(notebookSort==='name')items.sort((a,b)=>a.name.localeCompare(b.name,'vi'));
 return items.length?items.map(d=>{
  const entry=journal[d.id] || {}, image=heroImage(d);
  return `<article class="notebook-card" data-notebook-id="${d.id}"><figure><img ${heroAttributes(d)} loading="lazy"><figcaption>${image?'Minh họa do AI tạo':'Ảnh thật · '+escapeHTML(creditFor(d)?.author || 'Wikimedia Commons')}</figcaption></figure><div class="notebook-card-body"><span class="eyebrow">${d.tag}</span><h2><a href="#/dia-phuong/${d.id}">${d.name} ${icon('arrow')}</a></h2><p>${d.description}</p><label class="notebook-visited"><input type="checkbox" data-journal-visited="${d.id}" ${entry.visited?'checked':''}> Đã khám phá</label><label class="notebook-note-label" for="note-${d.id}">Ghi chú của tôi</label><textarea id="note-${d.id}" data-journal-note="${d.id}" rows="3" maxlength="2000" placeholder="Điều bạn muốn tìm hiểu, câu chuyện muốn ghi nhớ…">${escapeHTML(entry.note || '')}</textarea><span class="notebook-note-status" role="status" data-note-status="${d.id}">${entry.note?'Đã lưu ghi chú':'Ghi chú tự lưu khi bạn nhập'}</span><div class="notebook-card-actions"><a class="secondary-button" href="#/dia-phuong/${d.id}">Đọc tiếp ${icon('book')}</a><button class="remove-saved" data-remove-saved="${d.id}" aria-label="Bỏ lưu ${d.name}">Bỏ lưu</button></div></div></article>`;
 }).join(''):`<div class="empty-saved">${icon('bookmark')}<h2>${saved.length?'Chưa tìm thấy mục phù hợp':'Thêm một miền đất vào sổ tay'}</h2><p>${saved.length?'Thử từ khóa khác hoặc chọn “Tất cả”.':'Chọn địa phương bên dưới để bắt đầu ghi lại hành trình khám phá của bạn.'}</p>${saved.length?'<button class="secondary-button" data-notebook-reset>Xóa bộ lọc</button>':'<a class="primary-button" href="#/">Mở bản đồ '+icon('arrow')+'</a>'}</div>`;
}
function notebookView() {
 const visited=saved.filter(id=>journal[id]?.visited).length;
 main.innerHTML=`<div class="detail-shell notebook-shell"><div class="breadcrumb"><a href="#/">${icon('back')} Bản đồ Việt Nam</a><span>/</span><span>Sổ tay của tôi</span></div><header class="notebook-heading"><div><span class="eyebrow">NHỮNG MIỀN ĐẤT & KÝ ỨC</span><h1>Sổ tay của tôi</h1><p>Lưu những miền đất yêu thích, ghi lại điều muốn tìm hiểu và tiếp nối hành trình của bạn.</p></div><button class="secondary-button" data-notebook-export ${saved.length?'':'disabled'}>Tải sổ tay ↓</button></header><div class="notebook-summary"><span><strong>${saved.length}</strong> địa phương đã lưu</span><span><strong>${visited}</strong> đã khám phá</span><span><strong>${saved.length-visited}</strong> muốn khám phá</span></div><p class="notebook-storage">${storageAvailable?'Sổ tay và ghi chú tự lưu trên trình duyệt này.':'Trình duyệt không cho phép lưu. Nội dung chỉ được giữ trong phiên hiện tại.'}</p><div class="notebook-toolbar"><label>Tìm trong sổ tay<input id="notebook-search" type="search" placeholder="Địa phương hoặc ghi chú…" value="${escapeHTML(notebookSearch)}"></label><label>Trạng thái<select id="notebook-filter"><option value="all">Tất cả</option><option value="planned">Muốn khám phá</option><option value="visited">Đã khám phá</option></select></label><label>Sắp xếp<select id="notebook-sort"><option value="recent">Mới lưu trước</option><option value="name">Tên A–Z</option></select></label></div><div class="notebook-grid" id="notebook-results">${notebookCards()}</div><section class="notebook-add"><h2>Thêm miền đất vào sổ tay</h2><p>Chọn một địa phương để lưu và viết ghi chú riêng.</p><div>${destinations.map(d=>`<button class="secondary-button" data-save="${d.id}" aria-pressed="${saved.includes(d.id)}" ${saved.includes(d.id)?'disabled':''}>${icon(saved.includes(d.id)?'check':'bookmark')}${d.name}${saved.includes(d.id)?' · Đã lưu':''}</button>`).join('')}</div></section></div>`;
 $('#notebook-filter').value=notebookFilter;$('#notebook-sort').value=notebookSort;
}
function exportNotebook() {
 const text=['SỔ TAY CỦA TÔI · ATLAS VIỆT','',...saved.map(id=>{const d=destinationById(id),entry=journal[id] || {};return `${d.name} — ${entry.visited?'Đã khám phá':'Muốn khám phá'}\n${entry.note || 'Chưa có ghi chú.'}\n`;})].join('\n');
 const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));
 const link=document.createElement('a');link.href=url;link.download='so-tay-atlas-viet.txt';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function notFound() { main.innerHTML=`<div class="error-box"><span class="eyebrow">NGOÀI PHẠM VI SỔ TAY</span><h2>Chưa có câu chuyện ở đây</h2><p>Sổ tay hiện có ${scopeLabel}.</p><a class="primary-button" href="#/">Trở về bản đồ ${icon('arrow')}</a></div>`; }
function render() {
 if(!geo)return;
 disposeOnlineTour();
 const [path,query='']=(location.hash.slice(1)||'/').split('?');
 if(path==='/'||path===''){document.title='Atlas Việt — Mỗi miền đất, một câu chuyện';homeView();}
 else if(path==='/so-tay'){document.title='Sổ tay của tôi — Atlas Việt';notebookView();}
 else {const match=path.match(/^\/dia-phuong\/([a-z-]+)\/?$/);if(match){const canonical=legacyIds[match[1]];if(canonical){location.replace('#/dia-phuong/'+canonical+(query?'?'+query:''));return;}detailView(match[1],new URLSearchParams(query));const d=destinationById(match[1]);document.title=d?d.name+' — Atlas Việt':'Ngoài phạm vi — Atlas Việt';}else notFound();}
 $('.nav-explore').classList.toggle('active',path==='/');
 $('#saved-nav').classList.toggle('active',path==='/so-tay');
 if(path==='/so-tay')$('#saved-nav').setAttribute('aria-current','page');else $('#saved-nav').removeAttribute('aria-current');
}
document.addEventListener('click',event=>{
 const target=event.target.closest('button,a,[data-open],[data-province]');if(!target)return;
 if(target.dataset.open){openDestination(target.dataset.open);}
 if(target.dataset.province){const d=destinations.find(d=>d.province===Number(target.dataset.province));if(d)openDestination(d.id);else notify(target.dataset.name+' chưa nằm trong phạm vi sổ tay.');}
 if(target.dataset.aiImage)openImage(destinationById(target.dataset.aiDestination),target.dataset.aiImage);
 if(target.dataset.save)toggleSaved(target.dataset.save);
 if(target.dataset.tab){location.hash=`/dia-phuong/${target.dataset.destination}?tab=${target.dataset.tab}`;}
 if(target.hasAttribute('data-tour-start')||target.hasAttribute('data-tour-retry'))startOnlineTour();
 if(target.hasAttribute('data-tour-select'))selectTourScene(Number(target.dataset.tourSelect));
 if(target.hasAttribute('data-tour-stop'))stopOnlineTour();
 if(target.hasAttribute('data-tour-fullscreen')){const stage=$('#tour-stage');if(stage?.requestFullscreen)stage.requestFullscreen().catch(()=>notify('Không thể mở toàn màn hình. Bạn vẫn có thể xem tour trong khung hiện tại.'));else notify('Trình duyệt này chưa hỗ trợ toàn màn hình.');}
 if(target.hasAttribute('data-close-info'))dismissDialog(infoDialog);
 if(target.hasAttribute('data-sources'))showSources();
 if(target.dataset.removeSaved){const id=target.dataset.removeSaved;toggleSaved(id);const next=$('[data-remove-saved]') || $('#notebook-search');next?.focus();}
 if(target.hasAttribute('data-notebook-export'))exportNotebook();
 if(target.hasAttribute('data-notebook-reset')){notebookSearch='';notebookFilter='all';notebookView();$('#notebook-search').focus();}
});
document.addEventListener('keydown',event=>{
 const target=event.target;
 if((event.key==='Enter'||event.key===' ')&&target.matches('g[role=button]')){event.preventDefault();target.dispatchEvent(new MouseEvent('click',{bubbles:true}));}
 if(target.matches('[role=tab]')&&['ArrowLeft','ArrowRight','Home','End'].includes(event.key)){
  event.preventDefault();const buttons=$$('[role=tab]');const index=buttons.indexOf(target);const next=event.key==='Home'?0:event.key==='End'?buttons.length-1:(index+(event.key==='ArrowRight'?1:-1)+buttons.length)%buttons.length;buttons[next].click();setTimeout(()=>$$('[role=tab]')[next]?.focus(),0);
 }
});
dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dismissDialog(dialog);}});
infoDialog.addEventListener('click',event=>{if(event.target===infoDialog){const r=infoDialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dismissDialog(infoDialog);}});
$('#saved-nav').onclick=showSaved;
$('#sources-footer').onclick=showSources;
$('#about-nav').onclick=()=>openInfo('Mỗi miền đất, một câu chuyện',`<p>Atlas Việt là bản mẫu sổ tay điện tử Dư địa chí dành cho người muốn tìm hiểu địa lý, lịch sử và văn hóa qua bản đồ tương tác.</p><p><strong>Phạm vi:</strong> ${scopeLabel}.</p><p>Phiên bản này hoàn thiện luồng khám phá. Hướng dẫn viên Atlas giúp gợi ý hành trình, tìm tư liệu và trả lời có nguồn. Hình minh họa AI đã có trong các bộ ảnh địa phương. Bài viết địa phương được biên soạn từ kho tư liệu, có dẫn nguồn cho từng phần và hồ sơ địa danh.</p><p>Thông tin được biên soạn cần có nguồn dẫn, mốc đối chiếu và sự tôn trọng văn hóa địa phương. Những mục chưa xác minh phải được đánh dấu rõ.</p><button class="secondary-button" data-sources>Xem nguồn dữ liệu ${icon('arrow')}</button>`);
$('#chat-toggle').onclick=()=>{const panel=$('#chat-panel');panel.hidden=!panel.hidden;$('#chat-toggle').setAttribute('aria-expanded',String(!panel.hidden));};
$('#chat-close').onclick=()=>{$('#chat-panel').hidden=true;$('#chat-toggle').setAttribute('aria-expanded','false');$('#chat-toggle').focus();};

createProvinceHints(destinations);
window.addEventListener('hashchange',render);
installMotion();
updateSavedCount();
try {
 const responses=await Promise.all([fetch('assets/vietnam-provinces.geojson'),fetch('assets/credits.json')]);
 if(responses.some(r=>!r.ok))throw new Error('Không thể tải dữ liệu bản đồ.');
 [geo,credits]=await Promise.all(responses.map(r=>r.json()));
 const articles=await fetch('assets/articles.json');
 if(!articles.ok)throw new Error('Không thể tải bài viết địa phương.');
 articleRegions=(await articles.json()).regions;
 try { const media=await fetch('assets/ai-images.json',{cache:'no-store'});if(media.ok)aiRegions=(await media.json()).regions || {}; } catch { /* Keep the map and credited photos available without an optional media index. */ }
 render();
}catch(error){main.innerHTML=`<div class="error-box"><h2>Bản đồ chưa tải được</h2><p>${escapeHTML(error.message)}</p><p>Hãy mở website qua máy chủ HTTP và tải lại trang.</p><button class="primary-button" onclick="location.reload()">Thử lại</button></div>`;}

window.addEventListener('pagehide',()=>stopTourNarration());

document.addEventListener('input',event=>{
 const target=event.target;
 if(target.id==='notebook-search'){notebookSearch=target.value;$('#notebook-results').innerHTML=notebookCards();}
 if(target.dataset.journalNote){
  const id=target.dataset.journalNote;if(!saved.includes(id))return;
  journal[id]={...journal[id],note:target.value};
  const ok=persistNotebook();$('[data-note-status="'+id+'"]').textContent=ok?'Đã lưu ghi chú':'Ghi chú đang giữ trong phiên này';
 }
});
document.addEventListener('change',event=>{
 const target=event.target;
 if(target.id==='notebook-filter'){notebookFilter=target.value;$('#notebook-results').innerHTML=notebookCards();}
 if(target.id==='notebook-sort'){notebookSort=target.value;$('#notebook-results').innerHTML=notebookCards();}
 if(target.dataset.journalVisited){const id=target.dataset.journalVisited;if(!saved.includes(id))return;journal[id]={...journal[id],visited:target.checked};persistNotebook();notebookView();$('[data-journal-visited="'+id+'"]')?.focus();}
});
