// Reading views use local sourced material; source IDs remain scoped to a region.
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const link = source => `<a href="${esc(source.url)}" target="_blank" rel="noopener noreferrer">${esc(source.title)} ↗</a>`;
const citations = (region, ids) => `<p class="article-citations">Nguồn: ${[...new Set(ids)].map(id => region.sources[id]).filter(Boolean).map(link).join(' · ')}</p>`;
const sectionImages = {
 'ninh-binh':['trang-an','cuc-phuong','hoa-lu','phat-diem','tam-coc','hang-mua'],
 'ha-noi':['pho-co-ha-noi','hoang-thanh-thang-long','van-mieu-quoc-tu-giam','bao-tang-dan-toc-hoc','pho-co-ha-noi','nha-hat-lon-ha-noi'],
 'quang-ninh':['vinh-ha-long','vinh-bai-tu-long','yen-tu','quan-lan','co-to','thanh-lan'],
 'lao-cai':['sa-pa','mu-cang-chai','ho-thac-ba','ngoi-tu','ngoi-tu','khau-pha']
};
const section = (region, item, image, index) => `<section class="reading-section story-row${image?'':' text-only'}" data-reveal><div class="story-media">${image}</div><div class="story-copy"><span class="eyebrow">${String(index+1).padStart(2,'0')} · ${esc(region.name)}</span><h3>${esc(item.title)}</h3><p>${esc(item.text)}</p>${citations(region, item.source_ids)}</div></section>`;
export function overviewView(region, image = '') {
 const overview=region?.overview;
 if(!overview)return '';
 return `<article class="regional-overview" aria-label="Tổng quan ${esc(region.name)}"><header><span class="eyebrow">TỔNG QUAN ĐỊA PHƯƠNG</span><h2>${esc(region.title)}</h2>${image}<p class="article-lead">${esc(overview.lead)}</p></header><div class="overview-topics">${overview.sections.map(item=>`<section><h3>${esc(item.title)}</h3><p>${esc(item.text)}</p>${citations(region,item.source_ids)}</section>`).join('')}</div><section class="overview-landmarks"><h3>Năm địa danh đại diện</h3><ul>${overview.representatives.map(item=>`<li><strong>${esc(item.name)}</strong> — ${esc(item.text)}</li>`).join('')}</ul>${citations(region,overview.representatives.flatMap(item=>item.source_ids))}</section><p class="reading-note">Phạm vi và nội dung tổng quan được đối chiếu ngày ${esc(region.overviewReviewedOn)}.</p></article>`;
}
export function articleView(d, tab, regions, placeImage) {
 const r = regions[d.id];
 if (!r || ['bo-anh','du-lich'].includes(tab)) return null;
 if (tab === 'dia-danh') return `<div class="section-heading"><h2>Những địa danh kể chuyện</h2><span>${r.places.length} hồ sơ địa danh</span></div><div class="place-grid reading-places">${r.places.map((p,i)=>`<article class="place-card story-row${placeImage(d,p.id)?'':' text-only'}" data-reveal data-place-card="${p.id}"><div class="story-media">${placeImage(d,p.id)}</div><div class="story-copy"><span class="eyebrow">ĐỊA DANH ${String(i+1).padStart(2,'0')}</span><h3>${esc(p.name)}</h3><p>${esc(p.summary)}</p>${p.facts.map(f=>`<p>${esc(f.text)}</p>${citations(r,f.source_ids)}`).join('')}${p.highlights?.length?`<h4>Điểm nhấn</h4><ul>${p.highlights.map(h=>`<li>${esc(h)}</li>`).join('')}</ul>`:''}${citations(r,p.source_ids)}<button class="secondary-button" data-ask-atlas="${esc(p.name)}" data-chat-province="${d.id}">✧ Hỏi Atlas về địa danh này</button></div></article>`).join('')}</div>`;
 if (tab === 'nguon') return `<div class="section-heading"><h2>Tư liệu cho bài viết ${esc(r.name)}</h2><span>Đối chiếu trong kho: ${esc(r.researchedOn)}</span></div><p class="reading-note">Nguồn được dẫn ngay dưới từng đoạn và hồ sơ địa danh. Ảnh AI là hình minh họa; nguồn bài viết không xác nhận các chi tiết trong ảnh. Tên địa phương và số liệu trong tư liệu được đọc theo mốc thời gian của nguồn.</p>${Object.values(r.sources).map(s=>`<div class="source-item"><strong>${esc(s.publisher)}</strong><p>${link(s)}</p><p>Ngày đọc nguồn trong kho tư liệu: ${esc(s.accessed_on)}${s.displayed_date?` · Ngày nguồn ghi: ${esc(s.displayed_date)}`:''}</p>${s.note?`<p>${esc(s.note)}</p>`:''}</div>`).join('')}`;
 const selected = tab==='lich-su' ? [r.sections[2]] : tab==='van-hoa' ? r.sections.slice(3,5) : [r.sections[0],r.sections[1],r.sections[5]];
 const title = tab==='lich-su' ? `Dấu xưa trong câu chuyện ${r.name}` : tab==='van-hoa' ? `Văn hóa và hương vị ${r.name}` : r.title;
 return `<article class="regional-article"><header><span class="eyebrow">SỔ TAY ${esc(r.name).toUpperCase()}</span><h2>${esc(title)}</h2>${tab==='tong-quan'?`<p class="article-lead">${esc(r.lead)}</p>`:''}</header>${selected.map((s,i)=>section(r,s,placeImage(d,sectionImages[d.id]?.[r.sections.indexOf(s)]),i)).join('')}<footer class="reading-note">Tư liệu được đọc ngày ${esc(r.researchedOn)}. Giờ mở cửa, giá vé và lịch hoạt động cần được kiểm tra với đơn vị quản lý trước chuyến đi.</footer><a class="secondary-button" href="#/dia-phuong/${d.id}?tab=dia-danh">Đọc ${r.places.length} hồ sơ địa danh →</a></article>`;
}

let revealObserver;
let focusRoot;
const revealFocused = event => event.target.closest('.reveal-ready')?.classList.add('is-visible');
export function animateReading(root) {
 revealObserver?.disconnect();
 focusRoot?.removeEventListener('focusin',revealFocused);
 const rows=[...root.querySelectorAll('[data-reveal], .gallery-item')];
 if(matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window))return;
 revealObserver=new IntersectionObserver(entries=>{
  for(const entry of entries){
   if(entry.isIntersecting){entry.target.classList.add('is-visible');revealObserver.unobserve(entry.target);}
  }
 },{threshold:0,rootMargin:'0px 0px -32px 0px'});
 for(const row of rows){row.classList.add('reveal-ready');revealObserver.observe(row);}
 // Keyboard focus should immediately reveal an offscreen or still-animating row.
 focusRoot=root;
 root.addEventListener('focusin',revealFocused);
}
