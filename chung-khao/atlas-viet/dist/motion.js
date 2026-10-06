const reducedMotion=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
// Keep native dialog focus/keyboard behavior while giving explicit dismissal a short exit.
export function dismissDialog(dialog) {
 if(!dialog.open || dialog.dataset.dismissing)return;
 if(reducedMotion()){dialog.close();return;}
 dialog.dataset.dismissing='true';
 const animation=dialog.animate([{opacity:1,transform:'translateY(0) scale(1)'},{opacity:0,transform:'translateY(10px) scale(.985)'}],{duration:150,easing:'ease-in',fill:'forwards'});
 animation.finished.then(()=>{dialog.close();animation.cancel();delete dialog.dataset.dismissing;});
}
export function installMotion() {
 for(const dialog of document.querySelectorAll('dialog')){
  dialog.addEventListener('cancel',event=>{event.preventDefault();dismissDialog(dialog);});
 }
 document.addEventListener('pointerdown',event=>{
  if(reducedMotion())return;
  const button=event.target.closest('.primary-button,.secondary-button,.map-controls button,#focus-north');
  if(!button || button.disabled)return;
  const rect=button.getBoundingClientRect(),size=Math.max(rect.width,rect.height)*2;
  const ripple=document.createElement('span');ripple.className='tap-ripple';ripple.setAttribute('aria-hidden','true');
  Object.assign(ripple.style,{width:size+'px',height:size+'px',left:event.clientX-rect.left-size/2+'px',top:event.clientY-rect.top-size/2+'px'});
  button.append(ripple);ripple.addEventListener('animationend',()=>ripple.remove(),{once:true});
 });
}
