"""Exercise real map → modal → detail flows; save desktop/mobile QA screenshots."""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / '.qa'
QA.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:4321/'

async def main():
    errors=[]
    async with async_playwright() as pw:
        browser=await pw.chromium.launch()
        page=await browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
        page.on('pageerror',lambda error:errors.append(str(error)))
        await page.add_init_script("if (!localStorage.getItem('atlas-scope-migration-tested')) { localStorage.setItem('atlas-viet-saved',JSON.stringify(['ha-long','sa-pa','quang-ninh'])); localStorage.setItem('atlas-scope-migration-tested','1'); }")
        await page.goto(BASE,wait_until='networkidle')
        await page.locator('#country-map').wait_for()
        await page.evaluate('document.fonts.ready')
        assert await page.locator('.province').count()==34
        assert await page.locator('.province.in-scope').count()==4
        assert await page.locator('.destination-card').count()==4
        assert await page.evaluate("JSON.parse(localStorage.getItem('atlas-viet-saved'))") == ['quang-ninh','lao-cai']
        await page.locator('#saved-nav').click()
        assert await page.locator('.saved-item a').all_text_contents()==['Quảng Ninh','Lào Cai']
        assert await page.locator('.saved-item img').evaluate_all('(images)=>images.every(i=>i.complete && i.naturalWidth>0)')
        for _ in range(2): await page.locator('[data-remove-saved]').first.click()
        await page.keyboard.press('Escape')
        assert 'Ninh Bình, Hà Nội, Quảng Ninh và Lào Cai' in await page.locator('.scope-strip').inner_text()
        assert await page.evaluate('Array.from(document.images).every(i=>i.complete && i.naturalWidth>0)')
        await page.screenshot(path=str(QA/'desktop-home.png'),full_page=True,animations="disabled")
        initial=await page.locator('#country-map').get_attribute('viewBox')
        await page.locator('#focus-north').click()
        assert await page.locator('#country-map').get_attribute('viewBox')!=initial
        await page.locator('[data-zoom="reset"]').click()
        assert await page.locator('#country-map').get_attribute('viewBox')==initial
        await page.locator('[data-province="16"]').dispatch_event('click')
        assert 'chưa nằm trong phạm vi' in await page.locator('#toast').inner_text()
        for slug,name in [('ninh-binh','Ninh Bình'),('ha-noi','Hà Nội'),('quang-ninh','Quảng Ninh'),('lao-cai','Lào Cai')]:
            await page.locator(f'.marker[data-open="{slug}"]').dispatch_event('click')
            assert await page.locator('#destination-dialog').is_visible()
            assert name in await page.locator('#destination-title').inner_text()
            assert await page.locator('.local-marker').count()==4
            assert await page.locator('.local-province.selected').evaluate('(el)=>{const b=el.getBBox(),v=el.ownerSVGElement.viewBox.baseVal;return b.x>=v.x && b.y>=v.y && b.x+b.width<=v.x+v.width && b.y+b.height<=v.y+v.height;}')
            if slug in ['quang-ninh','lao-cai']: await page.screenshot(path=str(QA/(slug+'-popup.png')),full_page=True,animations='disabled')
            buttons=page.locator('.place-list-button')
            await buttons.nth(2).click()
            assert await page.locator('.place-list-button.is-active').count()==1
            if slug=='ninh-binh':await page.screenshot(path=str(QA/'desktop-popup.png'),full_page=True,animations="disabled")
            await page.locator('#detail-link').click()
            await page.locator('#detail-title').wait_for()
            assert name==await page.locator('#detail-title').inner_text()
            assert await page.locator('.place-card').count()==4
            await page.reload(wait_until='networkidle')
            assert name==await page.locator('#detail-title').inner_text()
            for tab in ['tong-quan','du-lich','lich-su','van-hoa','nguon','bo-anh','dia-danh']:
                await page.locator(f'[data-tab="{tab}"]').click()
                await page.wait_for_function('(tab)=>document.querySelector("[role=tabpanel]")?.getAttribute("aria-labelledby") === "tab-"+tab',arg=tab)
                assert await page.locator('#tab-content').inner_text()
                if tab=='bo-anh':
                    region={'ha-long':'quang-ninh','sa-pa':'lao-cai'}.get(slug,slug)
                    media=json.loads((ROOT/'dist/assets/ai-images.json').read_text())
                    count=len(media['regions'].get(region,{}).get('images',[]))
                    assert await page.locator('.gallery-item').count()==count
                    if count:
                        first=page.locator('.gallery-item button').first
                        await first.click()
                        assert await page.locator('#info-dialog.image-viewer').is_visible()
                        assert 'Minh họa do AI tạo' in await page.locator('.image-full figcaption').inner_text()
                        assert await page.locator('.image-full img').evaluate('(image)=>image.complete && image.naturalWidth>0')
                        await page.keyboard.press('Escape')
                        assert not await page.locator('#info-dialog').is_visible()
                        assert await first.evaluate('(button)=>button===document.activeElement')
                        for image in await page.locator('.gallery-item img').all():
                            await image.scroll_into_view_if_needed()
                            await image.evaluate('(image)=>image.decode()')
                        assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                        await page.screenshot(path=str(QA/(slug+'-gallery.png')),full_page=True,animations='disabled')
            if slug=='ninh-binh':
                await page.locator('[data-save="ninh-binh"]').click()
                assert await page.locator('#saved-count').inner_text()=='1'
                await page.reload(wait_until='networkidle')
                assert await page.locator('#saved-count').inner_text()=='1'
                await page.screenshot(path=str(QA/'desktop-detail.png'),full_page=True,animations="disabled")
            await page.locator('.breadcrumb a').click()
            await page.locator('#country-map').wait_for()
        for old,new,name in [('ha-long','quang-ninh','Quảng Ninh'),('sa-pa','lao-cai','Lào Cai')]:
            await page.goto(BASE+'#/dia-phuong/'+old+'?tab=dia-danh',wait_until='networkidle')
            await page.wait_for_function('(slug)=>location.hash.includes("/"+slug+"?")',arg=new)
            assert await page.locator('#detail-title').inner_text()==name
            assert await page.locator('[data-tab=dia-danh]').get_attribute('aria-selected')=='true'
        await page.locator('.breadcrumb a').click()
        await page.locator('#saved-nav').click()
        assert await page.locator('.saved-item').count()==1
        await page.keyboard.press('Escape')
        assert not await page.locator('#info-dialog').is_visible()
        await page.locator('#chat-toggle').click()
        assert await page.locator('#chat-panel').is_visible()
        assert await page.locator('#chat-form').is_visible()
        assert 'RAG' in await page.locator('#chat-status').inner_text()
        assert 'Quảng Ninh và Lào Cai' in await page.locator('.chat-scope').inner_text()
        await page.locator('#chat-close').click()
        await page.locator('#sources-footer').click()
        assert 'bốn tỉnh/thành phố' in await page.locator('#info-content').inner_text()
        await page.keyboard.press('Escape')
        await page.goto(BASE+'#/dia-phuong/da-nang',wait_until='networkidle')
        assert 'Chưa có câu chuyện' in await page.locator('main').inner_text()
        mobile=await browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
        mobile.on('pageerror',lambda error:errors.append(str(error)))
        await mobile.goto(BASE,wait_until='networkidle')
        await mobile.locator('#country-map').wait_for()
        assert await mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
        await mobile.screenshot(path=str(QA/'mobile-home.png'),full_page=True,animations="disabled")
        await mobile.locator('[data-card="lao-cai"]').click()
        await mobile.screenshot(path=str(QA/'mobile-popup.png'),full_page=True,animations="disabled")
        assert await mobile.locator('#destination-dialog').evaluate('(el)=>el.scrollWidth<=el.clientWidth+1')
        await mobile.locator('#detail-link').click()
        await mobile.locator('#detail-title').wait_for()
        assert await mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
        await mobile.screenshot(path=str(QA/'mobile-detail.png'),full_page=True,animations="disabled")
        await mobile.locator('[data-tab="bo-anh"]').click()
        await mobile.locator('.ai-gallery').wait_for()
        assert await mobile.evaluate('document.documentElement.scrollWidth <= innerWidth')
        await mobile.locator('.gallery-item button').first.click()
        assert await mobile.locator('#info-dialog').evaluate('(el)=>el.scrollWidth<=el.clientWidth+1')
        await mobile.screenshot(path=str(QA/'mobile-image-viewer.png'),full_page=True,animations='disabled')
        await mobile.keyboard.press('Escape')
        await browser.close()
    assert not errors, errors
    print('PASS: 34 provinces; 4 province map/modal/detail flows; full province bounds; legacy routes and saved migration; all tabs; deep links; saved persistence; out-of-scope; desktop/mobile overflow; no browser errors.')
    print('Screenshots:',QA)

asyncio.run(main())
