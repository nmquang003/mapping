"""Verify prepared hover suggestions with the RAG backend unavailable."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

QA = Path(__file__).resolve().parents[1] / '.qa'

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 1000})
        errors, chat_requests = [], []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('request', lambda request: chat_requests.append(request.url) if '/api/chat' in request.url else None)
        await page.route('**/api/**', lambda route: route.abort())
        await page.goto('http://127.0.0.1:4321/', wait_until='networkidle')
        bubble = page.locator('#province-hint')
        text = bubble.locator('.province-hint-text')
        assert not await bubble.is_visible()
        # Brief sweeps never flash a bubble or leave a stale delayed suggestion.
        ninh_binh = page.locator('[data-province="15"]')
        await ninh_binh.dispatch_event('pointerover', {'pointerType': 'mouse'})
        await ninh_binh.dispatch_event('pointerout', {'pointerType': 'mouse'})
        await page.wait_for_timeout(400)
        assert not await bubble.is_visible()
        # All 34 province boundaries receive a prepared chat sentence with an icon.
        for province in await page.locator('#country-map [data-province]').all():
            name = await province.get_attribute('data-name')
            await province.dispatch_event('pointerover', {'pointerType': 'mouse'})
            await bubble.wait_for(state='visible')
            assert len(await text.inner_text()) > 20
            assert not (await text.inner_text())[0].isalnum()
            if name not in ['Ninh Bình', 'Hà Nội', 'Quảng Ninh', 'Lào Cai']:
                assert name in await text.inner_text()
            await province.dispatch_event('pointerout', {'pointerType': 'mouse'})
        # Use a real mouse hover; markers and cards share the province behavior.
        await page.locator('[data-card="ninh-binh"]').hover()
        await bubble.wait_for(state='visible')
        assert await bubble.locator('button').count() == 0
        assert await bubble.locator('.province-hint-title').count() == 0
        # Returning during the linger period also picks a different sentence.
        for slug in ['ninh-binh', 'ha-noi', 'quang-ninh', 'lao-cai']:
            card = page.locator(f'[data-card="{slug}"]')
            await card.hover()
            await bubble.wait_for(state='visible')
            for _ in range(5):
                previous = await text.inner_text()
                await page.mouse.move(0, 0)
                await page.wait_for_timeout(80)
                await card.hover()
                await bubble.wait_for(state='visible')
                assert previous != await text.inner_text()
            # Movements inside one target must not trigger another choice.
            previous = await text.inner_text()
            await card.dispatch_event('pointerover', {'pointerType': 'mouse'})
            await page.wait_for_timeout(400)
            assert previous == await text.inner_text()
        previous = await text.inner_text()
        await page.wait_for_function("previous => document.querySelector('.province-hint-text').textContent !== previous", arg=previous)
        QA.mkdir(exist_ok=True)
        await page.screenshot(path=str(QA / 'desktop-province-hint.png'), full_page=True, animations='disabled')
        await bubble.hover()
        await page.wait_for_timeout(1900)
        assert await bubble.is_visible()
        await page.keyboard.press('Escape')
        assert not await bubble.is_visible()
        await page.locator('[data-card="ha-noi"]').focus()
        await bubble.wait_for(state='visible')
        assert await text.inner_text()
        await page.locator('#chat-toggle').click()
        assert await page.locator('#chat-panel').is_visible()
        assert not await bubble.is_visible()
        await page.locator('[data-card="lao-cai"]').hover()
        await page.wait_for_timeout(400)
        assert not await bubble.is_visible()
        await page.locator('#chat-close').click()
        await page.mouse.move(0, 0)
        await page.locator('[data-card="quang-ninh"]').hover()
        await bubble.wait_for(state='visible')
        await page.mouse.move(0, 0)
        await bubble.wait_for(state='hidden')
        # Dragging and touch events do not trigger suggestions.
        await ninh_binh.dispatch_event('pointerover', {'pointerType': 'mouse'})
        await bubble.wait_for(state='visible')
        await ninh_binh.dispatch_event('pointerdown', {'pointerType': 'mouse', 'button': 0})
        await page.locator('[data-province="1"]').dispatch_event('pointerover', {'pointerType': 'mouse', 'buttons': 1})
        await page.wait_for_timeout(400)
        assert not await bubble.is_visible()
        await ninh_binh.dispatch_event('pointerup', {'pointerType': 'mouse'})
        await page.locator('[data-province="1"]').dispatch_event('pointerover', {'pointerType': 'touch'})
        await page.wait_for_timeout(400)
        assert not await bubble.is_visible()
        # Keyboard suggestions remain readable on narrow screens.
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.locator('[data-card="ninh-binh"]').focus()
        await bubble.wait_for(state='visible')
        bounds = await bubble.bounding_box()
        assert bounds['x'] >= 0 and bounds['x'] + bounds['width'] <= 390
        assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        await page.screenshot(path=str(QA / 'mobile-province-hint.png'), full_page=True, animations='disabled')
        await page.keyboard.press('Escape')
        assert not await bubble.is_visible()
        assert not chat_requests, chat_requests
        assert not errors, errors
        await browser.close()
    print('PASS: all 34 provinces, random non-repeating re-entry, icons, sentence-only bubble, rotation, offline/backend unavailable, debounce, Escape, focus, chat suppression, drag/touch, mobile layout; no chat requests or JS errors.')

asyncio.run(main())
