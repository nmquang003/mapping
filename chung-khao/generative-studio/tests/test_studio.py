import base64
import io
import json
import zipfile
from pathlib import Path

import httpx
import pytest
from PIL import Image

from studio.api import APIError, Gateway
from studio.service import Studio, text_request
from studio.storage import Store


@pytest.fixture
def workspace(tmp_path):
    store=Store(tmp_path/'data')
    pid=store.create_project('Project / thử nghiệm')
    return store,pid,Studio(store)


def api(handler):
    return Gateway('secret-test-key',transport=httpx.MockTransport(handler))


def test_model_specific_text_parameters():
    endpoint,payload=text_request('gpt-6.1-sol','Hello',search=True)
    assert endpoint=='/responses'
    assert payload['max_output_tokens']==4096
    assert payload['tools']==[{'type':'web_search'}]
    _,payload=text_request('gpt-6-luna','Hello')
    assert 'max_completion_tokens' in payload and 'temperature' not in payload and 'max_tokens' not in payload
    _,payload=text_request('deepseek-flash','Hello',thinking=False)
    assert payload['thinking']=={'type':'disabled'}
    with pytest.raises(ValueError): text_request('deepseek-flash','Hello',search=True)
    with pytest.raises(ValueError): text_request('o3','Hello',effort='max')


@pytest.mark.parametrize('model,field,absent',[('nano-banana-2','aspect_ratio','size'),('gpt-image-2.5-flare','size','aspect_ratio')])
def test_image_payload_and_decoding(workspace,model,field,absent):
    store,pid,studio=workspace
    image=Image.new('RGB',(12,8),'red');buff=io.BytesIO();image.save(buff,format='PNG')
    def handler(req):
        body=json.loads(req.content)
        assert field in body and absent not in body and body['n']==1
        return httpx.Response(200,json={'data':[{'b64_json':base64.b64encode(buff.getvalue()).decode()}]},headers={'x-litellm-response-cost':'0.01'})
    rid=studio.generate(api(handler),pid,'image',model,'test')
    assert store.get(rid)['status']=='completed'
    assert store.get(rid)['cost']==0.01
    assert Image.open(store.files(rid)[0]).size==(12,8)
    assert 'secret-test-key' not in (store.directory(rid)/'request.json').read_text()


def test_project_revision_and_zip_persistence(workspace):
    store,pid,studio=workspace
    rid=studio.generate(api(lambda r:httpx.Response(200,json={'choices':[{'message':{'content':'Kịch bản'}}]})),pid,'text','gemini-3.5-flash-lite','Viết')
    child=store.save_text_revision(rid,'Bản sửa')
    store.update(child,title='Final',favorite=1,tags='cảnh-01')
    again=Store(store.root)
    assert again.get(child)['parent']==rid
    assert again.list_runs(pid,query='cảnh-01',favorites=True)[0]['id']==child
    with zipfile.ZipFile(store.export(pid)) as z:
        assert any(n.endswith('output.txt') for n in z.namelist())
        assert not any('.env' in n or 'sqlite' in n for n in z.namelist())
    with pytest.raises(ValueError): store.project_dir('../escape')


def test_video_poll_failure_then_resume(workspace):
    store,pid,studio=workspace
    stage={'fail':True,'posts':0}
    def handler(req):
        if req.method=='POST':
            stage['posts']+=1
            return httpx.Response(200,json={'id':'video_123','status':'processing'},headers={'x-litellm-response-cost':'0.2'})
        if req.url.path.endswith('/content'):
            return httpx.Response(200,content=b'mp4-content',headers={'content-type':'video/mp4'})
        if stage['fail']: return httpx.Response(503,text='temporary')
        return httpx.Response(200,json={'id':'video_123','status':'completed'})
    gateway=api(handler)
    rid=studio.generate(gateway,pid,'video','veo-3.1-lite-generate-001','Video',{'seconds':'4','size':'1280x720'})
    studio.poll(gateway,pid)
    assert store.get(rid)['status']=='processing' and store.get(rid)['remote_id']=='video_123'
    stage['fail']=False
    Studio(Store(store.root)).poll(gateway,pid)
    assert store.get(rid)['status']=='completed'
    assert (store.directory(rid)/'output.mp4').read_bytes()==b'mp4-content'
    assert stage['posts']==1


def test_no_retry_on_uncertain_post_and_redact(workspace):
    store,pid,studio=workspace
    calls=[]
    def handler(req):
        calls.append(req)
        raise httpx.ReadTimeout('secret-test-key',request=req)
    rid=studio.generate(api(handler),pid,'image','nano-banana-2','test')
    assert len(calls)==1 and store.get(rid)['status']=='uncertain'
    assert 'secret-test-key' not in store.get(rid)['error']


@pytest.mark.parametrize('detail,expected',[('Budget has been exceeded','hết budget'),('Rate limit exceeded','giới hạn tốc độ')])
def test_429_classification(detail,expected):
    with pytest.raises(APIError,match=expected):
        api(lambda r:httpx.Response(429,text=detail)).json('/images/generations',{})


def test_embedding_two_calls_per_line(workspace):
    store,pid,studio=workspace
    seen=[]
    def handler(req):
        body=json.loads(req.content);seen.append(body['input'])
        return httpx.Response(200,json={'data':[{'embedding':[1.,0.], 'index':0}]})
    rid=studio.generate(api(handler),pid,'embedding','gemini-embedding-2','one\ntwo')
    assert seen==['one','two']
    data=json.loads((store.directory(rid)/'output.json').read_text())
    assert [r['index'] for r in data['data']]==[0,1]


def test_transcription_multipart_and_speech(workspace,tmp_path):
    store,pid,studio=workspace
    upload=tmp_path/'input.wav';upload.write_bytes(b'audio')
    def handler(req):
        assert 'multipart/form-data' in req.headers['content-type']
        assert b'name="file"' in req.content and b'name="response_format"' in req.content
        return httpx.Response(200,json={'text':'Xin chào'})
    rid=studio.generate(api(handler),pid,'transcription','gpt-transcribe','Phiên âm',upload=upload)
    assert (store.directory(rid)/'output.txt').read_text()=='Xin chào'
    rid=studio.generate(api(lambda r:httpx.Response(200,content=b'RIFF',headers={'content-type':'audio/wav'})),pid,'speech','gemini-3.1-flash-tts-preview','Xin chào',{'voice':'Zephyr'})
    assert store.files(rid)[0].suffix=='.wav'


def test_local_image_revision_and_cross_project_rejection(workspace):
    store,pid,studio=workspace
    rid=studio.save_image_edit(pid,None,Image.new('RGB',(16,16)))
    child=studio.save_image_edit(pid,rid,Image.new('RGB',(8,8)))
    assert store.get(child)['parent']==rid
    other=store.create_project('Other')
    with pytest.raises(ValueError): studio.save_image_edit(other,rid,Image.new('RGB',(8,8)))


def test_ui_build_and_callback_registration(workspace):
    from app import build_app
    store,_,_=workspace
    ui=build_app(store)
    config=ui.get_config_file()
    assert len(config['dependencies'])>30
    assert any(c['type']=='imageeditor' for c in config['components'])
    assert any(c['type']=='timer' for c in config['components'])


def test_browser_client_image_workflow(workspace):
    """Exercise real Gradio HTTP queue/serialization with a mocked BTC transport."""
    from app import build_app
    from gradio_client import Client
    store,pid,_=workspace
    image=Image.new('RGB',(10,10),'blue');buff=io.BytesIO();image.save(buff,format='PNG')
    transport=httpx.MockTransport(lambda req:httpx.Response(200,json={'data':[{'b64_json':base64.b64encode(buff.getvalue()).decode()}]}))
    ui=build_app(store,lambda key,base:Gateway(key,base,transport))
    import socket
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    try:
        _,url,_=ui.launch(server_name='127.0.0.1',server_port=port,prevent_thread_lock=True,quiet=True,
                          allowed_paths=[str(store.root/'projects')],footer_links=[])
        client=Client(url,verbose=False)
        fn_index=next(i for i,f in ui.fns.items() if len(f.inputs)==9 and getattr(f.inputs[-1],'label',None)=='Chế độ gọi')
        result=client.predict('mock-key',pid,'nano-banana-2','Ảnh thử nghiệm','1:1','1024x1024','low','standard',fn_index=fn_index)
        rid=result[0]['value']
        assert store.get(rid)['status']=='completed'
        display_index=next(i for i,f in ui.fns.items() if f.fn.__name__=='display')
        rendered=client.predict(rid,pid,fn_index=display_index)
        assert rendered[2]['visible'] is True
        assert rendered[2]['value']
        assert store.files(rid)[0].exists()
        export_index=next(i for i,f in ui.fns.items() if f.fn.__name__=='export_selected')
        archive=client.predict(pid,rid,fn_index=export_index)
        assert Path(archive).exists()
    finally:
        ui.close()


def test_restart_marks_interrupted_posts_but_keeps_video_jobs(workspace):
    store,pid,studio=workspace
    rid=store.create_run(pid,'image','nano-banana-2','pending',{})
    video=studio.recover_video(pid,'veo-3.1-lite-generate-001','video_existing')
    assert store.recover_interrupted()==[rid]
    assert store.get(rid)['status']=='uncertain'
    assert store.get(video)['status']=='processing'
    assert store.get(video)['remote_id']=='video_existing'
