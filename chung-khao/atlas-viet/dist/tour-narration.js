import { narrations } from './narration-catalog.js';
const preferences={enabled:true,volume:.75};

export function narrationView() {
 return `<div class="tour-music" id="tour-audio-controls" hidden><button class="secondary-button" data-narration-toggle aria-pressed="false">Bật thuyết minh</button><label for="tour-volume">Âm lượng</label><input id="tour-volume" type="range" min="0" max="100" step="1" value="${Math.round(preferences.volume*100)}" aria-label="Âm lượng thuyết minh"><span id="narration-status" role="status" aria-live="polite">Thuyết minh tiếng Việt · Giọng đọc AI</span></div>`;
}

export function createNarration(region, section) {
 const chapters=narrations[region].chapters, root=section.querySelector('#tour-audio-controls');
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
  button.textContent=playing?'Tắt thuyết minh':audio.ended?'Nghe lại thuyết minh':'Bật thuyết minh';
  button.setAttribute('aria-pressed',String(playing));
 };
 const play=()=>{
  const token=++playToken;
  if(audio.error)audio.load();
  audio.play().then(()=>{
   if(disposed||token!==playToken)return;
   if(!preferences.enabled){audio.pause();return;}
   status('Thuyết minh tiếng Việt · Giọng đọc AI');update();
  }).catch(error=>{
   if(disposed||token!==playToken||error.name==='AbortError')return;
   status(error.name==='NotAllowedError'?'Bấm Bật thuyết minh để nghe.':'Chưa tải được thuyết minh. Bấm Bật thuyết minh để thử lại.');update();
  });
 };
 const select=(next,shouldPlay=preferences.enabled)=>{
  ++playToken;audio.pause();index=next;audio.src=chapters[index].src;update();
  if(shouldPlay)play();
 };
 listen(audio,'playing',update);listen(audio,'pause',update);
 listen(audio,'ended',()=>{
  if(disposed)return;
  if(preferences.enabled&&index<chapters.length-1)select(index+1,true);
  else {status('Đã nghe hết thuyết minh.');update();}
 });
 listen(audio,'error',()=>{
  if(disposed)return;
  status('Chưa tải được thuyết minh. Bấm Bật thuyết minh để thử lại.');update();
 });
 listen($('[data-narration-toggle]'),'click',()=>{
  if(!audio.paused){preferences.enabled=false;++playToken;audio.pause();status('Đã tắt thuyết minh.');}
  else {preferences.enabled=true;if(audio.ended)select(0,true);else play();}
 });
 listen($('#tour-volume'),'input',event=>{preferences.volume=Number(event.target.value)/100;audio.volume=preferences.volume;});
 select(0,false);
 return {
  start:()=>{root.hidden=false;if(preferences.enabled&&!audio.ended)play();},
  destroy:()=>{disposed=true;++playToken;events.abort();audio.pause();audio.removeAttribute('src');audio.load();audio.remove();root.hidden=true;}
 };
}
