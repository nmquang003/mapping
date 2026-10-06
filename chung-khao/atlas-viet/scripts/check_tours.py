"""Check host UI with deterministic iframe responses, independent of AirPano uptime."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:4321/'
QA = Path(__file__).resolve().parents[1] / '.qa'


async def main():
    QA.mkdir(exist_ok=True)
    requests, errors = [], []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 1000})
        page.on('pageerror', lambda error: errors.append(str(error)))

        async def embed(route):
            requests.append(route.request.url)
            await route.fulfill(content_type='text/html', body='<html><body style="background:#214e43;color:white"><p>Test iframe response</p></body></html>')

        await page.route('https://www.airpano.com/**', embed)
        for slug, count, provider in [('ha-noi', 5, 'hanoi-vietnam'), ('quang-ninh', 9, 'halong-bay-vietnam')]:
            await page.goto(BASE + f'#/dia-phuong/{slug}?tab=du-lich', wait_until='networkidle')
            await page.locator('[data-tour-start]').wait_for()
            assert await page.locator('[data-tab=du-lich]').get_attribute('aria-selected') == 'true'
            assert await page.locator('[data-tour-select]').count() == count
            assert await page.locator('iframe').count() == 0
            assert not await page.locator('#tour-controls').is_visible()
            before = len(requests)
            await page.locator('[data-tour-select="4"]').click()
            assert len(requests) == before  # Choosing a starting scene does not load the tour.
            await page.locator('[data-tour-start]').click()
            await page.wait_for_function('document.querySelector("#tour-status").textContent.includes("Khung AirPano")')
            assert requests[-1] == f'https://www.airpano.com/embed.php?3D={provider}&startscene=4'
            assert await page.locator('#tour-frame').get_attribute('allowfullscreen') is not None
            assert not await page.locator('#tour-poster').is_visible()
            await page.locator('[data-tour-fullscreen]').click()
            await page.wait_for_function('document.fullscreenElement?.id==="tour-stage"')
            await page.evaluate('document.exitFullscreen()')
            await page.locator('[data-tour-select="0"]').click()
            await page.wait_for_function('document.querySelector("#tour-status").textContent.includes("Khung AirPano")')
            assert requests[-1].endswith('startscene=0')
            assert await page.locator('#tour-source').get_attribute('href') == f'https://www.airpano.com/360photo/{provider}/?startscene=0'
            await page.locator('[data-tour-retry]').click()
            await page.wait_for_function('document.querySelector("#tour-status").textContent.includes("Khung AirPano")')
            await page.locator('[data-tour-stop]').click()
            assert await page.locator('iframe').count() == 0
            assert await page.locator('#tour-poster').is_visible()
            assert not await page.locator('#tour-controls').is_visible()
            assert await page.locator('[data-tour-start]').evaluate('(button)=>button===document.activeElement')
            await page.locator('[data-tour-start]').click()
            await page.locator('[data-tab=lich-su]').click()
            await page.locator('.timeline').wait_for()
            assert await page.locator('iframe').count() == 0
        for slug, message in [('ninh-binh', 'Dữ liệu 360° đang được bổ sung'), ('lao-cai', 'Chưa có tour 360°')]:
            await page.goto(BASE + f'#/dia-phuong/{slug}?tab=du-lich', wait_until='networkidle')
            assert message in await page.locator('.tour-empty').inner_text()
            assert await page.locator('iframe').count() == 0
            await page.locator('.tour-empty a').click()
            await page.locator('.place-grid').wait_for()
        await page.goto(BASE + '#/dia-phuong/quang-ninh?tab=du-lich', wait_until='networkidle')
        await page.screenshot(path=str(QA / 'desktop-tour.png'), full_page=True)
        await page.locator('[data-tab=du-lich]').focus()
        await page.keyboard.press('ArrowRight')
        await page.locator('.timeline').wait_for()
        assert await page.locator('[data-tab=lich-su]').evaluate('(button)=>button===document.activeElement')

        mobile = await browser.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        await mobile.route('https://www.airpano.com/**', embed)
        for slug in ['ha-noi', 'quang-ninh', 'ninh-binh', 'lao-cai']:
            await mobile.goto(BASE + f'#/dia-phuong/{slug}?tab=du-lich', wait_until='networkidle')
            assert await mobile.evaluate('document.documentElement.scrollWidth<=innerWidth')
        await mobile.goto(BASE + '#/dia-phuong/quang-ninh?tab=du-lich', wait_until='networkidle')
        await mobile.screenshot(path=str(QA / 'mobile-tour.png'), full_page=True)
        await mobile.locator('[data-tour-select="8"]').click()
        await mobile.locator('[data-tour-start]').click()
        await mobile.wait_for_function('document.querySelector("#tour-status").textContent.includes("Khung AirPano")')
        assert requests[-1].endswith('startscene=8')
        assert await mobile.evaluate('document.documentElement.scrollWidth<=innerWidth')
        await mobile.locator('[data-tour-stop]').click()
        await browser.close()
    assert not errors, errors
    print('PASS: lazy iframe; 14 starting scenes; retry/stop; source links; iframe cleanup; deep links; keyboard tabs; empty states; desktop/mobile overflow.')


asyncio.run(main())
