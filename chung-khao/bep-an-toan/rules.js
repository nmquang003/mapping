export const FOODS={chicken:{name:'Gà nướng',icon:'🍗',raw:'Gà sống'},salad:{name:'Salad rau',icon:'🥗',raw:'Rau chưa rửa'},fruit:{name:'Trái cây',icon:'🍉',raw:'Quả chưa rửa'}};
export const LEVELS=[{name:'Gian hàng đầu tiên',subtitle:'Làm quen với bếp, vệ sinh và món gà nướng.',icon:'🌱',duration:150,target:4,menu:['chicken'],interval:29,patience:100,event:null},{name:'Bữa trưa rộn ràng',subtitle:'Thêm salad, tách sống – chín và phối hợp cùng Nam.',icon:'☀️',duration:180,target:6,menu:['chicken','salad'],interval:23,patience:95,event:'water'},{name:'Giải cứu hội chợ',subtitle:'Ba món, tủ lạnh trục trặc và khách đến liên tục.',icon:'🎪',duration:210,target:8,menu:['chicken','salad','fruit'],interval:20,patience:90,event:'fridge'}];
export const COOK_SECONDS=10;
export const HANDWASH_SECONDS=2;
export const MAX_EXPOSURE=50; // accelerated gameplay clock, never a real-world storage limit
export function createItem(kind){return {kind,stage:'raw',contaminated:false,verified:false,exposure:0};}
export function isRawMeat(item){return item?.kind==='chicken'&&['raw','cut'].includes(item.stage);}
export function touchFood(item,dirtyHands){if(dirtyHands&&!isRawMeat(item))item.contaminated=true;return isRawMeat(item)||dirtyHands;}
export function prepareItem(item,boardDirty){if(item.stage!=='washed'&&item.kind!=='chicken')return {ok:false,reason:'wash'};if(item.kind==='chicken'){item.stage='cut';return {ok:true,boardDirty:true};}if(boardDirty)item.contaminated=true;item.stage='ready';return {ok:true,boardDirty};}
export function cookItem(item){item.stage='cooked';item.contaminated=false;item.verified=false;return item;}
export function foodRisk(item){if(item.exposure>=MAX_EXPOSURE)return 'storage';if(item.contaminated)return 'cross';if(item.kind==='chicken'&&(item.stage!=='cooked'||!item.verified))return 'cook';if(item.kind!=='chicken'&&item.stage!=='ready')return 'prepare';return null;}
export function starsFor(served,target,mistakes){if(served<target)return 0;if(mistakes===0&&served>=target+2)return 3;return mistakes<=1?2:1;}
export function seededRandom(seed){let a=seed>>>0;return()=>{a+=0x6D2B79F5;let t=a;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return ((t^t>>>14)>>>0)/4294967296;};}
