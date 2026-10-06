import { narrations } from './narration-catalog.js';
const escapeHTML=value=>String(value).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const preferences={enabled:true,volume:.75};
const clock=seconds=>`${Math.floor(seconds/60)}:${String(Math.floor(seconds%60)).padStart(2,'0')}`;

export function narrationView(region) {
 const chapters=narrations[region].chapters;
 return `<section class="tour-narration" id="tour-narration" aria-label="Thuyết minh địa phương" hidden>
 <div class="narration-heading"><div><h3>Nghe Atlas thuyết minh</h3><p>Bốn phần, tự chuyển tiếp · Giọng đọc tổng hợp tiếng Việt</p></div><label for="narration-chapter">Chọn chủ đề<select id="narration-chapter">${chapters.map((chapter,index)=>`<option value="${index}">${index+1}. ${escapeHTML(chapter.title)}</option>`).join('')}</select></label></div>
 <div class="narration-controls"><button class="secondary-button" data-narration-toggle aria-pressed="false">Nghe thuyết minh</button><button class="secondary-button" data-narration-restart>Nghe lại phần này</button><label for="narration-volume">Âm lượng</label><input id="narration-volume" type="range" min="0" max="100" value="${Math.round(preferences.volume*100)}" aria-label="Âm lượng thuyết minh"></div>
 <div class="narration-progress"><span id="narration-time">0:00</span><progress id="narration-progress" max="1" value="0" aria-label="Tiến độ thuyết minh"></progress><span id="narration-duration">0:00</span></div>
 <p id="narration-status" role="status" aria-live="polite">Thuyết minh sẽ bắt đầu cùng tour.</p>
 <details class="narration-transcript"><summary>Đọc lời thuyết minh và nguồn</summary><h4 id="narration-title"></h4><p id="narration-text"></p><ul id="narration-sources"></ul></details></section>`;
}

export function createNarration(region, section) {
 const chapters=narrations[region].chapters, root=section.querySelector('#tour-narration');
 const $=selector=>root.querySelector(selector);
 const events=new AbortController();
 const audio=document.createElement('audio');audio.id='tour-audio';audio.preload='none';
 audio.volume=preferences.volume;audio.loop=false;section.append(audio);
 let index=0,disposed=false,playToken=0;
 const listen=(node,event,callback)=>node.addEventListener(event,callback,{signal:events.signal});
 const status=text=>{$('#narration-status').textContent=text;};
 const update=()=>{
  const playing=!audio.paused&&!audio.ended;
  const button=$('[data-narration-toggle]');
  button.textContent=playing?'Tạm dừng':audio.ended?'Nghe lại thuyết minh':'Nghe thuyết minh';
  button.setAttribute('aria-pressed',String(playing));
 };
 const progress=()=>{
  const duration=Number.isFinite(audio.duration)?audio.duration:0;
  $('#narration-progress').max=duration||1;
  $('#narration-progress').value=audio.currentTime;
  $('#narration-time').textContent=clock(audio.currentTime);
  $('#narration-duration').textContent=clock(duration||chapters[index].duration);
 };
 const play=()=>{
  const token=++playToken;
  if(audio.error)audio.load();
  audio.play().then(()=>{
   if(disposed||token!==playToken)return;
   if(!preferences.enabled){audio.pause();return;}
   status(`Đang nghe: ${chapters[index].title}`);update();
  }).catch(error=>{
   if(disposed||token!==playToken||error.name==='AbortError')return;
   status(error.name==='NotAllowedError'?'Bấm Nghe thuyết minh để bắt đầu.':'Chưa tải được thuyết minh. Bấm Nghe thuyết minh để thử lại hoặc chọn phần khác.');update();
  });
 };
 const select=(next,shouldPlay=preferences.enabled)=>{
  ++playToken;audio.pause();index=next;audio.src=chapters[index].src;
  $('#narration-chapter').value=String(index);
  $('#narration-title').textContent=chapters[index].title;
  $('#narration-text').textContent=chapters[index].text;
  $('#narration-sources').replaceChildren(...chapters[index].sources.map(source=>{
   const li=document.createElement('li'),link=document.createElement('a');
   link.textContent=source.title;link.href=source.url;link.target='_blank';link.rel='noopener noreferrer';li.append(link);return li;
  }));
  status(`Đã chọn: ${chapters[index].title}`);progress();update();
  if(shouldPlay)play();
 };
 listen(audio,'playing',update);listen(audio,'pause',update);
 listen(audio,'loadedmetadata',progress);listen(audio,'timeupdate',progress);
 listen(audio,'ended',()=>{
  if(disposed)return;
  if(preferences.enabled&&index<chapters.length-1)select(index+1,true);
  else {status('Đã nghe hết thuyết minh. Bạn có thể nghe lại hoặc chọn một chủ đề.');update();}
 });
 listen(audio,'error',()=>{
  if(disposed)return;
  status('Chưa tải được thuyết minh. Bấm Nghe thuyết minh để thử lại hoặc chọn phần khác.');update();
 });
 listen($('[data-narration-toggle]'),'click',()=>{
  if(!audio.paused){preferences.enabled=false;++playToken;audio.pause();status(`Đã tạm dừng: ${chapters[index].title}`);}
  else {preferences.enabled=true;if(audio.ended)select(0,true);else play();}
 });
 listen($('[data-narration-restart]'),'click',()=>{preferences.enabled=true;audio.currentTime=0;play();});
 listen($('#narration-chapter'),'change',event=>select(Number(event.target.value)));
 listen($('#narration-volume'),'input',event=>{preferences.volume=Number(event.target.value)/100;audio.volume=preferences.volume;});
 select(0,false);
 return {
  start:()=>{root.hidden=false;if(preferences.enabled)play();},
  destroy:()=>{disposed=true;++playToken;events.abort();audio.pause();audio.removeAttribute('src');audio.load();audio.remove();root.hidden=true;}
 };
}
