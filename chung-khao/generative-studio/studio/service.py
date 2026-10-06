import base64
import io
import json
import mimetypes
import threading
from pathlib import Path

from PIL import Image

from .api import APIError

MODELS = json.loads(Path(__file__).with_name('models.json').read_text())


def is_openai_text(model):
    return model.startswith('gpt-') or model in ('o3', 'o4-mini')


def reasoning_choices(model):
    if model in ('o3', 'o4-mini'):
        return ['low', 'medium', 'high']
    base = ['low', 'medium', 'high', 'xhigh', 'max']
    return base if model in ('gpt-6.1-sol', 'gpt-6-astra') else ['none', *base]


def text_request(model, prompt, system='', context='', search=False, temperature=0.7, tokens=4096, effort='low', thinking=False):
    messages = []
    if system.strip():
        messages.append({'role': 'system', 'content': system.strip()})
    if context.strip():
        messages.append({'role': 'assistant', 'content': context.strip()})
    messages.append({'role': 'user', 'content': prompt})
    if search and model.startswith('deepseek'):
        raise ValueError('DeepSeek không hỗ trợ tìm kiếm web.')
    if is_openai_text(model) and effort not in reasoning_choices(model):
        raise ValueError('Mức reasoning không được model hỗ trợ.')
    if search and is_openai_text(model):
        return '/responses', {'model': model, 'input': messages, 'tools': [{'type': 'web_search'}],
                              'reasoning': {'effort': effort}, 'max_output_tokens': int(tokens)}
    data = {'model': model, 'messages': messages}
    if is_openai_text(model):
        if effort not in reasoning_choices(model):
            raise ValueError('Mức reasoning không được model hỗ trợ.')
        data.update(max_completion_tokens=int(tokens), reasoning_effort=effort)
    else:
        data.update(max_tokens=int(tokens), temperature=temperature)
        if model.startswith('deepseek'):
            data['thinking'] = {'type': 'enabled' if thinking else 'disabled'}
    if search:
        data['tools'] = [{'googleSearch': {}}]
    return '/chat/completions', data


def extract_text(data):
    if 'choices' in data:
        msg = data['choices'][0]['message']
        content = msg.get('content') or ''
        if isinstance(content, list):
            content = '\n'.join(p.get('text', '') for p in content)
        return content
    return data.get('output_text') or '\n'.join(
        c.get('text', '') for item in data.get('output', []) for c in item.get('content', []) if c.get('type') == 'output_text')


def sources_from(data):
    sources = []
    for meta in data.get('vertex_ai_grounding_metadata', []):
        for chunk in meta.get('groundingChunks', []):
            web = chunk.get('web', {})
            if web.get('uri'):
                sources.append({'title': web.get('title', ''), 'url': web['uri']})
    for item in data.get('output', []):
        for content in item.get('content', []):
            for annotation in content.get('annotations', []):
                if annotation.get('type') == 'url_citation':
                    sources.append({'title': annotation.get('title', ''), 'url': annotation.get('url', '')})
    return sources


class Studio:
    def __init__(self, store):
        self.store = store
        self.video_lock = threading.Lock()

    def generate(self, api, pid, kind, model, prompt, options=None, upload=None, parent=None):
        options = options or {}
        if model not in MODELS[kind]:
            raise ValueError('Model không có trong cấu hình của tác vụ.')
        if not prompt.strip() and kind != 'transcription':
            raise ValueError('Nhập nội dung đầu vào.')
        if kind == 'text':
            endpoint, payload = text_request(model, prompt, **options)
        elif kind == 'image':
            endpoint = '/images/generations'
            payload = {'model': model, 'prompt': prompt, 'n': 1}
            if model.startswith('gpt-image'):
                payload.update(size=options.get('size', '1024x1024'), quality=options.get('quality', 'low'))
            else:
                payload['aspect_ratio'] = options.get('aspect_ratio', '1:1')
            if options.get('mode') == 'chat':
                if model.startswith('gpt-image'):
                    raise ValueError('Model ảnh OpenAI dùng chế độ chuẩn.')
                endpoint = '/chat/completions'
                payload = {'model': model, 'messages': [{'role': 'user', 'content': prompt}], 'modalities': ['image']}
        elif kind == 'video':
            endpoint = '/videos'
            seconds, size = str(options.get('seconds', '4')), options.get('size', '1280x720')
            if seconds not in ('4', '6', '8') or size not in ('1280x720', '1920x1080', '720x1280', '1080x1920'):
                raise ValueError('Thời lượng hoặc kích thước video không hợp lệ.')
            if 'lite' in model and size not in ('1280x720', '720x1280'):
                raise ValueError('Veo Lite: chọn độ phân giải 720p.')
            payload = {'model': model, 'prompt': prompt, 'seconds': seconds, 'size': size}
        elif kind == 'speech':
            endpoint = '/audio/speech'
            voices = MODELS['openai_voices'] if model.startswith('gpt-') else MODELS['gemini_voices']
            if options.get('voice') not in voices:
                raise ValueError('Chọn giọng phù hợp với model.')
            payload = {'model': model, 'input': prompt, 'voice': options['voice']}
        elif kind == 'transcription':
            if not upload:
                raise ValueError('Upload hoặc ghi âm trước khi phiên âm.')
            endpoint, payload = '/audio/transcriptions', {'model': model, 'response_format': 'json'}
        elif kind == 'embedding':
            lines = [line.strip() for line in prompt.splitlines() if line.strip()]
            if len(lines) > 100:
                raise ValueError('Tối đa 100 đoạn trong một lần tạo.')
            endpoint, payload = '/embeddings', {'model': model, 'input': lines}
        else:
            endpoint, payload = '/moderations', {'model': model, 'input': prompt}
        rid = self.store.create_run(pid, kind, model, prompt, {'endpoint': endpoint, 'body': payload, 'upload': bool(upload)}, parent)
        folder = self.store.directory(rid)
        try:
            copied = self.store.copy_input(rid, upload)
            file = None
            if copied and kind in ('transcription', 'video'):
                file = ('file' if kind == 'transcription' else 'input_reference', copied,
                        mimetypes.guess_type(copied)[0] or 'application/octet-stream')
            if kind == 'speech':
                response, cost = api.request('POST', endpoint, payload)
                content_type = response.headers.get('content-type', '')
                suffix = '.wav' if 'wav' in content_type else '.mp3'
                (folder / ('output' + suffix)).write_bytes(response.content)
                self.store.update(rid, status='completed', cost=cost)
                return rid
            if kind == 'embedding' and model == 'gemini-embedding-2':
                merged, costs = [], []
                for line in payload['input']:
                    data, cost = api.json(endpoint, {'model': model, 'input': line})
                    merged.append({**data['data'][0], 'index': len(merged)})
                    if cost is not None:
                        costs.append(cost)
                    # Persist partial results before starting the next billed call.
                    self.store.write_json(rid, 'output.json', {'data': merged})
                data, cost = {'data': merged}, sum(costs) if len(costs) == len(merged) else None
            else:
                data, cost = api.json(endpoint, payload, file=file)
            if kind == 'video':
                if not data.get('id'):
                    raise APIError('API chưa trả video_id. Không tự tạo lại tác vụ.', uncertain=True)
                self.store.update(rid, status='processing', remote_id=data['id'], cost=cost)
                self.store.write_json(rid, 'response.json', data)
                return rid
            if kind == 'image':
                images = data.get('data', []) if endpoint == '/images/generations' else data['choices'][0]['message'].get('images', [])
                if not images:
                    raise APIError('API không trả ảnh trong response.')
                for i, entry in enumerate(images):
                    encoded = entry.get('b64_json') or entry.get('image_url', {}).get('url', '')
                    if encoded.startswith('data:'):
                        encoded = encoded.split(',', 1)[1]
                    raw = base64.b64decode(encoded, validate=True)
                    with Image.open(io.BytesIO(raw)) as image:
                        image.save(folder / f'output-{i+1}.png')
                summary = {k: v for k, v in data.items() if k not in ('data', 'choices')}
                summary['images'] = [{'revised_prompt': x.get('revised_prompt')} for x in images]
                self.store.write_json(rid, 'response.json', summary)
            else:
                self.store.write_json(rid, 'response.json', data)
                if kind in ('text', 'transcription'):
                    text = extract_text(data) if kind == 'text' else data.get('text', '')
                    (folder / 'output.txt').write_text(text, encoding='utf-8')
                else:
                    self.store.write_json(rid, 'output.json', data)
            self.store.update(rid, status='completed', cost=cost)
        except Exception as exc:
            error = str(exc).replace(api.key, '[REDACTED]') if isinstance(exc, (APIError, ValueError)) else 'Không thể xử lý hoặc lưu kết quả. Kiểm tra file output đã lưu; không tự gửi lại tác vụ.'
            status = 'uncertain' if getattr(exc, 'uncertain', False) else 'failed'
            self.store.update(rid, status=status, error=error)
        return rid

    def poll(self, api, pid):
        if not self.video_lock.acquire(blocking=False):
            return []
        changed = []
        try:
            for run in self.store.list_runs(pid, 'video'):
                if run['status'] != 'processing' or not run['remote_id']:
                    continue
                rid = run['id']
                try:
                    data, _ = api.video_status(run['remote_id'])
                    self.store.write_json(rid, 'response.json', data)
                    status = data.get('status')
                    if status == 'completed':
                        response, _ = api.video_content(run['remote_id'])
                        (self.store.directory(rid) / 'output.mp4').write_bytes(response.content)
                        self.store.update(rid, status='completed', error='')
                    elif status == 'failed':
                        self.store.update(rid, status='failed', error=str(data.get('error', 'Video thất bại.')).replace(api.key, '[REDACTED]'))
                    else:
                        self.store.update(rid, error='')
                    changed.append(rid)
                except Exception:
                    # Keep remote id and processing state so GET/download can resume.
                    self.store.update(rid, error='Chưa kiểm tra/tải được video. Mã tác vụ vẫn được giữ; thử kiểm tra lại.')
        finally:
            self.video_lock.release()
        return changed

    def recover_video(self, pid, model, remote_id):
        if not remote_id.strip():
            raise ValueError('Nhập video_id đã nhận từ BTC.')
        rid = self.store.create_run(pid, 'video', model, 'Khôi phục tác vụ video', {'remote_id': remote_id.strip()})
        self.store.update(rid, remote_id=remote_id.strip(), status='processing')
        return rid

    def save_image_edit(self, pid, source, image):
        if image is None:
            raise ValueError('Chọn hoặc tải ảnh vào trình chỉnh sửa.')
        if source and self.store.get(source)['project'] != pid:
            raise ValueError('Ảnh gốc thuộc project khác.')
        rid = self.store.create_run(pid, 'image', 'local-edit', 'Chỉnh sửa ảnh local', {}, source or None)
        image.save(self.store.directory(rid) / 'output.png')
        self.store.update(rid, status='completed')
        return rid
