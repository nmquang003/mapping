"""Verify actual local speech files, chapters and media lifecycle."""
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
BASE=os.environ.get('ATLAS_TEST_URL','http://127.0.0.1:4321/').rstrip('/')+'/'
QA=Path(__file__).resolve().parents[1]/'.qa'

async def main():
 QA.mkdir(exist_ok=True)
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(args=['--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
  page=await browser.new_page(viewport={'width':1440,'height':1000})
  errors=[];external=[];audio_requests=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  async def route(r):
   url=r.request.url
   if not url.startswith(BASE) and not url.startswith('data:'):
    external.append(url);await r.abort()
   else:
    if '/audio/' in url:audio_requests.append(url)
    await r.continue_()
  await page.route('**/*',route)
  await page.route('**/api/status',lambda r:r.fulfill(status=503,json={'error':'API unavailable; narration works offline'}))
  for region in ['ninh-binh','ha-noi','quang-ninh','lao-cai']:
   await page.goto(BASE+f'#/dia-phuong/{region}?tab=du-lich',wait_until='networkidle')
   assert await page.locator('#tour-audio').count()==0
   assert not any('/peaceful-tour.mp3' in u for u in audio_requests)
   await page.locator('[data-tour-start]').click()
   await page.wait_for_function('document.querySelector("#tour-audio")?.currentTime>0')
   assert not await page.locator('#tour-audio').evaluate('(a)=>a.loop')
   assert await page.locator('#narration-chapter option').count()==4
   for index in range(4):
    await page.select_option('#narration-chapter',str(index))
    await page.wait_for_function('document.querySelector("#tour-audio").currentTime>0 && document.querySelector("#tour-audio").duration>20')
    assert await page.locator('#narration-text').text_content()
    assert await page.locator('#narration-sources a').count()>0
    assert float(await page.locator('#narration-progress').get_attribute('max'))>20
   await page.locator('[data-narration-toggle]').click()
   assert await page.locator('#tour-audio').evaluate('(a)=>a.paused')
   await page.select_option('#narration-chapter','1')
   assert await page.locator('#tour-audio').evaluate('(a)=>a.paused')
   await page.locator('[data-narration-toggle]').click()
   await page.wait_for_function('document.querySelector("#tour-audio").currentTime>0')
   await page.locator('[data-narration-restart]').click()
   assert await page.locator('#tour-audio').evaluate('(a)=>a.currentTime<2 && !a.paused')
   # Reach the real media end; the next chapter should start automatically.
   await page.locator('#tour-audio').evaluate('(a)=>{a.playbackRate=16;}')
   await page.wait_for_function('document.querySelector("#narration-chapter").value==="2" && document.querySelector("#tour-audio").currentTime>0')
   await page.select_option('#narration-chapter','3')
   await page.wait_for_function('document.querySelector("#tour-audio").currentTime>0')
   await page.locator('#tour-audio').evaluate('(a)=>{a.playbackRate=16;}')
   await page.wait_for_function('document.querySelector("#tour-audio").ended')
   assert 'Đã nghe hết' in await page.locator('#narration-status').inner_text()
   await page.locator('[data-narration-toggle]').click()
   await page.wait_for_function('document.querySelector("#narration-chapter").value==="0" && document.querySelector("#tour-audio").currentTime>0')
   await page.locator('#tour-audio').evaluate('(a)=>{a.playbackRate=1;}')
   if region=='ninh-binh':
    await page.locator('.narration-transcript summary').click()
    await page.screenshot(path=str(QA/'narration-desktop.png'),full_page=True)
   await page.evaluate('window.oldNarration=document.querySelector("#tour-audio")')
   await page.locator('[data-tour-stop]').click()
   assert await page.evaluate('window.oldNarration.paused && !window.oldNarration.hasAttribute("src")')
  assert len(set(audio_requests))>=16
  mobile=await browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
  await mobile.route('**/api/status',lambda r:r.fulfill(status=503,json={'error':'Offline'}))
  await mobile.goto(BASE+'#/dia-phuong/lao-cai?tab=du-lich',wait_until='networkidle')
  await mobile.locator('[data-tour-start]').click()
  await mobile.wait_for_function('document.querySelector("#tour-audio").currentTime>0')
  await mobile.select_option('#narration-chapter','2')
  await mobile.locator('.narration-transcript summary').click()
  assert await mobile.evaluate('document.documentElement.scrollWidth<=innerWidth')
  await mobile.screenshot(path=str(QA/'narration-mobile.png'),full_page=True)
  await mobile.evaluate('window.oldNarration=document.querySelector("#tour-audio")')
  await mobile.locator('[data-tab=lich-su]').click()
  await mobile.wait_for_function('!document.querySelector("#tour-audio")')
  assert await mobile.evaluate('window.oldNarration.paused')
  assert not errors,errors
  assert not external,external
  await browser.close()
 print('PASS: 16 actual narration MP3s, chapters and source transcripts, progress/replay, pause preservation, automatic next/end, lazy loading, lifecycle, desktop/mobile, no API dependency.')

asyncio.run(main())
