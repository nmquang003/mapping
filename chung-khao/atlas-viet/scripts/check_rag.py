"""Browser checks with mocked API by default; --live exercises the real BTC RAG."""
import argparse
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE='http://127.0.0.1:4322/'

async def main(live):
    errors=[]
    async with async_playwright() as pw:
        browser=await pw.chromium.launch()
        context=await browser.new_context(viewport={'width':1440,'height':1000})
        if not live:
            async def mock(route):
                data=route.request.post_data_json
                await route.fulfill(json={
                    'status':'answered','answer':'Hoa Lư là cố đô.',
                    'claims':[{'text':'Hoa Lư là cố đô. <img src=x onerror=alert(1)>','source_ids':['ninh-binh:S05']}],
                    'sources':[{'id':'ninh-binh:S05','title':'Cố đô Hoa Lư','publisher':'Du lịch Ninh Bình',
                    'url':'https://dulichninhbinh.com.vn/item/3020','accessed_on':'2026-10-06'}]})
            await context.route('**/api/chat',mock)
        page=await context.new_page()
        page.on('pageerror',lambda e:errors.append(str(e)))
        await page.goto(BASE,wait_until='networkidle')
        await page.locator('#chat-toggle').click()
        await page.locator('#chat-question').fill('Hoa Lư có vai trò gì trong lịch sử?')
        await page.locator('#chat-submit').click()
        await page.wait_for_function('!document.querySelector("#chat-submit").disabled',timeout=240000)
        assert not await page.locator('#chat-error').is_visible(),await page.locator('#chat-error').inner_text()
        assert await page.locator('.chat-citation').count()>0
        assert 'Hoa Lư' in await page.locator('#chat-messages').inner_text()
        assert await page.locator('#chat-messages img').count()==0
        assert await page.locator('#chat-question').is_enabled()
        await page.screenshot(path=str(ROOT/'.qa/rag-desktop.png'),full_page=True,animations='disabled')
        if live:
            await page.locator('#chat-question').fill('Huế có những di tích nào?')
            await page.locator('#chat-submit').click()
            await page.wait_for_function('!document.querySelector("#chat-submit").disabled',timeout=240000)
            assert 'chưa có trong phạm vi' in await page.locator('#chat-messages').inner_text()
        else:
            await context.unroute('**/api/chat')
            await context.route('**/api/chat',lambda route:route.fulfill(status=503,json={'error':'API BTC tạm thời lỗi.'}))
            await page.locator('#chat-question').fill('Câu hỏi kiểm tra lỗi')
            await page.locator('#chat-submit').click()
            await page.wait_for_function('!document.querySelector("#chat-submit").disabled')
            assert 'API BTC tạm thời lỗi.' in await page.locator('#chat-error').inner_text()
            assert await page.locator('#chat-question').input_value()=='Câu hỏi kiểm tra lỗi'
            await page.locator('#chat-close').click()
            await page.goto(BASE+'#/dia-phuong/ninh-binh?tab=dia-danh',wait_until='networkidle')
            await page.locator('[data-ask-atlas]').first.click()
            assert await page.locator('#chat-dataset').input_value()=='ninh-binh'
            assert 'Tràng An' in await page.locator('#chat-question').input_value()
        await page.set_viewport_size({'width':390,'height':844})
        await page.screenshot(path=str(ROOT/'.qa/rag-mobile.png'),full_page=True,animations='disabled')
        assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert await page.locator('#chat-panel').evaluate('(p)=>p.getBoundingClientRect().height<=innerHeight-90')
        await browser.close()
    assert not errors,errors
    print('PASS: RAG browser ('+('live BTC' if live else 'mocked API')+'): citations, input, mobile fit, '+('out-of-scope' if live else 'XSS-safe text, API error recovery, landmark context')+'.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--live',action='store_true');args=parser.parse_args()
    asyncio.run(main(args.live))
