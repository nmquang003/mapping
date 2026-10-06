const {chromium}=require('playwright');
const fs=require('fs');
const assert=require('assert');
(async()=>{
 const browser=await chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const root=require('path').resolve(__dirname,'..');const base=process.env.ATLAS_BASE_URL || 'http://127.0.0.1:4321/';fs.mkdirSync(root+'/.qa',{recursive:true});
 for(const [slug,count] of [['ninh-binh',7],['ha-noi',8],['quang-ninh',7],['lao-cai',7]]){
  for(const tab of ['dia-danh','lich-su','van-hoa','nguon','bo-anh','du-lich']){
   await page.goto(`${base}#/dia-phuong/${slug}?tab=${tab}`,{waitUntil:'networkidle'});
   await page.locator('#tab-content').waitFor();
   if(tab==='dia-danh'){assert.equal(await page.locator('.place-card').count(),count);assert(await page.locator('.article-citations').count()>=count);}
   if(['lich-su','van-hoa'].includes(tab)){assert.equal(await page.locator('.regional-article').count(),1);assert(await page.locator('.article-citations').count()>0);}
   for(const img of await page.locator('img:visible').all()){await img.scrollIntoViewIfNeeded();await img.evaluate(i=>i.decode());}
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),slug+' '+tab);
  }
  console.log('PASS',slug,count,'profiles; all tabs, images, citations');
 }
 for(const width of [1440,390]){
  await page.setViewportSize({width,height:1000});
  for(const tab of ['dia-danh','bo-anh']){
   await page.goto(base+'#/dia-phuong/ninh-binh?tab='+tab,{waitUntil:'networkidle'});
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),width+' '+tab);
   for(const img of await page.locator('img:visible').all()){await img.scrollIntoViewIfNeeded();await img.evaluate(i=>i.decode());}
   await page.screenshot({path:root+`/.qa/articles-${width}-${tab}.png`,fullPage:true});
  }
  await page.goto(base,{waitUntil:'networkidle'});
  assert.equal(await page.locator('.card-caption').count(),4);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'home '+width);
  await page.screenshot({path:root+`/.qa/articles-${width}-home.png`,fullPage:true});
 }
 assert.deepEqual(errors,[]);console.log('PASS desktop/mobile layouts; no browser errors');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
