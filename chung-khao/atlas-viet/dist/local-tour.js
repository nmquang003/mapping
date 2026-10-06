// Pannellum 2.5.6 is vendored locally; panorama requests stay on this origin.
export function createLocalTour(container, metadata, titles, firstIndex, callbacks) {
 const quality=matchMedia('(max-width: 760px)').matches?'mobile':'hi';
 const scenes={};
 metadata.scenes.forEach((scene,index)=>{
  const view=scene.view;
  const spherical=scene.projection==='equirectangular';
  const asset=path=>new URL(`assets/360/${path}`,document.baseURI).href;
  scenes[scene.id]={
   type:spherical?'equirectangular':'cubemap',title:titles[index],
   ...(spherical?{panorama:asset(scene.panorama[quality]),ignoreGPanoXMP:true}:{
    cubeMap:['f','r','b','l','u','d'].map(face=>asset(scene.variants[quality][face]))}),
   yaw:spherical?view.yaw:((Number(view.hlookat)+180)%360+360)%360-180,
   pitch:spherical?view.pitch:-Number(view.vlookat),hfov:spherical?view.hfov:Number(view.fov),
   minHfov:spherical?45:Number(view.fovmin),maxHfov:spherical?120:Number(view.fovmax),
   hotSpots:scene.hotspots.filter(h=>metadata.scenes.some(s=>s.id===h.linkedscene)).map(h=>({
    type:'scene',sceneId:h.linkedscene,yaw:spherical?h.yaw:Number(h.ath),pitch:spherical?h.pitch:-Number(h.atv),
    text:titles[metadata.scenes.findIndex(s=>s.id===h.linkedscene)]
   }))
  };
 });
 const viewer=window.pannellum.viewer(container,{
  default:{firstScene:metadata.scenes[firstIndex].id,autoLoad:true,escapeHTML:true,
   showFullscreenCtrl:false,mouseZoom:'fullscreenonly',sceneFadeDuration:250,
   strings:{loadingLabel:'Đang tải cảnh…',loadButtonLabel:'Mở cảnh 360°',
    bylineLabel:'%s',noWebGLError:'Thiết bị chưa hỗ trợ hiển thị 360°.',
    fileAccessError:'Không tải được ảnh panorama. Hãy thử lại.',
    genericWebGLError:'Không thể hiển thị cảnh 360°. Hãy thử lại.'}},scenes
 });
 viewer.on('scenechange',id=>callbacks.change(metadata.scenes.findIndex(s=>s.id===id)));
 viewer.on('load',()=>callbacks.load());
 viewer.on('error',()=>callbacks.error());
 const observer=new ResizeObserver(()=>viewer.resize());observer.observe(container);
 return {
  select:index=>viewer.loadScene(metadata.scenes[index].id),
  destroy:()=>{observer.disconnect();viewer.destroy();}
 };
}
