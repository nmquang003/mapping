import json
import threading
from pathlib import Path
from urllib.parse import quote, urlsplit

import httpx


class APIError(Exception):
    def __init__(self, message, uncertain=False):
        super().__init__(message)
        self.uncertain = uncertain


class Gateway:
    # Shared across sessions: conservative concurrency, not a team-wide quota guarantee.
    semaphore = threading.BoundedSemaphore(3)

    def __init__(self, key, base='https://api.thucchien.ai/v1', transport=None):
        self.key = key.strip()
        if not self.key:
            raise ValueError('Nhập API key gọi model BTC hoặc cấu hình STUDIO_API_KEY.')
        parsed = urlsplit(base.strip())
        if parsed.scheme != 'https' or parsed.netloc != 'api.thucchien.ai' or parsed.query or parsed.fragment:
            raise ValueError('Studio chỉ kết nối HTTPS tới api.thucchien.ai.')
        self.base = base.rstrip('/')
        self.transport = transport

    def request(self, method, endpoint, payload=None, file=None):
        headers = {'Authorization': 'Bearer ' + self.key}
        kwargs = {}
        if file:
            kwargs['data'] = {k: str(v) for k, v in payload.items()}
        else:
            kwargs['json'] = payload if method != 'GET' else None
        try:
            with self.semaphore, httpx.Client(timeout=httpx.Timeout(300, connect=20), transport=self.transport) as client:
                if file:
                    with Path(file[1]).open('rb') as f:
                        kwargs['files'] = {file[0]: (Path(file[1]).name, f, file[2])}
                        response = client.request(method, self.base + endpoint, headers=headers, **kwargs)
                else:
                    response = client.request(method, self.base + endpoint, headers=headers, **kwargs)
        except httpx.HTTPError:
            raise APIError('Mất kết nối hoặc hết thời gian chờ. Yêu cầu có thể đã được nhận; studio không tự gửi lại.', uncertain=method == 'POST') from None
        if response.is_error:
            detail = response.text[:800].replace(self.key, '[REDACTED]')
            if response.status_code == 429:
                message = 'Đã hết budget; cần bổ sung budget.' if 'budget' in detail.lower() else 'Vượt giới hạn tốc độ. Chờ rồi thử lại; studio không tự gửi lại yêu cầu tạo.'
            elif response.status_code in (401, 403):
                message = 'API key không hợp lệ hoặc không có quyền gọi model.'
            else:
                message = f'API trả lỗi {response.status_code}.'
            raise APIError(message + '\n' + detail)
        cost = response.headers.get('x-litellm-response-cost')
        try:
            cost = float(cost) if cost else None
        except ValueError:
            cost = None
        return response, cost

    def json(self, endpoint, payload=None, method='POST', file=None):
        response, cost = self.request(method, endpoint, payload, file)
        try:
            return response.json(), cost
        except json.JSONDecodeError:
            raise APIError('API không trả JSON hợp lệ.', uncertain=method == 'POST') from None

    def video_status(self, remote_id):
        return self.json('/videos/' + quote(remote_id, safe=''), method='GET')

    def video_content(self, remote_id):
        return self.request('GET', '/videos/' + quote(remote_id, safe='') + '/content')
