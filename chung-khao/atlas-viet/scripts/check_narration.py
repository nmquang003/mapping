"""Verify compact tour controls and sequential playback of all 16 real MP3s."""
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
   assert await page.locator('#tour-audio-controls').is_hidden()
   assert await page.locator('#tour-narration, #narration-chapter, .narration-transcript, #narration-progress').count()==0
   assert 'Nghe Atlas thuyết minh' not in await page.locator('body').inner_text()
   assert not any('/peaceful-tour.mp3' in u for u in audio_requests)
   await page.locator('[data-tour-start]').click()
   await page.wait_for_function('document.querySelector("#tour-audio")?.currentTime>0')
   assert not await page.locator('#tour-audio').evaluate('(a)=>a.loop')
   assert await page.locator('#tour-audio-controls button').count()==1
   await page.locator('[data-narration-toggle]').click()
   assert await page.locator('#tour-audio').evaluate('(a)=>a.paused')
   await page.locator('[data-tour-select="1"]').click()
   assert await page.locator('#tour-audio').evaluate('(a)=>a.paused')
   await page.locator('[data-narration-toggle]').click()
   await page.wait_for_function('document.querySelector("#tour-audio").currentTime>0 && !document.querySelector("#tour-audio").paused')
   if region=='ninh-binh':
    await page.locator('[data-narration-toggle]').blur()
    await page.screenshot(path=str(QA/'narration-desktop.png'),full_page=True)
   for chapter in ['gioi-thieu','dia-ly','lich-su','van-hoa']:
    await page.wait_for_function('(name)=>{const a=document.querySelector("#tour-audio");return a.src.includes(name+".mp3")&&a.currentTime>0&&a.duration>20;}',arg=chapter)
    await page.locator('#tour-audio').evaluate('(a)=>{a.playbackRate=16;}')
   await page.wait_for_function('document.querySelector("#tour-audio").ended')
   assert 'Đã nghe hết' in await page.locator('#narration-status').inner_text()
   await page.locator('[data-narration-toggle]').click()
   await page.wait_for_function('document.querySelector("#tour-audio").src.includes("gioi-thieu.mp3") && document.querySelector("#tour-audio").currentTime>0')
   await page.locator('#tour-audio').evaluate('(a)=>{a.playbackRate=1;}')
   await page.evaluate('window.oldNarration=document.querySelector("#tour-audio")')
   await page.locator('[data-tour-stop]').click()
   assert await page.evaluate('window.oldNarration.paused && !window.oldNarration.hasAttribute("src")')
   assert await page.locator('#tour-audio-controls').is_hidden()
  assert len(set(audio_requests))>=16
  mobile=await browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
  await mobile.route('**/api/status',lambda r:r.fulfill(status=503,json={'error':'Offline'}))
  await mobile.goto(BASE+'#/dia-phuong/lao-cai?tab=du-lich',wait_until='networkidle')
  await mobile.locator('[data-tour-start]').click()
  await mobile.wait_for_function('document.querySelector("#tour-audio")?.currentTime>0')
  assert await mobile.evaluate('document.documentElement.scrollWidth<=innerWidth')
  await mobile.locator('[data-tour-start]').blur()
  await mobile.screenshot(path=str(QA/'narration-mobile.png'),full_page=True)
  await mobile.evaluate('window.oldNarration=document.querySelector("#tour-audio")')
  await mobile.locator('[data-tab=lich-su]').click()
  await mobile.wait_for_function('!document.querySelector("#tour-audio")')
  assert await mobile.evaluate('window.oldNarration.paused')
  assert not errors,errors
  assert not external,external
  await browser.close()
 print('PASS: compact original tour layout, no narration panel, all 16 actual MP3s play sequentially, toggle/resume, automatic next/end/replay, lazy loading, cleanup, desktop/mobile, no API dependency.')

asyncio.run(main())
