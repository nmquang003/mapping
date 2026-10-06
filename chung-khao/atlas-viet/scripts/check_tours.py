"""Exercise actual local cubemaps; fail if a tour needs any third-party request."""
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

BASE = os.environ.get('ATLAS_TEST_URL', 'http://127.0.0.1:4321/').rstrip('/') + '/'
QA = Path(__file__).resolve().parents[1] / '.qa'

async def loaded(page):
    await page.wait_for_function('document.querySelector("#tour-status")?.textContent.startsWith("Đang xem:")')
    await page.wait_for_function('!document.querySelector("#tour-viewer .pnlm-fade-img")')
    assert await page.locator('#tour-viewer canvas').count() == 1

async def main():
    QA.mkdir(exist_ok=True)
    errors, external, images = [], [], []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(args=['--enable-webgl', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
        page = await browser.new_page(viewport={'width':1440,'height':1000})
        page.on('pageerror', lambda e: errors.append(str(e)))
        async def requests(route):
            url=route.request.url
            if not url.startswith(BASE) and not url.startswith('data:'):
                external.append(url)
                await route.abort()
            else:
                if '/assets/360/' in url and url.endswith('.jpg'): images.append(url)
                await route.continue_()
        await page.route('**/*',requests)
        await page.route('**/api/status',lambda route:route.fulfill(status=503,json={'error':'Backend intentionally unavailable in tour checks.'}))
        for slug,count in [('ha-noi',5),('quang-ninh',9),('ninh-binh',8),('lao-cai',22)]:
            await page.goto(BASE+f'#/dia-phuong/{slug}?tab=du-lich',wait_until='networkidle')
            await page.locator('[data-tour-start]').wait_for()
            assert await page.locator('[data-tour-select]').count()==count
            assert await page.locator('iframe, #tour-viewer, #tour-audio').count()==0
            before=len(images)
            await page.locator('[data-tour-select="4"]').click()
            assert len(images)==before
            await page.locator('[data-tour-start]').click()
            await loaded(page)
            await page.wait_for_function('document.querySelector("#tour-audio")?.currentTime>0 && !document.querySelector("#tour-audio").paused')
            assert await page.locator('#tour-audio').evaluate('(a)=>!a.loop && a.volume===.75')
            await page.evaluate('window.testAudio=document.querySelector("#tour-audio")')
            await page.locator('#tour-volume').evaluate('(input)=>{input.value=40;input.dispatchEvent(new Event("input",{bubbles:true}));}')
            assert await page.locator('#tour-audio').evaluate('(a)=>a.volume===.4')
            await page.locator('[data-narration-toggle]').click()
            assert await page.locator('#tour-audio').evaluate('(a)=>a.paused')
            await page.locator('[data-tour-select="0"]').click()
            await loaded(page)
            assert await page.locator('#tour-audio').evaluate('(a)=>a.paused')
            await page.locator('[data-narration-toggle]').click()
            await page.wait_for_function('document.querySelector("[data-narration-toggle]").getAttribute("aria-pressed")==="true"')
            # Return to the default volume before the next destination.
            await page.locator('#tour-volume').evaluate('(input)=>{input.value=75;input.dispatchEvent(new Event("input",{bubbles:true}));}')
            await page.locator('[data-tour-fullscreen]').click()
            await page.wait_for_function('document.fullscreenElement?.id==="tour-stage"')
            await page.evaluate('document.exitFullscreen()')
            for i in range(count):
                await page.locator(f'[data-tour-select="{i}"]').click()
                await loaded(page)
                assert await page.evaluate('window.testAudio===document.querySelector("#tour-audio") && !window.testAudio.paused')
                assert await page.locator(f'[data-tour-select="{i}"]').get_attribute('aria-pressed')=='true'
            # Hotspot navigation must update external scene selection too.
            await page.locator('.pnlm-hotspot.pnlm-scene').first.dispatch_event('click')
            await loaded(page)
            assert await page.locator('[data-tour-select][aria-pressed=true]').get_attribute('data-tour-select')!=str(count-1)
            narration_time=await page.locator('#tour-audio').evaluate('(a)=>a.currentTime')
            await page.locator('[data-tour-retry]').click()
            await loaded(page)
            assert await page.evaluate('window.testAudio===document.querySelector("#tour-audio")')
            assert await page.locator('#tour-audio').evaluate('(a)=>a.currentTime')>=narration_time
            await page.screenshot(path=str(QA/f'local-{slug}.png'),full_page=True)
            await page.locator('[data-tour-stop]').click()
            assert await page.locator('#tour-viewer, #tour-audio').count()==0
            assert await page.evaluate('window.testAudio.paused && !window.testAudio.hasAttribute("src")')
            assert await page.locator('#tour-poster').is_visible()
            await page.locator('[data-tour-start]').click()
            await page.evaluate('window.leavingAudio=document.querySelector("#tour-audio")')
            await page.locator('[data-tab=lich-su]').click()
            await page.wait_for_function('document.querySelector("[data-tab=lich-su]")?.getAttribute("aria-selected")=="true"')
            assert await page.locator('#tour-viewer, #tour-audio').count()==0
            assert await page.evaluate('window.leavingAudio.paused')
        mobile=await browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
        await mobile.route('**/*',requests)
        await mobile.route('**/api/status',lambda route:route.fulfill(status=503,json={'error':'Backend intentionally unavailable in tour checks.'}))
        mobile.on('pageerror',lambda e:errors.append(str(e)))
        for slug in ['quang-ninh','ninh-binh','lao-cai']:
            await mobile.goto(BASE+f'#/dia-phuong/{slug}?tab=du-lich')
            await mobile.locator('[data-tour-start]').click()
            await loaded(mobile)
            assert any(('/panos/mobile/' if slug=='quang-ninh' else '/sa-pa/mobile/' if slug=='lao-cai' else '/ninh-binh/mobile/') in url for url in images)
            assert await mobile.evaluate('document.documentElement.scrollWidth<=innerWidth')
            await mobile.wait_for_function('document.querySelector("#tour-audio")?.currentTime>0')
            if slug in ['ninh-binh','lao-cai']:
                for i in range(8 if slug=='ninh-binh' else 22):
                    await mobile.locator(f'[data-tour-select="{i}"]').click()
                    await loaded(mobile)
                assert ('VRTour' if slug=='lao-cai' else 'Vietnam.travel') in await mobile.locator('.tour-credit').inner_text()
            await mobile.screenshot(path=str(QA/f'local-mobile-{slug}.png'),full_page=True)
            await mobile.locator('[data-tour-stop]').click()
        # Missing local image has an actionable error and retry recovers.
        await page.goto(BASE+'#/dia-phuong/ha-noi?tab=du-lich')
        async def missing(route): await route.fulfill(status=404,body='missing')
        await page.route('**/panos/hi/01/_f.jpg',missing)
        await page.locator('[data-tour-start]').click()
        await page.wait_for_function('document.querySelector("#tour-status").textContent.includes("Không tải được")')
        await page.unroute('**/panos/hi/01/_f.jpg',missing)
        await page.locator('[data-tour-retry]').click()
        await loaded(page)
        # Autoplay rejection remains recoverable through the explicit Narration button.
        blocked=await browser.new_page()
        await blocked.route('**/*',requests)
        await blocked.route('**/api/status',lambda route:route.fulfill(status=503,json={'error':'Backend intentionally unavailable in tour checks.'}))
        await blocked.add_init_script('window.originalPlay=HTMLMediaElement.prototype.play; HTMLMediaElement.prototype.play=function(){return Promise.reject(new DOMException("blocked","NotAllowedError"));}')
        await blocked.goto(BASE+'#/dia-phuong/ha-noi?tab=du-lich')
        await blocked.locator('[data-tour-start]').click()
        await loaded(blocked)
        await blocked.wait_for_function('document.querySelector("#narration-status").textContent.includes("Bấm Bật thuyết minh")')
        assert await blocked.locator('[data-narration-toggle]').get_attribute('aria-pressed')=='false'
        await blocked.evaluate('()=>{HTMLMediaElement.prototype.play=window.originalPlay;}')
        await blocked.locator('[data-narration-toggle]').click()
        await blocked.wait_for_function('document.querySelector("#tour-audio").currentTime>0')
        await blocked.locator('[data-tour-stop]').click()
        await blocked.route('**/audio/narration/**',missing)
        await blocked.locator('[data-tour-start]').click()
        await blocked.wait_for_function('document.querySelector("#narration-status").textContent.includes("Chưa tải được thuyết minh")')
        await blocked.unroute('**/audio/narration/**',missing)
        await blocked.locator('[data-narration-toggle]').click()
        await blocked.wait_for_function('document.querySelector("#tour-audio").currentTime>0')
        await browser.close()
    assert not external,external
    assert not errors,errors
    print('PASS: 44 actual local scenes, hotspot sync, lazy loading, fullscreen, retry/stop, route cleanup, mobile, missing-image recovery; real narration playback, pause/volume, continuity, cleanup, autoplay recovery; zero external requests.')

asyncio.run(main())
