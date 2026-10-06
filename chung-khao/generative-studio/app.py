"""Local Gradio workspace for the BTC gateway. Run with: python app.py."""
import argparse
import html
import json
import os
from pathlib import Path

os.environ.setdefault('GRADIO_ANALYTICS_ENABLED', 'False')
import gradio as gr
import numpy as np
from dotenv import load_dotenv
from PIL import Image

from studio.api import APIError, Gateway
from studio.service import MODELS, Studio, is_openai_text, reasoning_choices, sources_from
from studio.storage import Store

APP_DIR = Path(__file__).resolve().parent
REPO = APP_DIR.parent.parent
load_dotenv(REPO / '.env')
load_dotenv(APP_DIR / '.env', override=True)
DATA = Path(os.getenv('STUDIO_DATA_DIR', str(REPO / 'local/generative-studio'))).resolve()
CSS = '''
.gradio-container {max-width:1480px !important; margin:auto !important;}
#hero {padding:22px 26px; background:linear-gradient(110deg,#18332e,#345c4d);border-radius:18px;margin-bottom:16px;color:white;}
#hero h1 {color:white;margin:0;font-size:28px} #hero p{color:#d9e9e0;margin:6px 0 0}
#preview {border:1px solid #d5dfd8;border-radius:16px;padding:18px;}
#generate button {font-weight:600;}
'''


def build_app(store=None, gateway_factory=Gateway):
    store = store or Store(DATA)
    studio = Studio(store)
    if not store.projects():
        store.create_project('Project đầu tiên')
    projects = store.projects()
    default_project = projects[0]['id']

    def gateway(key):
        return gateway_factory(key or os.getenv('STUDIO_API_KEY', ''), os.getenv('STUDIO_API_BASE', 'https://api.thucchien.ai/v1'))

    def project_choices():
        return [(p['name'], p['id']) for p in store.projects()]

    def listing(pid, kind='all', query='', favorites=False, selected=None):
        rows = store.list_runs(pid, kind, query, favorites)
        choices = [(f"{'★ ' if r['favorite'] else ''}{r['created'][11:19]} · {r['kind']} · {r['title']} · {r['status']}", r['id']) for r in rows]
        value = selected if selected in {r['id'] for r in rows} else None
        table = [[r['id'], r['title'], r['kind'], r['model'], r['status'], r['created'],
                  '' if r['cost'] is None else f"${r['cost']:.6f}"] for r in rows]
        total = sum(r['cost'] or 0 for r in store.list_runs(pid))
        unknown = sum(r['cost'] is None and r['model'] != 'local-edit' for r in store.list_runs(pid))
        summary = f"**{len(rows)} kết quả** · Chi phí API đã báo trong project: **${total:.6f}** · {unknown} lần chưa có số liệu chi phí."
        return gr.update(choices=choices, value=value), table, summary

    def render(rid, pid):
        if not rid:
            return ('Chọn kết quả trong thư viện hoặc bắt đầu tạo.', '', [], None, None, [], {}, '', '', False, '', None, '')
        r = store.get(rid)
        if r['project'] != pid:
            raise gr.Error('Kết quả thuộc project khác.')
        folder = store.directory(rid)
        files = store.files(rid)
        text = (folder / 'output.txt').read_text(encoding='utf-8') if (folder / 'output.txt').exists() else ''
        images = [str(p) for p in files if p.suffix == '.png']
        video = next((str(p) for p in files if p.suffix == '.mp4'), None)
        audio = next((str(p) for p in files if p.suffix in ('.mp3', '.wav')), None)
        result_path = folder / ('output.json' if (folder / 'output.json').exists() else 'response.json')
        data = json.loads(result_path.read_text()) if result_path.exists() else {}
        sources = sources_from(data)
        source_md = '\n'.join(f"- [{html.escape(s['title'] or s['url'])}]({s['url']})" for s in sources)
        # Render Google Search Suggestions in an isolated iframe, never raw in the app DOM.
        suggestions = ''.join(m.get('searchEntryPoint', {}).get('renderedContent', '') for m in data.get('vertex_ai_grounding_metadata', []))
        source_html = '<iframe sandbox="allow-popups allow-popups-to-escape-sandbox" style="width:100%;height:140px;border:0" srcdoc="' + html.escape(suggestions, quote=True) + '"></iframe>' if suggestions else ''
        status = f"**{r['status']}** · `{r['model']}` · {r['created']}"
        if r['cost'] is not None:
            status += f" · ${r['cost']:.6f}"
        if r['remote_id']:
            status += '\n\nVideo ID: `' + r['remote_id'] + '`'
        if r['error']:
            status += '\n\n' + r['error']
        return (status, text, images, video, audio, [str(p) for p in files], data, source_md,
                r['title'], bool(r['favorite']), r['tags'], images[0] if images else None, source_html)

    def generate(key, pid, parent, kind, model, prompt, options, upload=None):
        try:
            rid = studio.generate(gateway(key), pid, kind, model, prompt, options, upload, parent or None)
            return listing(pid, selected=rid)
        except (ValueError, APIError) as exc:
            raise gr.Error(str(exc)) from None

    def check_connection(key):
        try:
            data, _ = gateway(key).json('/models', method='GET')
            return f"Kết nối thành công · API liệt kê {len(data.get('data', []))} model. Không tạo nội dung."
        except (ValueError, APIError) as exc:
            return str(exc)

    with gr.Blocks(title='AI Thực Chiến · Generative Studio', analytics_enabled=False) as demo:
        gr.HTML('<div id="hero"><h1>Generative Studio</h1><p>AI Thực Chiến · Từ ý tưởng đến ảnh, video và giọng nói — trong cùng một project.</p></div>')
        with gr.Row():
            project = gr.Dropdown(project_choices(), value=default_project, label='Project đang làm', scale=2)
            project_name = gr.Textbox(label='Tên project mới', placeholder='Ví dụ: Video giới thiệu sản phẩm', scale=2)
            create_project = gr.Button('＋ Tạo project', scale=1)
        with gr.Accordion('Kết nối API & nơi lưu dữ liệu', open=False):
            with gr.Row():
                key = gr.Textbox(label='API key gọi model BTC', type='password', placeholder='Để trống nếu đã đặt STUDIO_API_KEY')
                connection = gr.Button('Kiểm tra kết nối', scale=0)
            connection_status = gr.Textbox(label='Trạng thái kết nối', interactive=False)
            gr.Markdown(f"Dữ liệu được lưu trên máy tại `{store.root}`. Key logging BTC và key gọi model là hai cấu hình riêng.")
        parent = gr.State(None)
        with gr.Row():
            lineage = gr.Markdown('Lần tạo mới độc lập.')
            reset_lineage = gr.Button('Tạo độc lập / bỏ liên kết phiên bản',size='sm',scale=0)
        parent.change(lambda rid: 'Phiên bản dựa trên: `' + rid + '`' if rid else 'Lần tạo mới độc lập.',[parent],[lineage])
        reset_lineage.click(lambda: None,[],[parent])
        with gr.Row(equal_height=False):
            with gr.Column(scale=6):
                with gr.Tabs() as tabs:
                    with gr.Tab('Hình ảnh', id='image'):
                        image_prompt = gr.Textbox(label='Mô tả hình ảnh', lines=6, placeholder='Chủ thể, bối cảnh, phong cách, ánh sáng, bố cục…')
                        with gr.Row():
                            image_model = gr.Dropdown(MODELS['image'], value=MODELS['image'][0], label='Model')
                            aspect = gr.Dropdown(['1:1','3:4','4:3','16:9','9:16'],value='1:1',label='Tỷ lệ khung hình')
                        with gr.Row():
                            image_size = gr.Dropdown(['1024x1024','1536x1024','1024x1536'],value='1024x1024',label='Kích thước OpenAI',visible=False)
                            quality = gr.Dropdown(['low','medium','high'],value='low',label='Chất lượng OpenAI',visible=False)
                        with gr.Accordion('Nâng cao', open=False):
                            image_mode = gr.Radio(['standard','chat'],value='standard',label='Chế độ gọi', info='Chat chỉ dành cho model Nano Banana. Mỗi request chuẩn tạo một ảnh.')
                        image_go = gr.Button('Tạo ảnh', variant='primary')
                        gr.Examples([['Một chú mèo đội nón lá, phong cách tranh Đông Hồ, nền sáng'],['Ảnh sản phẩm chai nước hoa trên mặt đá, ánh sáng studio, phong cách tối giản']], inputs=image_prompt)
                    with gr.Tab('Văn bản', id='text'):
                        text_prompt = gr.Textbox(label='Yêu cầu',lines=5,placeholder='Viết kịch bản, mô tả sản phẩm, sửa đoạn văn…')
                        text_model = gr.Dropdown(MODELS['text'],value=MODELS['text'][0],label='Model')
                        context = gr.Textbox(label='Nội dung trước đó / bản cần chỉnh sửa',lines=4)
                        system = gr.Textbox(label='Chỉ dẫn chung',value='Bạn là trợ lý sáng tạo. Trả lời bằng tiếng Việt trừ khi được yêu cầu khác.',lines=2)
                        with gr.Accordion('Tham số', open=False):
                            search = gr.Checkbox(label='Tìm kiếm web (có thêm phí)',value=False)
                            temperature = gr.Slider(0,2,value=0.7,step=0.1,label='Temperature')
                            tokens = gr.Slider(1024,32768,value=4096,step=1024,label='Giới hạn token output (bao gồm reasoning)')
                            effort = gr.Dropdown(reasoning_choices('gpt-6-luna'),value='low',label='Reasoning OpenAI',visible=False)
                            thinking = gr.Checkbox(label='Thinking DeepSeek',value=False,visible=False)
                        text_go = gr.Button('Tạo văn bản',variant='primary')
                    with gr.Tab('Video', id='video'):
                        video_prompt = gr.Textbox(label='Mô tả video',lines=5,placeholder='Mô tả chuyển động, góc máy, ánh sáng và âm thanh…')
                        video_model = gr.Dropdown(MODELS['video'],value=MODELS['video'][0],label='Model')
                        video_input = gr.Image(type='filepath',sources=['upload'],format='png',label='Ảnh khởi đầu (tùy chọn)')
                        with gr.Row():
                            seconds = gr.Dropdown(['4','6','8'],value='4',label='Thời lượng (giây)')
                            video_size = gr.Dropdown(['1280x720','720x1280'],value='1280x720',label='Kích thước')
                        estimate = gr.Markdown('Ước tính: **$0.20** / video 4 giây với Veo Lite. BTC tính phí khi tạo tác vụ.')
                        video_go = gr.Button('Bắt đầu tạo video',variant='primary')
                        auto_poll = gr.Checkbox(label='Tự kiểm tra video mỗi 10 giây',value=True)
                        poll_button = gr.Button('Kiểm tra / tải video đang chờ')
                        gr.Markdown('Có thể chuyển sang tab khác khi chờ. Bỏ tự kiểm tra chỉ dừng theo dõi, không hủy tác vụ BTC.')
                        with gr.Accordion('Khôi phục video bằng ID',open=False):
                            remote_id = gr.Textbox(label='Video ID từ BTC')
                            recover = gr.Button('Thêm tác vụ để theo dõi (không tạo video mới)')
                    with gr.Tab('Giọng nói', id='speech'):
                        speech_text = gr.Textbox(label='Nội dung đọc',lines=8)
                        speech_model = gr.Dropdown(MODELS['speech'],value=MODELS['speech'][0],label='Model')
                        voice = gr.Dropdown(MODELS['gemini_voices'],value='Zephyr',label='Giọng')
                        speech_go = gr.Button('Tạo giọng nói',variant='primary')
                    with gr.Tab('Phiên âm', id='transcription'):
                        recording = gr.Audio(type='filepath',sources=['upload','microphone'],label='Upload hoặc ghi âm')
                        transcription_model = gr.Dropdown(MODELS['transcription'],value=MODELS['transcription'][0],label='Model')
                        transcription_go = gr.Button('Chuyển thành văn bản',variant='primary')
                    with gr.Tab('Embedding', id='embedding'):
                        embedding_text = gr.Textbox(label='Mỗi dòng là một đoạn văn bản',lines=8)
                        embedding_model = gr.Dropdown(MODELS['embedding'],value=MODELS['embedding'][0],label='Model')
                        gr.Markdown('Gemini Embedding 2 gọi riêng từng dòng. Kết quả được lưu dạng JSON; so sánh chỉ dùng vector trong cùng lần tạo/model.')
                        embedding_go = gr.Button('Tạo embedding',variant='primary')
                        similarity_go = gr.Button('So sánh độ tương đồng của output đã chọn')
                        similarity = gr.Dataframe(label='Cosine similarity',interactive=False)
                    with gr.Tab('Kiểm duyệt', id='moderation'):
                        moderation_text = gr.Textbox(label='Nội dung kiểm tra',lines=6)
                        moderation_go = gr.Button('Kiểm tra nội dung',variant='primary')
                    with gr.Tab('Sửa ảnh local', id='edit'):
                        editor = gr.ImageEditor(type='pil',sources=['upload'],label='Crop hoặc resize ảnh',brush=False,eraser=False)
                        edit_go = gr.Button('Lưu ảnh thành phiên bản mới',variant='primary')
            with gr.Column(scale=6,elem_id='preview'):
                gr.Markdown('### Kết quả & phiên bản')
                status = gr.Markdown('Chọn kết quả trong thư viện hoặc bắt đầu tạo.')
                preview_image = gr.Gallery(label='Ảnh',columns=2,height=340,visible=False)
                preview_video = gr.Video(label='Video',visible=False)
                preview_audio = gr.Audio(label='Audio',visible=False)
                output_text = gr.Textbox(label='Văn bản — có thể chỉnh sửa',lines=12,visible=False)
                with gr.Row():
                    save_text = gr.Button('Lưu bản văn đã sửa')
                    reuse = gr.Button('Dùng lại prompt & tham số')
                with gr.Row():
                    to_speech = gr.Button('Văn bản → Giọng nói')
                    to_image_prompt = gr.Button('Văn bản → Prompt ảnh')
                    to_video = gr.Button('Ảnh → Video')
                    to_editor = gr.Button('Ảnh → Sửa local')
                selected_image = gr.State(None)
                files = gr.File(label='Tải output',file_count='multiple',interactive=False)
                sources = gr.Markdown()
                suggestions = gr.HTML()
                with gr.Accordion('Chi tiết response / usage',open=False):
                    result_json = gr.JSON(label='Response')
                with gr.Accordion('Thông tin phiên bản',open=False):
                    title = gr.Textbox(label='Tên kết quả')
                    tags = gr.Textbox(label='Tags',placeholder='Ví dụ: nhân vật, cảnh-01, final')
                    favorite = gr.Checkbox(label='★ Đánh dấu chọn')
                    save_meta = gr.Button('Lưu tên / tags / đánh dấu')
        gr.Markdown('### Thư viện project')
        with gr.Row():
            kind_filter = gr.Dropdown(['all','image','text','video','speech','transcription','embedding','moderation'],value='all',label='Loại')
            query = gr.Textbox(label='Tìm theo tên, prompt, model hoặc tag')
            favorites = gr.Checkbox(label='Chỉ mục đã chọn')
            refresh = gr.Button('Làm mới')
        run_select = gr.Dropdown(label='Chọn một lần tạo để xem / chỉnh sửa',choices=[],value=None)
        history = gr.Dataframe(headers=['ID','Tên','Loại','Model','Trạng thái','Thời gian','Chi phí'],interactive=False,wrap=True,max_height=280)
        stats = gr.Markdown()
        with gr.Row():
            export_project = gr.Button('Xuất toàn bộ project ZIP')
            export_run = gr.Button('Xuất kết quả đang chọn ZIP')
            archive = gr.File(label='Tải ZIP',interactive=False)
        timer = gr.Timer(10)
        list_outputs = [run_select,history,stats]
        view_outputs = [status,output_text,preview_image,preview_video,preview_audio,files,result_json,sources,title,favorite,tags,selected_image,suggestions]

        def display(rid,pid):
            values = list(render(rid,pid))
            values[1] = gr.update(value=values[1],visible=bool(rid and store.get(rid)['kind'] in ('text','transcription')))
            values[2] = gr.update(value=values[2],visible=bool(values[2]))
            values[3] = gr.update(value=values[3],visible=bool(values[3]))
            values[4] = gr.update(value=values[4],visible=bool(values[4]))
            return values

        def add_project(name):
            try:
                pid = store.create_project(name)
                return gr.update(choices=project_choices(),value=pid), ''
            except ValueError as exc:
                raise gr.Error(str(exc)) from None
        create_project.click(add_project,[project_name],[project,project_name])
        connection.click(check_connection,[key],[connection_status])
        def switch_project(pid):
            return (*listing(pid),None,gr.update(value='all'),'',False)
        project.change(switch_project,[project],[*list_outputs,parent,kind_filter,query,favorites]).then(display,[run_select,project],view_outputs)
        demo.load(lambda pid: listing(pid),[project],list_outputs)
        run_select.change(display,[run_select,project],view_outputs)
        refresh.click(listing,[project,kind_filter,query,favorites,run_select],list_outputs)
        for component in [kind_filter,query,favorites]:
            component.change(listing,[project,kind_filter,query,favorites,run_select],list_outputs)

        def wire(button, fn, inputs):
            button.click(fn,inputs,list_outputs,concurrency_id='gateway',concurrency_limit=3).then(display,[run_select,project],view_outputs)
        wire(image_go,lambda k,p,pa,m,pr,a,s,q,mode: generate(k,p,pa,'image',m,pr,{'aspect_ratio':a,'size':s,'quality':q,'mode':mode}),
             [key,project,parent,image_model,image_prompt,aspect,image_size,quality,image_mode])
        wire(text_go,lambda k,p,pa,m,pr,sy,co,se,t,n,e,th: generate(k,p,pa,'text',m,pr,{'system':sy,'context':co,'search':se,'temperature':t,'tokens':n,'effort':e,'thinking':th}),
             [key,project,parent,text_model,text_prompt,system,context,search,temperature,tokens,effort,thinking])
        wire(video_go,lambda k,p,pa,m,pr,s,sz,im: generate(k,p,pa,'video',m,pr,{'seconds':s,'size':sz},im),[key,project,parent,video_model,video_prompt,seconds,video_size,video_input])
        wire(speech_go,lambda k,p,pa,m,pr,v: generate(k,p,pa,'speech',m,pr,{'voice':v}),[key,project,parent,speech_model,speech_text,voice])
        wire(transcription_go,lambda k,p,pa,m,a: generate(k,p,pa,'transcription',m,'Phiên âm',{},a),[key,project,parent,transcription_model,recording])
        wire(embedding_go,lambda k,p,pa,m,pr: generate(k,p,pa,'embedding',m,pr,{}),[key,project,parent,embedding_model,embedding_text])
        wire(moderation_go,lambda k,p,pa,pr: generate(k,p,pa,'moderation','omni-moderation-latest',pr,{}),[key,project,parent,moderation_text])

        def image_controls(model, mode):
            oi = model.startswith('gpt-image')
            return gr.update(visible=not oi and mode!='chat'),gr.update(visible=oi),gr.update(visible=oi),gr.update(value='standard' if oi else mode,interactive=not oi)
        image_model.change(image_controls,[image_model,image_mode],[aspect,image_size,quality,image_mode])
        image_mode.change(lambda m,mode: gr.update(visible=not m.startswith('gpt-image') and mode!='chat'),[image_model,image_mode],[aspect])
        def text_controls(model, current_effort, current_search):
            oi = is_openai_text(model)
            choices = reasoning_choices(model)
            return gr.update(visible=not oi),gr.update(visible=oi,choices=choices,value=current_effort if current_effort in choices else 'low'),gr.update(visible=model.startswith('deepseek')),gr.update(value=False if model.startswith('deepseek') else current_search,interactive=not model.startswith('deepseek'))
        text_model.change(text_controls,[text_model,effort,search],[temperature,effort,thinking,search])
        speech_model.change(lambda m,v: gr.update(choices=MODELS['openai_voices'] if m.startswith('gpt-') else MODELS['gemini_voices'],value=v if v in (MODELS['openai_voices'] if m.startswith('gpt-') else MODELS['gemini_voices']) else ('alloy' if m.startswith('gpt-') else 'Zephyr')),[speech_model,voice],[voice])
        video_model.change(lambda m,sz: gr.update(choices=['1280x720','720x1280'] if 'lite' in m else ['1280x720','720x1280','1920x1080','1080x1920'],value='1280x720' if 'lite' in m and sz not in ('1280x720','720x1280') else sz),[video_model,video_size],[video_size])
        def video_estimate(m,s,sz):
            rate = MODELS['video_usd_per_second'][m]
            if 'fast' in m and sz in ('1920x1080','1080x1920'):
                rate = 0.12
            return f'Ước tính theo tài liệu BTC: **${rate*int(s):.2f}**. Giá có thể thay đổi; BTC tính phí khi tạo tác vụ.'
        for c in [video_model,seconds,video_size]:
            c.change(video_estimate,[video_model,seconds,video_size],[estimate])

        def poll(k,p,selected,enabled=True,kind='all',query='',favorites=False):
            if enabled and (k or os.getenv('STUDIO_API_KEY')):
                studio.poll(gateway(k),p)
            return listing(p,kind,query,favorites,selected)
        def video_preview(rid,pid):
            if not rid or store.get(rid)['kind']!='video':
                return gr.skip(),gr.skip(),gr.skip()
            values=render(rid,pid)
            return values[0],gr.update(value=values[3],visible=bool(values[3])),values[5]
        timer.tick(poll,[key,project,run_select,auto_poll,kind_filter,query,favorites],list_outputs,concurrency_id='video-poll',concurrency_limit=1).then(video_preview,[run_select,project],[status,preview_video,files])
        poll_button.click(poll,[key,project,run_select],list_outputs).then(display,[run_select,project],view_outputs)
        wire(recover,lambda p,m,r: listing(p,selected=studio.recover_video(p,m,r)),[project,video_model,remote_id])

        def save_revision(rid,pid,text):
            if not rid or store.get(rid)['kind'] not in ('text','transcription'):
                raise gr.Error('Chọn output văn bản trước.')
            if store.get(rid)['project'] != pid:
                raise gr.Error('Output thuộc project khác.')
            return listing(pid,selected=store.save_text_revision(rid,text))
        wire(save_text,save_revision,[run_select,project,output_text])
        def save_edit(pid,rid,value):
            im = value.get('composite') if value else None
            try:
                return listing(pid,selected=studio.save_image_edit(pid,rid,im))
            except ValueError as exc:
                raise gr.Error(str(exc)) from None
        wire(edit_go,save_edit,[project,parent,editor])
        def metadata(rid,pid,name,t,f):
            if not rid or store.get(rid)['project'] != pid:
                raise gr.Error('Chọn kết quả trong project.')
            store.update(rid,title=name.strip() or store.get(rid)['title'],tags=t,favorite=int(f))
            return listing(pid,selected=rid)
        save_meta.click(metadata,[run_select,project,title,tags,favorite],list_outputs)
        def transfer_text(text,rid,tab):
            if not text.strip():
                raise gr.Error('Chọn hoặc nhập output văn bản trước.')
            return text,rid,gr.update(selected=tab)
        to_speech.click(lambda t,r: transfer_text(t,r,'speech'),[output_text,run_select],[speech_text,parent,tabs])
        to_image_prompt.click(lambda t,r: transfer_text(t,r,'image'),[output_text,run_select],[image_prompt,parent,tabs])
        def transfer_image(path,rid,tab):
            if not path:
                raise gr.Error('Chọn một output ảnh trước.')
            return path,rid,gr.update(selected=tab)
        to_video.click(lambda p,r: transfer_image(p,r,'video'),[selected_image,run_select],[video_input,parent,tabs])
        to_editor.click(lambda p,r: transfer_image(p,r,'edit'),[selected_image,run_select],[editor,parent,tabs])
        def gallery_pick(rid,evt:gr.SelectData):
            images = [str(p) for p in store.files(rid) if p.suffix=='.png']
            return images[int(evt.index)]
        preview_image.select(gallery_pick,[run_select],[selected_image])

        def reuse_run(rid,pid):
            if not rid or store.get(rid)['project'] != pid:
                raise gr.Error('Chọn một lần tạo trước.')
            r=store.get(rid)
            req=json.loads((store.directory(rid)/'request.json').read_text()).get('body',{})
            kind=r['kind'];m=r['model'];pr=r['prompt']
            # Restore relevant form; leave other tabs unchanged.
            updates=[gr.skip() for _ in range(28)]
            if kind=='image' and m in MODELS['image']:
                updates[0:6]=[pr,m,req.get('aspect_ratio','1:1'),req.get('size','1024x1024'),req.get('quality','low'),'chat' if 'messages' in req else 'standard']
            elif kind=='text' and m in MODELS['text']:
                msgs=req.get('messages',req.get('input',[]))
                updates[6:14]=[pr,m,next((x['content'] for x in msgs if x['role']=='system'),''),next((x['content'] for x in msgs if x['role']=='assistant'),''),bool(req.get('tools')),req.get('temperature',0.7),req.get('max_tokens',req.get('max_completion_tokens',req.get('max_output_tokens',4096))),req.get('reasoning_effort',req.get('reasoning',{}).get('effort','low'))]
            elif kind=='video':
                inp=next(store.directory(rid).glob('input.*'),None)
                updates[14:19]=[pr,m,req.get('seconds','4'),req.get('size','1280x720'),str(inp) if inp else None]
            elif kind=='speech':
                updates[19:22]=[pr,m,req.get('voice','Zephyr')]
            elif kind=='embedding':
                updates[22:24]=[pr,m]
            elif kind=='transcription':
                inp=next(store.directory(rid).glob('input.*'),None)
                updates[24:26]=[str(inp) if inp else None,m]
            elif kind=='moderation':
                updates[26]=pr
            if kind=='text':
                updates[27]=req.get('thinking',{}).get('type')=='enabled'
            return (*updates,rid,gr.update(selected=kind if kind!='moderation' else 'moderation'))
        reuse.click(reuse_run,[run_select,project],[image_prompt,image_model,aspect,image_size,quality,image_mode,text_prompt,text_model,system,context,search,temperature,tokens,effort,video_prompt,video_model,seconds,video_size,video_input,speech_text,speech_model,voice,embedding_text,embedding_model,recording,transcription_model,moderation_text,thinking,parent,tabs])
        def compare(rid):
            if not rid or store.get(rid)['kind']!='embedding':
                raise gr.Error('Chọn output embedding trước.')
            data=json.loads((store.directory(rid)/'output.json').read_text())
            vectors=np.array([x['embedding'] for x in sorted(data['data'],key=lambda x:x.get('index',0))],dtype=float)
            norms=np.linalg.norm(vectors,axis=1,keepdims=True)
            normalized=np.divide(vectors,norms,out=np.zeros_like(vectors),where=norms!=0)
            matrix=(normalized@normalized.T).round(4)
            return gr.update(value=matrix.tolist(),headers=[f'Đoạn {i+1}' for i in range(len(matrix))])
        similarity_go.click(compare,[run_select],[similarity])
        export_project.click(store.export,[project],[archive])
        def export_selected(pid,rid):
            if not rid:
                raise gr.Error('Chọn kết quả trước.')
            return store.export(pid,rid)
        export_run.click(export_selected,[project,run_select],[archive])
    demo.queue(max_size=32,default_concurrency_limit=3)
    return demo


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=7860)
    parser.add_argument('--open',action='store_true')
    args=parser.parse_args()
    os.environ['GRADIO_TEMP_DIR']=str(DATA/'cache')
    store=Store(DATA)
    store.recover_interrupted()
    build_app(store).launch(server_name='127.0.0.1',server_port=args.port,inbrowser=args.open,share=False,
                       allowed_paths=[str(DATA/'projects')],blocked_paths=[str(REPO/'.env'),str(APP_DIR/'.env'),str(DATA/'studio.sqlite')],
                       max_file_size='100mb',theme=gr.themes.Soft(primary_hue='emerald',neutral_hue='slate'),css=CSS,
                       show_error=False,run_history=False,footer_links=[])
