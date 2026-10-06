"""Check notebook persistence, migration, sample lifecycle and responsive UI."""
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

BASE = os.environ.get('ATLAS_TEST_URL', 'http://127.0.0.1:4321/')
QA = Path(__file__).resolve().parents[1] / '.qa'

async def main():
    QA.mkdir(exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={'width':1440,'height':1000})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        await page.goto(BASE+'#/so-tay', wait_until='networkidle')
        await page.locator('.notebook-card').first.wait_for()
        assert await page.locator('.notebook-card').count() == 3
        assert await page.locator('#saved-count').inner_text() == '3'
        assert await page.locator('[data-journal-visited="ha-noi"]').is_checked()
        await page.locator('#note-ninh-binh').fill('Ghi nhớ <script>alert(1)</script> & "Hoa Lư"')
        await page.reload(wait_until='networkidle')
        assert await page.locator('#note-ninh-binh').input_value() == 'Ghi nhớ <script>alert(1)</script> & "Hoa Lư"'
        await page.locator('[data-journal-visited="ninh-binh"]').check()
        await page.locator('#notebook-filter').select_option('visited')
        assert await page.locator('.notebook-card').count() == 2
        await page.locator('#notebook-filter').select_option('all')
        await page.locator('#notebook-search').fill('hoa lu')
        assert await page.locator('.notebook-card').count() == 1
        await page.locator('#notebook-search').fill('khong ton tai')
        await page.locator('[data-notebook-reset]').click()
        await page.locator('#notebook-sort').select_option('name')
        assert (await page.locator('.notebook-card h2 a').all_text_contents())[0].strip() == 'Hà Nội'
        async with page.expect_download() as download_info:
            await page.locator('[data-notebook-export]').click()
        download = await download_info.value
        assert download.suggested_filename == 'so-tay-atlas-viet.txt'
        content = Path(await download.path()).read_text()
        assert 'Hoa Lư' in content and 'Đã khám phá' in content
        for width in [1440,390]:
            await page.set_viewport_size({'width':width,'height':1000})
            assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            for img in await page.locator('.notebook-card img').all():
                await img.scroll_into_view_if_needed()
                await img.evaluate('(img)=>img.decode()')
            await page.locator('#main').focus()
            await page.screenshot(path=str(QA/f'notebook-{width}.png'),full_page=True)
        await page.locator('[data-save="quang-ninh"]').click()
        assert await page.locator('.notebook-card').count() == 4
        for _ in range(4):
            await page.locator('[data-remove-saved]').first.click()
        await page.reload(wait_until='networkidle')
        assert await page.locator('.notebook-card').count() == 0
        assert await page.locator('[data-notebook-export]').is_disabled()
        await page.locator('[data-save="ninh-binh"]').click()
        assert 'Hoa Lư' in await page.locator('#note-ninh-binh').input_value()
        await page.locator('.notebook-card h2 a').click()
        await page.locator('[data-save="ninh-binh"]').click()
        assert await page.locator('#saved-count').inner_text() == '0'
        legacy = await browser.new_page()
        await legacy.add_init_script("if (!localStorage.getItem('atlas-viet-notebook-seeded-v1')) localStorage.setItem('atlas-viet-saved', JSON.stringify(['ha-long','sa-pa','quang-ninh']));")
        await legacy.goto(BASE+'#/so-tay',wait_until='networkidle')
        assert await legacy.locator('.notebook-card').count() == 2
        assert await legacy.evaluate("JSON.parse(localStorage.getItem('atlas-viet-saved'))") == ['quang-ninh','lao-cai']
        assert errors == [], errors
        await browser.close()
    print('PASS notebook samples, notes, status, search, filter, sorting, export, removal, reload, migration, desktop/mobile; no browser errors')

asyncio.run(main())
