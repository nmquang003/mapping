"""Gradio playground for the AI Thuc Chien Gateway: Image / Video / TTS / STT.

The gateway runs on LiteLLM and (per the organizers) accepts the same parameters as
the original providers (Nano Banana, Veo 3.1, Gemini/OpenAI TTS, Whisper...). This UI
exposes those options, plus a raw JSON box to send any field the UI does not cover.
Every tab has a Request / Response panel showing what the gateway received and returned.

Run:
    export AITC_API_KEY="sk-..."
    uv run demo.py
"""
import base64
import json
import mimetypes
import os
import shlex
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html import escape
from urllib.parse import quote

import gradio as gr
import requests

BASE_URL = os.getenv("AITC_BASE_URL", "https://api.thucchien.ai").rstrip("/")
ENV_KEY = os.getenv("AITC_API_KEY", "")
TIMEOUT = 300
# Options not in the BTC docs default to AUTO = the field is left out of the request.
AUTO = "auto"

# ------------------------------------------------------------------ specs
GOOGLE_RATIOS = [AUTO, "1:1", "3:2", "2:3", "4:3", "3:4", "5:4", "4:5", "16:9", "9:16", "21:9"]

# kind=google: Nano Banana (Gemini image). kind=openai: gpt-image.
IMAGE_SPECS = {
    "nano-banana-2": {"kind": "google", "sizes": ["512", "1K", "2K", "4K"], "max_refs": 14},
    "nano-banana-2-lite": {"kind": "google", "sizes": ["512", "1K"], "max_refs": 14},
    "nano-banana-pro": {"kind": "google", "sizes": ["1K", "2K", "4K"], "max_refs": 14},
    "nano-banana": {"kind": "google", "sizes": [], "max_refs": 3},
    "gpt-image-2.5-flare": {"kind": "openai", "max_refs": 16},
    "gpt-image-2.5-sunburst": {"kind": "openai", "max_refs": 16},
}
OPENAI_SIZES = [AUTO, "1024x1024", "1536x1024", "1024x1536"]

VIDEO_MODELS = [
    "veo-3.1-lite-generate-001",
    "veo-3.1-fast-generate-001",
    "veo-3.1-generate-001",
]
VIDEO_SIZE = {
    ("16:9", "720p"): "1280x720",
    ("16:9", "1080p"): "1920x1080",
    ("16:9", "4k"): "3840x2160",
    ("9:16", "720p"): "720x1280",
    ("9:16", "1080p"): "1080x1920",
    ("9:16", "4k"): "2160x3840",
}

TTS_MODELS = [
    "gemini-3.1-flash-tts-preview",
    "gemini-2.5-flash-preview-tts",
    "gemini-2.5-pro-preview-tts",
    "gpt-4o-mini-tts",
]
GEMINI_VOICES = [
    "Zephyr", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus", "Aoede", "Callirrhoe",
    "Autonoe", "Enceladus", "Iapetus", "Umbriel", "Algieba", "Despina", "Erinome", "Algenib",
    "Rasalgethi", "Laomedeia", "Achernar", "Alnilam", "Schedar", "Gacrux", "Pulcherrima",
    "Achird", "Zubenelgenubi", "Vindemiatrix", "Sadachbia", "Sadaltager", "Sulafat",
]
OPENAI_VOICES = [
    "alloy", "ash", "ballad", "coral", "echo", "fable", "nova", "onyx", "sage", "shimmer",
    "verse", "marin", "cedar",
]
TTS_FORMATS = [AUTO, "mp3", "opus", "aac", "flac", "wav", "pcm"]

STT_MODELS = [
    "gemini-3.5-transcribe-preview",
    "gpt-4o-transcribe",
    "gpt-4o-mini-transcribe",
    "gpt-transcribe",
    "whisper-1",
]
STT_LANGS = ["auto", "vi", "en", "ja", "ko", "zh", "fr", "de", "es", "th", "id", "ru"]


# ------------------------------------------------------------------ helpers
def _headers(api_key: str) -> dict:
    key = (api_key or ENV_KEY).strip()
    if not key:
        raise gr.Error("Missing API key. Enter it in the top-right box or set AITC_API_KEY.")
    return {"Authorization": f"Bearer {key}"}


def _call(method, path, api_key, *, json_body=None, data=None, files=None, timeout=TIMEOUT):
    r = requests.request(
        method,
        f"{BASE_URL}{path}",
        headers=_headers(api_key),
        json=json_body,
        data=data,
        files=files,
        timeout=timeout,
    )
    _track_cost(r)
    if not r.ok:
        raise gr.Error(f"HTTP {r.status_code} {method} {path}: {r.text[:1000]}")
    return r


# Cost of every request made by this app process, from the gateway's
# x-litellm-response-cost header (BTC pricing docs). Shown in the budget bar.
_session = {"cost": 0.0}
_session_lock = threading.Lock()


def _track_cost(r: requests.Response):
    try:
        cost = float(r.headers.get("x-litellm-response-cost", ""))
    except ValueError:
        return
    with _session_lock:
        _session["cost"] += cost


def _tmp(suffix: str) -> str:
    f = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    f.close()
    return f.name


def _save(raw: bytes, suffix: str) -> str:
    path = _tmp(suffix)
    with open(path, "wb") as f:
        f.write(raw)
    return path


def _redact(obj, limit=160):
    """Shorten long strings (base64) for the debug panel."""
    if isinstance(obj, dict):
        return {k: _redact(v, limit) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_redact(v, limit) for v in obj]
    if isinstance(obj, str) and len(obj) > limit:
        return f"{obj[:60]}...<{len(obj)} chars>"
    return obj


def _debug(request, response) -> str:
    return json.dumps(
        {"request": _redact(request), "response": _redact(response)},
        ensure_ascii=False,
        indent=2,
        default=str,
    )


def _resp_json(r: requests.Response):
    try:
        return r.json()
    except ValueError:
        return {"_non_json_body": r.text[:2000]}


def _parse_extra(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        return {}
    try:
        val = json.loads(text)
    except json.JSONDecodeError as e:
        raise gr.Error(f"Raw parameters are not valid JSON: {e}")
    if not isinstance(val, dict):
        raise gr.Error('Raw parameters must be a JSON object, e.g. {"seed": 42}.')
    return val


def _mime(path: str) -> str:
    return mimetypes.guess_type(path)[0] or "image/png"


def _data_uri(path: str) -> str:
    with open(path, "rb") as f:
        return f"data:{_mime(path)};base64,{base64.b64encode(f.read()).decode()}"


def _veo_image(path: str) -> dict:
    with open(path, "rb") as f:
        return {"bytesBase64Encoded": base64.b64encode(f.read()).decode(), "mimeType": _mime(path)}


def _put(body: dict, key: str, value):
    """Set body[key] unless value is empty or AUTO, so undocumented fields stay out by default."""
    if value is None or value == "" or value == AUTO:
        return
    body[key] = value


def _form(d: dict) -> dict:
    """Dict -> multipart form fields. Objects / bools / lists are JSON-encoded."""
    return {k: v if isinstance(v, str) else json.dumps(v) for k, v in d.items()}


def _img_ext(raw: bytes) -> str:
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if raw[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if raw[8:12] == b"WEBP":
        return ".webp"
    return ".png"


def _audio_ext(raw: bytes) -> str:
    if raw[:4] == b"RIFF":
        return ".wav"
    if raw[:4] == b"OggS":
        return ".ogg"
    if raw[:4] == b"fLaC":
        return ".flac"
    return ".mp3"


# ------------------------------------------------------------------ multi-image uploader
def ref_uploader(label: str, max_n: int):
    """fal-style multi-image input: drop/upload many images (uploads append),
    click a thumbnail to preview it, hover + X to remove it."""
    return gr.Gallery(
        label=f"{label} · up to {max_n}",
        interactive=True,
        type="filepath",
        file_types=["image"],
        columns=6,
        object_fit="cover",
        elem_classes="ref-thumbs",
    )


def _paths(gallery) -> list:
    """Gallery value -> list of file paths (items are (path, caption) tuples)."""
    return [item[0] if isinstance(item, (tuple, list)) else item for item in gallery or []]


# ------------------------------------------------------------------ image
def _image_from_response(j: dict) -> str:
    """Handles /images/generations (b64_json | url) and /chat/completions (message.images)."""
    try:
        if "data" in j:
            item = j["data"][0]
            if item.get("b64_json"):
                raw = base64.b64decode(item["b64_json"])
            else:
                raw = requests.get(item["url"], timeout=TIMEOUT).content
        else:
            uri = j["choices"][0]["message"]["images"][0]["image_url"]["url"]
            raw = base64.b64decode(uri.split(",", 1)[-1])
    except (KeyError, IndexError, TypeError):
        raise gr.Error(f"No image in response: {json.dumps(_redact(j), ensure_ascii=False)[:800]}")
    return _save(raw, _img_ext(raw))


def _image_once(api_key, model, prompt, o, refs, extra):
    spec = IMAGE_SPECS[model]
    if spec["kind"] == "google":
        if refs:
            content = [{"type": "text", "text": prompt}]
            content += [{"type": "image_url", "image_url": {"url": _data_uri(p)}} for p in refs]
            body = {
                "model": model,
                "messages": [{"role": "user", "content": content}],
                "modalities": ["image"],
            }
            cfg = {}
            _put(cfg, "aspect_ratio", o["ratio"])
            _put(cfg, "image_size", o["size_g"])
            _put(body, "image_config", cfg or None)
            body.update(extra)
            r = _call("POST", "/v1/chat/completions", api_key, json_body=body)
        else:
            body = {"model": model, "prompt": prompt, "n": 1}
            _put(body, "aspect_ratio", o["ratio"])
            _put(body, "image_size", o["size_g"])
            body.update(extra)
            r = _call("POST", "/images/generations", api_key, json_body=body)
    else:
        body = {"model": model, "prompt": prompt, "n": 1}
        _put(body, "size", o["size_o"])
        _put(body, "quality", o["quality"])
        _put(body, "background", o["background"])
        _put(body, "output_format", o["fmt"])
        _put(body, "moderation", o["moderation"])
        if o["fmt"] in ("jpeg", "webp"):
            body["output_compression"] = int(o["compression"])
        body.update(extra)
        if refs:
            files = []
            for p in refs:
                with open(p, "rb") as f:
                    files.append(("image[]", (os.path.basename(p), f.read(), _mime(p))))
            r = _call("POST", "/images/edits", api_key, data=_form(body), files=files)
        else:
            r = _call("POST", "/images/generations", api_key, json_body=body)
    j = _resp_json(r)
    return _image_from_response(j), body, j


def gen_image(
    api_key, model, prompt, n, ratio, size_g, size_o, quality, background, fmt, compression,
    moderation, refs, extra_json,
):
    if not prompt.strip():
        raise gr.Error("Enter a prompt.")
    extra = _parse_extra(extra_json)
    refs = _paths(refs)
    spec = IMAGE_SPECS[model]
    if len(refs) > spec["max_refs"]:
        raise gr.Error(f"{model} accepts at most {spec['max_refs']} reference images (got {len(refs)}).")
    o = dict(
        ratio=ratio, size_g=size_g, size_o=size_o, quality=quality, background=background,
        fmt=fmt, compression=compression, moderation=moderation,
    )
    n = int(n)
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=n) as pool:
        futs = [pool.submit(_image_once, api_key, model, prompt, o, refs, extra) for _ in range(n)]
        results, errors = [], []
        for f in futs:
            try:
                results.append(f.result())
            except Exception as e:  # gr.Error or network error
                errors.append(str(e))
    if not results:
        raise gr.Error(errors[0])
    status = f"Done: {len(results)}/{n} image(s) in {time.time() - t0:.1f}s"
    if refs:
        status += f" · {len(refs)} reference image(s)"
    if errors:
        status += f" · {len(errors)} failed: {errors[0][:300]}"
    _, body, j = results[0]
    return [r[0] for r in results], status, _debug(body, j)


def on_image_model(model):
    spec = IMAGE_SPECS[model]
    is_google = spec["kind"] == "google"
    sizes = spec.get("sizes", [])
    return (
        gr.update(visible=is_google),
        gr.update(visible=not is_google),
        gr.update(choices=[AUTO] + sizes, value=AUTO, visible=bool(sizes)),
    )


# ------------------------------------------------------------------ video
def est_cost(model, seconds, resolution):
    if resolution == "4k":
        return "Estimated cost: 4k pricing unknown"
    rate = {"veo-3.1-lite-generate-001": 0.05, "veo-3.1-fast-generate-001": 0.10}.get(model, 0.40)
    if model == "veo-3.1-fast-generate-001" and resolution == "1080p":
        rate = 0.12
    secs = 8 if resolution != "720p" else int(seconds)
    return f"Estimated cost: ~${rate * secs:.2f} ({secs}s)"


def gen_video(
    api_key, model, prompt, negative, ratio, resolution, seconds, audio, seed,
    first_frame, last_frame, refs, extra_json,
):
    if not prompt.strip():
        raise gr.Error("Enter a prompt.")
    extra = _parse_extra(extra_json)
    refs = _paths(refs)
    if len(refs) > 3:
        raise gr.Error("Veo 3.1 accepts at most 3 reference images.")

    notes = []
    seconds = str(seconds)
    if (resolution != "720p" or refs or last_frame) and seconds != "8":
        seconds = "8"
        notes.append("duration set to 8s (required for 1080p/4k, reference images, last frame)")

    body = {
        "model": model,
        "prompt": prompt,
        "seconds": seconds,
        "size": VIDEO_SIZE[(ratio, resolution)],
    }
    if resolution == "4k":
        body["resolution"] = "4k"
    if negative.strip():
        body["negativePrompt"] = negative.strip()
    if audio != AUTO:
        body["generateAudio"] = audio == "on"
    seed = (seed or "").strip()
    if seed:
        try:
            body["seed"] = int(seed)
        except ValueError:
            raise gr.Error(f"Seed must be an integer, got {seed!r}.")
    if last_frame:
        body["lastFrame"] = _veo_image(last_frame)
    if refs:
        body["referenceImages"] = [{"image": _veo_image(p), "referenceType": "asset"} for p in refs]
    body.update(extra)

    yield None, "Submitting request...", ""
    if first_frame:
        with open(first_frame, "rb") as f:
            r = _call(
                "POST", "/v1/videos", api_key,
                data=_form(body),
                files={"input_reference": (os.path.basename(first_frame), f.read(), _mime(first_frame))},
            )
    else:
        r = _call("POST", "/v1/videos", api_key, json_body=body)
    video = _resp_json(r)
    if "id" not in video:
        raise gr.Error(f"No video id in response: {json.dumps(video)[:800]}")
    vid = video["id"]

    t0 = time.time()
    while video.get("status") not in ("completed", "failed"):
        yield None, f"[{time.time() - t0:.0f}s] id={vid} · status={video.get('status')} ...", _debug(body, video)
        time.sleep(8)
        video = _resp_json(_call("GET", f"/v1/videos/{vid}", api_key, timeout=60))

    if video["status"] == "failed":
        raise gr.Error(f"Video failed: {json.dumps(video.get('error') or video, ensure_ascii=False)[:800]}")

    yield None, "Downloading video...", _debug(body, video)
    content = _call("GET", f"/v1/videos/{vid}/content", api_key).content
    status = f"Done in {time.time() - t0:.0f}s (id={vid})"
    if notes:
        status += " · " + "; ".join(notes)
    yield _save(content, ".mp4"), status, _debug(body, video)


# ------------------------------------------------------------------ tts
def on_tts_model(model):
    is_openai = model.startswith("gpt-")
    voices = OPENAI_VOICES if is_openai else GEMINI_VOICES
    return (
        gr.update(choices=voices, value=voices[0]),
        gr.update(visible=is_openai),
        gr.update(visible=is_openai),
    )


def gen_tts(api_key, model, text, voice, style, speed, fmt, extra_json):
    if not text.strip():
        raise gr.Error("Enter some text.")
    extra = _parse_extra(extra_json)
    body = {"model": model, "input": text, "voice": voice}
    if model.startswith("gpt-"):
        _put(body, "instructions", style.strip())
        if float(speed) != 1.0:
            body["speed"] = float(speed)
        _put(body, "response_format", fmt)
    elif style.strip():
        body["input"] = f"{style.strip()}: {text}"
    body.update(extra)
    t0 = time.time()
    r = _call("POST", "/audio/speech", api_key, json_body=body)
    return (
        _save(r.content, _audio_ext(r.content)),
        f"Done in {time.time() - t0:.1f}s ({len(r.content) / 1024:.0f} KB)",
        _debug(body, {"content_type": r.headers.get("content-type"), "bytes": len(r.content)}),
    )


# ------------------------------------------------------------------ stt
def on_stt_model(model):
    whisper = model == "whisper-1"
    if model == "gpt-transcribe":  # BTC docs: must send response_format=json
        formats, value = ["json"], "json"
    else:
        formats = [AUTO, "json", "text", "srt", "verbose_json", "vtt"] if whisper else [AUTO, "json"]
        value = AUTO
    return (
        gr.update(choices=formats, value=value),
        gr.update(visible=whisper),
        gr.update(visible=whisper),
    )


def run_stt(api_key, model, audio_path, lang, prompt, fmt, temperature, granularities, extra_json):
    if not audio_path:
        raise gr.Error("Upload or record some audio.")
    extra = _parse_extra(extra_json)
    data = {"model": model}
    _put(data, "language", lang)
    _put(data, "prompt", prompt.strip())
    if model == "gpt-transcribe":  # BTC docs: required, 400 without it
        fmt = "json"
    _put(data, "response_format", fmt)
    if model == "whisper-1" and temperature:
        data["temperature"] = str(temperature)
    data.update(_form(extra))
    if granularities and fmt == "verbose_json":
        data["timestamp_granularities[]"] = list(granularities)
    t0 = time.time()
    with open(audio_path, "rb") as f:
        r = _call(
            "POST", "/audio/transcriptions", api_key,
            data=data, files={"file": (os.path.basename(audio_path), f.read())},
        )
    try:
        j = r.json()
        text = j.get("text", "") if isinstance(j, dict) else str(j)
    except ValueError:
        j, text = {"_raw": r.text}, r.text
    return text, f"Done in {time.time() - t0:.1f}s", _debug(data, j)


# ------------------------------------------------------------------ API snippets
# Code samples mirror the examples in the BTC docs (same URLs, same base_url per SDK example),
# so only documented fields appear. Placeholders are used for the key, never a real one.
KEY_PLACEHOLDER = "<your_api_key>"
DOC_RATIOS = ["1:1", "3:4", "4:3", "16:9", "9:16"]  # values listed in the BTC image docs
DOC_VIDEO_SIZES = ["1280x720", "1920x1080", "720x1280", "1080x1920"]
CHAT_METHOD = "Chat completions"
STANDARD_METHOD = "Images API"


def _kind(model: str) -> str:
    if model in IMAGE_SPECS:
        return "image-" + IMAGE_SPECS[model]["kind"]
    if model in VIDEO_MODELS:
        return "video"
    return "tts" if model in TTS_MODELS else "stt"


def _q(s) -> str:
    """Python / JSON string literal."""
    return json.dumps(s, ensure_ascii=False)


def _fill(tpl: str, **kw) -> str:
    for k, v in kw.items():
        tpl = tpl.replace(f"@@{k}@@", str(v))
    return tpl.strip("\n") + "\n"


def _snip_image_google(model, prompt, ratio, method):
    common = dict(BASE=BASE_URL, KEY=KEY_PLACEHOLDER, MODEL=_q(model), PROMPT=_q(prompt))
    if method == CHAT_METHOD:
        body = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        kw = dict(common, BODY=shlex.quote(json.dumps(body, ensure_ascii=False, indent=2)),
                  DATA=json.dumps(body, ensure_ascii=False, indent=4))
        curl = _fill('''
curl -s @@BASE@@/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer @@KEY@@" \\
  -d @@BODY@@ \\
  | jq -r '.choices[0].message.images[0].image_url.url' \\
  | sed 's/^data:image\\/png;base64,//' | base64 --decode > image.png
''', **kw)
        req = _fill('''
import base64
import requests

url = "@@BASE@@/v1/chat/completions"
headers = {"Authorization": "Bearer @@KEY@@"}
data = @@DATA@@

r = requests.post(url, headers=headers, json=data, timeout=300)
r.raise_for_status()
uri = r.json()["choices"][0]["message"]["images"][0]["image_url"]["url"]
with open("image.png", "wb") as f:
    f.write(base64.b64decode(uri.split(",", 1)[-1]))
''', **kw)
        sdk = _fill('''
import base64
from openai import OpenAI

client = OpenAI(api_key="@@KEY@@", base_url="@@BASE@@/v1")

resp = client.chat.completions.create(
    model=@@MODEL@@,
    messages=[{"role": "user", "content": @@PROMPT@@}],
    modalities=["image"],  # return image data
)
uri = resp.choices[0].message.images[0].get("image_url").get("url")
with open("image.png", "wb") as f:
    f.write(base64.b64decode(uri.split(",", 1)[-1]))
''', **kw)
        return curl, req, sdk

    body = {"model": model, "prompt": prompt, "aspect_ratio": ratio}
    kw = dict(common, RATIO=_q(ratio), BODY=shlex.quote(json.dumps(body, ensure_ascii=False, indent=2)),
              DATA=json.dumps(body, ensure_ascii=False, indent=4))
    curl = _fill('''
curl -s @@BASE@@/v1/images/generations \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer @@KEY@@" \\
  -d @@BODY@@ \\
  | jq -r '.data[0].b64_json' | base64 --decode > image.png
''', **kw)
    req = _fill('''
import base64
import requests

url = "@@BASE@@/v1/images/generations"
headers = {"Authorization": "Bearer @@KEY@@"}
data = @@DATA@@

r = requests.post(url, headers=headers, json=data, timeout=300)
r.raise_for_status()
with open("image.png", "wb") as f:
    f.write(base64.b64decode(r.json()["data"][0]["b64_json"]))
''', **kw)
    sdk = _fill('''
import base64
from openai import OpenAI

client = OpenAI(api_key="@@KEY@@", base_url="@@BASE@@/v1")

resp = client.images.generate(
    model=@@MODEL@@,
    prompt=@@PROMPT@@,
    extra_body={"aspect_ratio": @@RATIO@@},
)
with open("image.png", "wb") as f:
    f.write(base64.b64decode(resp.data[0].b64_json))
''', **kw)
    return curl, req, sdk


def _snip_image_openai(model, prompt, size, quality):
    body = {"model": model, "prompt": prompt, "size": size, "quality": quality}
    kw = dict(
        BASE=BASE_URL, KEY=KEY_PLACEHOLDER, MODEL=_q(model), PROMPT=_q(prompt), SIZE=_q(size),
        QUALITY=_q(quality), BODY=shlex.quote(json.dumps(body, ensure_ascii=False, indent=2)),
        DATA=json.dumps(body, ensure_ascii=False, indent=4),
    )
    curl = _fill('''
curl -s @@BASE@@/images/generations \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer @@KEY@@" \\
  -d @@BODY@@ \\
  | jq -r '.data[0].b64_json' | base64 --decode > image.png
''', **kw)
    req = _fill('''
import base64
import requests

url = "@@BASE@@/images/generations"
headers = {"Authorization": "Bearer @@KEY@@"}
data = @@DATA@@

r = requests.post(url, headers=headers, json=data, timeout=300)
r.raise_for_status()
with open("image.png", "wb") as f:
    f.write(base64.b64decode(r.json()["data"][0]["b64_json"]))
''', **kw)
    sdk = _fill('''
import base64
from openai import OpenAI

client = OpenAI(api_key="@@KEY@@", base_url="@@BASE@@")

result = client.images.generate(
    model=@@MODEL@@,
    prompt=@@PROMPT@@,
    size=@@SIZE@@,
    quality=@@QUALITY@@,
)
with open("image.png", "wb") as f:
    f.write(base64.b64decode(result.data[0].b64_json))
''', **kw)
    return curl, req, sdk


def _snip_video(model, prompt, seconds, size, i2v):
    fields = {"model": model, "prompt": prompt, "seconds": str(seconds), "size": size}
    kw = dict(
        BASE=BASE_URL, KEY=KEY_PLACEHOLDER, MODEL=_q(model), PROMPT=_q(prompt), SECONDS=_q(str(seconds)),
        SIZE=_q(size), BODY=shlex.quote(json.dumps(fields, ensure_ascii=False, indent=2)),
        DATA=json.dumps(fields, ensure_ascii=False, indent=4), RAWSECONDS=seconds, RAWSIZE=size,
        RAWPROMPT=shlex.quote(prompt),
    )
    if i2v:
        create_curl = _fill('''
# 1) create (image-to-video: multipart/form-data with input_reference)
curl -X POST @@BASE@@/v1/videos \\
  -H "Authorization: Bearer @@KEY@@" \\
  -F model=@@MODEL_RAW@@ \\
  -F prompt=@@RAWPROMPT@@ \\
  -F seconds=@@RAWSECONDS@@ \\
  -F size=@@RAWSIZE@@ \\
  -F input_reference=@start.png
''', MODEL_RAW=shlex.quote(model), **kw).rstrip("\n")
        create_req = 'r = requests.post(\n    f"{BASE}/v1/videos",\n    headers=headers,\n    data=fields,\n    files={"input_reference": open("start.png", "rb")},\n)'
        create_sdk = _fill('''
video = client.videos.create(
    model=@@MODEL@@,
    prompt=@@PROMPT@@,
    seconds=@@SECONDS@@,
    size=@@SIZE@@,
    input_reference=open("start.png", "rb"),
)''', **kw).rstrip("\n")
    else:
        create_curl = _fill('''
# 1) create
curl -X POST @@BASE@@/v1/videos \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer @@KEY@@" \\
  -d @@BODY@@
''', **kw).rstrip("\n")
        create_req = 'r = requests.post(f"{BASE}/v1/videos", headers=headers, json=fields)'
        create_sdk = _fill('''
video = client.videos.create(
    model=@@MODEL@@,
    prompt=@@PROMPT@@,
    seconds=@@SECONDS@@,
    size=@@SIZE@@,
)''', **kw).rstrip("\n")

    curl = create_curl + "\n\n" + _fill('''
# -> {"id": "video_...", "status": "processing", ...}

# 2) poll until "status" is "completed" (or "failed")
curl @@BASE@@/v1/videos/<video_id> \\
  -H "Authorization: Bearer @@KEY@@"

# 3) download the mp4
curl @@BASE@@/v1/videos/<video_id>/content \\
  -H "Authorization: Bearer @@KEY@@" \\
  --output video.mp4
''', **kw)

    req = _fill('''
import time
import requests

BASE = "@@BASE@@"
headers = {"Authorization": "Bearer @@KEY@@"}
fields = @@DATA@@

# 1) create
@@CREATE@@
r.raise_for_status()
video_id = r.json()["id"]

# 2) poll until done
while True:
    status = requests.get(f"{BASE}/v1/videos/{video_id}", headers=headers).json()
    print(status["status"])
    if status["status"] in ("completed", "failed"):
        break
    time.sleep(10)
if status["status"] == "failed":
    raise SystemExit(status)

# 3) download
r = requests.get(f"{BASE}/v1/videos/{video_id}/content", headers=headers)
r.raise_for_status()
with open("video.mp4", "wb") as f:
    f.write(r.content)
''', CREATE=create_req, **kw)

    sdk = _fill('''
import time
from openai import OpenAI

client = OpenAI(api_key="@@KEY@@", base_url="@@BASE@@")

# 1) create
@@CREATE@@
print("created:", video.id)

# 2) poll until done
while video.status not in ("completed", "failed"):
    time.sleep(10)
    video = client.videos.retrieve(video.id)
    print("status:", video.status)
if video.status == "failed":
    raise SystemExit(f"failed: {video.error}")

# 3) download
content = client.videos.download_content(video.id)
content.write_to_file("video.mp4")
''', CREATE=create_sdk, **kw)
    return curl, req, sdk


def _snip_tts(model, text, voice):
    body = {"model": model, "input": text, "voice": voice}
    kw = dict(
        BASE=BASE_URL, KEY=KEY_PLACEHOLDER, MODEL=_q(model), TEXT=_q(text), VOICE=_q(voice),
        BODY=shlex.quote(json.dumps(body, ensure_ascii=False, indent=2)),
        DATA=json.dumps(body, ensure_ascii=False, indent=4),
    )
    curl = _fill('''
curl @@BASE@@/audio/speech \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer @@KEY@@" \\
  -d @@BODY@@ \\
  --output speech.mp3
''', **kw)
    req = _fill('''
import requests

url = "@@BASE@@/audio/speech"
headers = {"Authorization": "Bearer @@KEY@@"}
data = @@DATA@@

r = requests.post(url, headers=headers, json=data, stream=True, timeout=300)
r.raise_for_status()
with open("speech.mp3", "wb") as f:
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)
''', **kw)
    sdk = _fill('''
from openai import OpenAI

client = OpenAI(api_key="@@KEY@@", base_url="@@BASE@@")

response = client.audio.speech.create(
    model=@@MODEL@@,
    voice=@@VOICE@@,
    input=@@TEXT@@,
)
response.stream_to_file("speech.mp3")
''', **kw)
    return curl, req, sdk


def _snip_stt(model):
    needs_json = model == "gpt-transcribe"  # BTC docs: required, else 400
    kw = dict(BASE=BASE_URL, KEY=KEY_PLACEHOLDER, MODEL=_q(model), MODEL_RAW=shlex.quote(model))
    curl = _fill(
        "curl @@BASE@@/audio/transcriptions \\\n"
        '  -H "Authorization: Bearer @@KEY@@" \\\n'
        "  -F model=@@MODEL_RAW@@ \\\n"
        + ("  -F response_format=json \\\n" if needs_json else "")
        + "  -F file=@speech.mp3",
        **kw,
    )
    req = _fill('''
import requests

with open("speech.mp3", "rb") as f:
    r = requests.post(
        "@@BASE@@/audio/transcriptions",
        headers={"Authorization": "Bearer @@KEY@@"},
        data=@@DATA@@,
        files={"file": ("speech.mp3", f, "audio/mpeg")},
        timeout=300,
    )
r.raise_for_status()
print(r.json()["text"])
''', DATA=json.dumps({"model": model, **({"response_format": "json"} if needs_json else {})}), **kw)
    sdk = _fill('''
from openai import OpenAI

client = OpenAI(api_key="@@KEY@@", base_url="@@BASE@@")

with open("speech.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model=@@MODEL@@,
        file=audio_file,@@FORMAT@@
    )
print(transcript.text)
''', FORMAT='\n        response_format="json",' if needs_json else "", **kw)
    return curl, req, sdk


def _notes(model: str, kind: str, method: str) -> str:
    if kind == "image-google":
        lines = [
            "**Response:** base64 PNG. Images API: `data[0].b64_json`. Chat: "
            "`choices[0].message.images[0].image_url.url` (a `data:image/png;base64,...` URI).",
            "**Options (docs):** `aspect_ratio` = 1:1, 3:4, 4:3, 16:9, 9:16 (Images API only; "
            "`size` has no effect). One image per request (`n` accepts only 1).",
            "The docs' Chat samples send only `model` + `messages`; the SDK sample adds `modalities=[\"image\"]`.",
        ]
        if model == "nano-banana":
            lines.append("⚠️ Docs: Google stops supporting `nano-banana` (gemini-2.5-flash-image) from 02/10/2026.")
    elif kind == "image-openai":
        lines = [
            "**Response:** base64 in `data[0].b64_json`.",
            "**Options (docs):** `size` = 1024x1024, 1536x1024, 1024x1536; `quality` = low, medium, high "
            "(`low` is cheapest; ~$0.006 for a 1024x1024 low image on `gpt-image-2.5-flare`). "
            "No `aspect_ratio`. One image per request.",
        ]
    elif kind == "video":
        lines = [
            "**Async:** create → poll status until `completed` / `failed` → download the mp4 "
            "(about 30 s to a few minutes for 4–8 s clips).",
            "**Options (docs):** `seconds` = 4, 6, 8; `size` = 1280x720, 1920x1080 (16:9) or 720x1280, 1080x1920 (9:16); "
            "image-to-video = multipart `input_reference`.",
            "Price per second (docs): lite $0.05 (720p), fast $0.10 (720p) / $0.12 (1080p), full $0.40.",
        ]
    elif kind == "tts":
        voices = "OpenAI voices (alloy, echo, fable, onyx, nova, shimmer...), not Gemini voices like `Kore`" \
            if model.startswith("gpt-") else "Gemini voices (Zephyr, Puck, Charon, Kore...)"
        lines = [
            f"**Voice:** {model} uses {voices}.",
            "**Response:** audio file (mp3) in the response body, save it to disk.",
        ]
    else:
        lines = [
            "**Request:** `multipart/form-data` (file upload), not JSON.",
            "**Response:** `{\"text\": ..., \"usage\": {...}, \"task\": \"transcribe\"}`.",
        ]
        if model == "gpt-transcribe":
            lines.append("⚠️ `gpt-transcribe` requires `response_format=json`, otherwise the gateway returns 400.")
    lines.append("_Snippets use the key placeholder `<your_api_key>`. Fields outside the BTC docs are not included._")
    return "\n\n".join(lines)


def make_snippets(model, text, method, ratio, size_o, quality, seconds, vsize, i2v, voice):
    kind = _kind(model)
    text = text or ""
    if kind == "image-google":
        out = _snip_image_google(model, text, ratio, method)
    elif kind == "image-openai":
        out = _snip_image_openai(model, text, size_o, quality)
    elif kind == "video":
        out = _snip_video(model, text, seconds, vsize, i2v)
    elif kind == "tts":
        out = _snip_tts(model, text, voice)
    else:
        out = _snip_stt(model)
    return (*out, _notes(model, kind, method))


def on_snip_model(model):
    kind = _kind(model)
    voices = OPENAI_VOICES if model.startswith("gpt-") else GEMINI_VOICES
    labels = {"video": "Prompt", "tts": "Text", "image-google": "Prompt", "image-openai": "Prompt"}
    return (
        gr.update(visible=kind != "stt", label=labels.get(kind, "Prompt")),
        gr.update(visible=kind == "image-google"),   # method
        gr.update(visible=kind == "image-google"),   # aspect ratio
        gr.update(visible=kind == "image-openai"),   # size
        gr.update(visible=kind == "image-openai"),   # quality
        gr.update(visible=kind == "video"),          # seconds
        gr.update(visible=kind == "video"),          # video size
        gr.update(visible=kind == "video"),          # image-to-video
        gr.update(visible=kind == "tts", choices=voices, value=voices[0]),
    )


SNIPPET_MODELS = (
    [(f"Image · {m}", m) for m in IMAGE_SPECS]
    + [(f"Video · {m}", m) for m in VIDEO_MODELS]
    + [(f"Text to speech · {m}", m) for m in TTS_MODELS]
    + [(f"Speech to text · {m}", m) for m in STT_MODELS]
)
SNIPPET_DEFAULTS = ("nano-banana-2", "A majestic white tiger walking through a snowy forest",
                    STANDARD_METHOD, "16:9", "1024x1024", "low", "4", "1280x720", False, "Zephyr")


# ------------------------------------------------------------------ budget bar
# BTC docs (Kiểm tra chi tiêu): budget belongs to the team and is shared by every key.
# /key/info gives this key's spend + team_id; /team/info gives team spend + max_budget.
BUDGET_REFRESH_SECONDS = 30


def _money(x) -> str:
    return f"${x:,.2f}" if isinstance(x, (int, float)) else "?"


def _bar_html(spend=None, budget=None, scope="team", key_spend=None, note="", error="") -> str:
    with _session_lock:
        session = _session["cost"]
    now = datetime.now().strftime("%H:%M:%S")
    if error:
        main = f'<span class="bb-err">⚠️ {escape(error)}</span>'
        pct, color = 0, "var(--neutral-400)"
    elif isinstance(budget, (int, float)) and budget > 0 and isinstance(spend, (int, float)):
        left = budget - spend
        pct = max(0.0, min(100.0, spend / budget * 100))
        color = "#16a34a" if pct < 70 else "#d97706" if pct < 90 else "#dc2626"
        main = (
            f'<span class="bb-title">💰 {scope.title()} budget</span>'
            f"<span><b>{_money(spend)}</b> spent of {_money(budget)} ({pct:.1f}%)</span>"
            f'<span class="bb-left" style="color:{color}">{_money(left)} left</span>'
        )
    else:
        pct, color = 0, "var(--neutral-400)"
        main = (
            f'<span class="bb-title">💰 {scope.title()} spend</span>'
            f"<span><b>{_money(spend)}</b> spent · budget unknown</span>"
        )
    extra = [f"this key {_money(key_spend)}"] if key_spend is not None else []
    extra += [f"this app session {_money(session)}", f"updated {now}"]
    if note:
        extra.append(escape(note))
    return (
        f'<div class="bb"><div class="bb-row">{main}'
        f'<span class="bb-muted">{" · ".join(extra)}</span></div>'
        f'<div class="bb-track"><div class="bb-fill" style="width:{pct:.1f}%;background:{color}"></div></div></div>'
    )


def budget_bar(api_key) -> str:
    """Never raises: it runs on a timer, so errors are shown in the bar instead of popups."""
    try:
        info = _call("GET", "/key/info", api_key, timeout=20).json().get("info", {})
    except Exception as e:  # missing key, 401, network...
        return _bar_html(error=(getattr(e, "message", None) or str(e) or type(e).__name__)[:200])
    key_spend, team_id = info.get("spend"), info.get("team_id")
    if not team_id:
        return _bar_html(info.get("spend"), info.get("max_budget"), "key")
    try:
        team = _call("GET", f"/team/info?team_id={quote(team_id)}", api_key, timeout=20).json()
        ti = team.get("team_info", {})
        return _bar_html(ti.get("spend"), ti.get("max_budget"), "team", key_spend)
    except Exception as e:
        return _bar_html(key_spend, info.get("max_budget"), "key", note=f"team info unavailable: {str(e)[:80]}")


# ------------------------------------------------------------------ UI
THEME = gr.themes.Base(
    primary_hue="indigo",
    secondary_hue="violet",
    neutral_hue="slate",
    radius_size=gr.themes.sizes.radius_lg,
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
)

CSS = """
.gradio-container {max-width: 100% !important; padding: 18px 28px !important}
#app-title h1 {margin: 0; font-size: 1.6rem; font-weight: 700}
#app-title p {margin: 2px 0 0; opacity: .65}
[id^="panel-"] {border: 1px solid var(--border-color-primary); border-radius: 16px;
        padding: 18px !important; background: var(--background-fill-secondary)}
.gen-btn {height: 48px; font-size: 1rem; font-weight: 600}
.hint, .hint p {opacity: .65; font-size: .85rem}
.status {opacity: .8}
/* fal-style compact square thumbnails for reference images */
.ref-thumbs {height: auto !important; min-height: 0 !important}
.ref-thumbs .gallery-container {height: auto !important}
.ref-thumbs .grid-wrap {height: auto !important; min-height: 0 !important; max-height: 340px}
.ref-thumbs .grid-container {grid-template-columns: repeat(auto-fill, 76px) !important;
        grid-auto-rows: 76px !important; gap: 8px !important; padding: 36px 8px 8px !important;
        align-content: start !important}
.ref-thumbs .grid-container .gallery-item, .ref-thumbs .grid-container .thumbnail-item {width: 76px !important;
        height: 76px !important; aspect-ratio: 1 !important; border-radius: 10px !important}
.ref-thumbs .thumbnail-item img {object-fit: cover !important}
.ref-thumbs .thumbnail-item:hover {outline: 2px solid var(--color-accent)}
.ref-thumbs .delete-button {top: 4px !important; right: 4px !important; left: auto !important;
        bottom: auto !important; border-radius: 999px !important; opacity: 0;
        transition: opacity .15s}
.ref-thumbs .gallery-item:hover .delete-button {opacity: 1}
.ref-thumbs .upload-container {min-height: 130px}
.ref-thumbs .gallery-container:has(.preview) {height: 440px !important}
/* budget bar pinned to the top of every tab.
   Gradio sets overflow:hidden on .gradio-container, which disables position:sticky;
   overflow:clip still clips but does not create a scroll container. */
.gradio-container {overflow: clip !important}
#budget-bar {position: sticky; top: 0; z-index: 100; background: var(--body-background-fill);
        padding: 8px 0 !important; gap: 8px; align-items: center}
.bb {border: 1px solid var(--border-color-primary); border-radius: 12px; padding: 8px 14px;
        background: var(--background-fill-secondary)}
.bb-row {display: flex; flex-wrap: wrap; gap: 6px 16px; align-items: baseline; font-size: .95rem}
.bb-title {font-weight: 700}
.bb-left {font-weight: 700}
.bb-muted {opacity: .6; font-size: .82rem; margin-left: auto}
.bb-err {color: #dc2626}
.bb-track {height: 6px; border-radius: 999px; background: var(--neutral-200); margin-top: 6px; overflow: hidden}
.bb-fill {height: 100%; border-radius: 999px; transition: width .4s}
"""

RAW_HINT = (
    '<span class="hint">Sent as-is to the gateway (merged into the request body). '
    "If the gateway rejects a field, the error is shown verbatim.</span>"
)


with gr.Blocks(title="AITC Playground", fill_width=True) as demo:
    with gr.Row(equal_height=True):
        with gr.Column(scale=3):
            gr.Markdown(
                f"# AITC Playground\nGateway: `{BASE_URL}` — Image · Video · Speech  \n"
                "Options marked *not in BTC docs* default to **auto** / empty = not sent.",
                elem_id="app-title",
            )
        with gr.Column(scale=2, min_width=320):
            api_key = gr.Textbox(
                label="API key",
                type="password",
                value=ENV_KEY,
                placeholder="Defaults to AITC_API_KEY",
            )

    with gr.Row(elem_id="budget-bar", equal_height=True):
        budget = gr.HTML('<div class="bb">💰 Loading budget…</div>')
        budget_btn = gr.Button("↻", size="sm", scale=0, min_width=44)
    budget_timer = gr.Timer(BUDGET_REFRESH_SECONDS)
    _refresh = dict(fn=budget_bar, inputs=api_key, outputs=budget, show_progress="hidden")
    budget_timer.tick(**_refresh)
    budget_btn.click(**_refresh)
    api_key.blur(**_refresh)
    demo.load(**_refresh)

    with gr.Tabs():
        # ============================== IMAGE
        with gr.Tab("🖼️  Image"):
            with gr.Row(equal_height=False):
                with gr.Column(scale=2, min_width=480, elem_id="panel-0"):
                    i_model = gr.Dropdown(list(IMAGE_SPECS), value="nano-banana-2", label="Model")
                    i_prompt = gr.Textbox(label="Prompt", lines=8, max_lines=30)
                    i_refs = ref_uploader("Reference images (not in BTC docs)", 14)
                    i_n = gr.Slider(1, 4, value=1, step=1, label="Number of images")

                    with gr.Column(visible=True) as i_google:
                        with gr.Row():
                            i_ratio = gr.Dropdown(GOOGLE_RATIOS, value="1:1", label="Aspect ratio")
                            i_size_g = gr.Dropdown(
                                [AUTO] + IMAGE_SPECS["nano-banana-2"]["sizes"],
                                value=AUTO,
                                label="Resolution (not in BTC docs)",
                            )
                    with gr.Column(visible=False) as i_openai:
                        with gr.Row():
                            i_size_o = gr.Dropdown(OPENAI_SIZES, value="1024x1024", label="Size")
                            i_quality = gr.Dropdown(
                                [AUTO, "low", "medium", "high"], value="low", label="Quality"
                            )
                        with gr.Row():
                            i_bg = gr.Dropdown(
                                [AUTO, "opaque", "transparent"],
                                value=AUTO,
                                label="Background (not in BTC docs)",
                            )
                            i_fmt = gr.Dropdown(
                                [AUTO, "png", "jpeg", "webp"], value=AUTO, label="Format (not in BTC docs)"
                            )
                        with gr.Row():
                            i_comp = gr.Slider(0, 100, value=90, step=1, label="Compression (jpeg/webp)")
                            i_mod = gr.Dropdown(
                                [AUTO, "low"], value=AUTO, label="Moderation (not in BTC docs)"
                            )

                    with gr.Accordion("Advanced: raw parameters (JSON)", open=False):
                        i_extra = gr.Textbox(lines=3, show_label=False, placeholder='{"seed": 42}')
                        gr.HTML(RAW_HINT)
                    i_btn = gr.Button("Generate", variant="primary", elem_classes="gen-btn")

                with gr.Column(scale=3, elem_id="panel-1"):
                    i_out = gr.Gallery(
                        label="Result",
                        interactive=False,
                        preview=True,
                        object_fit="contain",
                        height=640,
                        columns=2,
                    )
                    i_status = gr.Markdown(elem_classes="status")
                    with gr.Accordion("Request / Response", open=False):
                        i_debug = gr.Code(language="json", interactive=False, show_label=False)

            i_model.change(on_image_model, i_model, [i_google, i_openai, i_size_g])
            i_btn.click(
                gen_image,
                [
                    api_key, i_model, i_prompt, i_n, i_ratio, i_size_g, i_size_o, i_quality,
                    i_bg, i_fmt, i_comp, i_mod, i_refs, i_extra,
                ],
                [i_out, i_status, i_debug],
            ).then(**_refresh)

        # ============================== VIDEO
        with gr.Tab("🎬  Video"):
            with gr.Row(equal_height=False):
                with gr.Column(scale=2, min_width=480, elem_id="panel-2"):
                    v_model = gr.Dropdown(VIDEO_MODELS, value=VIDEO_MODELS[0], label="Model")
                    v_prompt = gr.Textbox(
                        label="Prompt (dialogue and sound cues allowed)", lines=8, max_lines=30
                    )
                    v_neg = gr.Textbox(label="Negative prompt (not in BTC docs; empty = not sent)", lines=2)
                    with gr.Row():
                        v_ratio = gr.Radio(["16:9", "9:16"], value="16:9", label="Aspect ratio")
                        v_res = gr.Radio(
                            ["720p", "1080p", "4k"], value="720p", label="Resolution (4k not in BTC docs)"
                        )
                    with gr.Row():
                        v_sec = gr.Radio(["4", "6", "8"], value="4", label="Duration (seconds)")
                        v_audio = gr.Radio(
                            [AUTO, "on", "off"], value=AUTO, label="Generate audio (not in BTC docs)"
                        )
                    with gr.Row():
                        v_first = gr.Image(label="First frame (image-to-video)", type="filepath", height=180)
                        v_last = gr.Image(
                            label="Last frame (not in BTC docs)", type="filepath", height=180
                        )
                    v_refs = ref_uploader("Reference images (not in BTC docs)", 3)
                    # Textbox, not gr.Number: in Gradio 6 Number(value=None) shows and sends 0.
                    v_seed = gr.Textbox(
                        label="Seed (not in BTC docs; empty = not sent)", placeholder="e.g. 42"
                    )
                    gr.HTML(
                        '<span class="hint">1080p / 4k / reference images / last frame require 8s — '
                        "the app sets it automatically.</span>"
                    )
                    with gr.Accordion("Advanced: raw parameters (JSON)", open=False):
                        v_extra = gr.Textbox(
                            lines=3, show_label=False, placeholder='{"personGeneration": "allow_adult"}'
                        )
                        gr.HTML(RAW_HINT)
                    v_cost = gr.Markdown(est_cost(VIDEO_MODELS[0], "4", "720p"))
                    v_btn = gr.Button("Generate", variant="primary", elem_classes="gen-btn")

                with gr.Column(scale=3, elem_id="panel-3"):
                    v_out = gr.Video(label="Result", height=520, autoplay=True)
                    v_status = gr.Markdown(elem_classes="status")
                    with gr.Accordion("Request / Response", open=False):
                        v_debug = gr.Code(language="json", interactive=False, show_label=False)

            for c in (v_model, v_sec, v_res):
                c.change(est_cost, [v_model, v_sec, v_res], v_cost)
            v_btn.click(
                gen_video,
                [
                    api_key, v_model, v_prompt, v_neg, v_ratio, v_res, v_sec, v_audio, v_seed,
                    v_first, v_last, v_refs, v_extra,
                ],
                [v_out, v_status, v_debug],
            ).then(**_refresh)

        # ============================== TTS
        with gr.Tab("🔊  Text to Speech"):
            with gr.Row(equal_height=False):
                with gr.Column(scale=2, min_width=480, elem_id="panel-4"):
                    t_model = gr.Dropdown(TTS_MODELS, value=TTS_MODELS[0], label="Model")
                    t_voice = gr.Dropdown(
                        GEMINI_VOICES, value="Zephyr", label="Voice", allow_custom_value=True
                    )
                    t_text = gr.Textbox(
                        label="Text",
                        lines=10,
                        max_lines=30,
                        value="Xin chào, đây là một thử nghiệm chuyển văn bản thành giọng nói.",
                    )
                    t_style = gr.Textbox(
                        label="Style / instructions (optional)",
                        placeholder="e.g. Say cheerfully / Speak slowly, like a bedtime story",
                        info="gpt-4o-mini-tts: sent as `instructions` (not in BTC docs). "
                        "Gemini: prepended to the text. Empty = nothing added.",
                    )
                    t_speed = gr.Slider(
                        0.25, 4.0, value=1.0, step=0.05,
                        label="Speed (not in BTC docs; 1.0 = not sent)", visible=False,
                    )
                    t_fmt = gr.Dropdown(
                        TTS_FORMATS, value=AUTO, label="Format (not in BTC docs; BTC returns mp3)",
                        visible=False,
                    )
                    with gr.Accordion("Advanced: raw parameters (JSON)", open=False):
                        t_extra = gr.Textbox(lines=3, show_label=False, placeholder="{}")
                        gr.HTML(RAW_HINT)
                    t_btn = gr.Button("Generate", variant="primary", elem_classes="gen-btn")

                with gr.Column(scale=3, elem_id="panel-5"):
                    t_out = gr.Audio(label="Result", type="filepath")
                    t_status = gr.Markdown(elem_classes="status")
                    with gr.Accordion("Request / Response", open=False):
                        t_debug = gr.Code(language="json", interactive=False, show_label=False)

            t_model.change(on_tts_model, t_model, [t_voice, t_speed, t_fmt])
            t_btn.click(
                gen_tts,
                [api_key, t_model, t_text, t_voice, t_style, t_speed, t_fmt, t_extra],
                [t_out, t_status, t_debug],
            ).then(**_refresh)

        # ============================== STT
        with gr.Tab("📝  Speech to Text"):
            with gr.Row(equal_height=False):
                with gr.Column(scale=2, min_width=480, elem_id="panel-6"):
                    s_model = gr.Dropdown(STT_MODELS, value=STT_MODELS[0], label="Model")
                    s_audio = gr.Audio(
                        label="Audio", type="filepath", sources=["upload", "microphone"]
                    )
                    with gr.Row():
                        s_lang = gr.Dropdown(
                            STT_LANGS, value=AUTO, label="Language (not in BTC docs)"
                        )
                        s_fmt = gr.Dropdown([AUTO, "json"], value=AUTO, label="Response format")
                    s_prompt = gr.Textbox(
                        label="Prompt hint (not in BTC docs; empty = not sent)",
                        lines=2,
                        info="Proper nouns, jargon... helps the model transcribe correctly.",
                    )
                    s_temp = gr.Slider(
                        0, 1, value=0, step=0.1, label="Temperature (not in BTC docs; 0 = not sent)",
                        visible=False,
                    )
                    s_gran = gr.CheckboxGroup(
                        ["word", "segment"],
                        label="Timestamp granularities (whisper-1 + verbose_json only)",
                        visible=False,
                    )
                    with gr.Accordion("Advanced: raw parameters (JSON)", open=False):
                        s_extra = gr.Textbox(lines=3, show_label=False, placeholder="{}")
                        gr.HTML(RAW_HINT)
                    s_btn = gr.Button("Transcribe", variant="primary", elem_classes="gen-btn")

                with gr.Column(scale=3, elem_id="panel-7"):
                    s_text = gr.Textbox(label="Transcript", lines=16, max_lines=40, buttons=["copy"])
                    s_status = gr.Markdown(elem_classes="status")
                    with gr.Accordion("Request / Response", open=False):
                        s_debug = gr.Code(language="json", interactive=False, show_label=False)

            s_model.change(on_stt_model, s_model, [s_fmt, s_gran, s_temp])
            s_btn.click(
                run_stt,
                [api_key, s_model, s_audio, s_lang, s_prompt, s_fmt, s_temp, s_gran, s_extra],
                [s_text, s_status, s_debug],
            ).then(**_refresh)

        # ============================== API SNIPPETS
        with gr.Tab("📋  API snippets"):
            _init = make_snippets(*SNIPPET_DEFAULTS)
            with gr.Row(equal_height=False):
                with gr.Column(scale=2, min_width=480, elem_id="panel-8"):
                    gr.Markdown(
                        "Pick a model to get ready-to-paste **cURL**, **Python requests** and "
                        "**OpenAI SDK** code, taken from the BTC docs examples."
                    )
                    n_model = gr.Dropdown(
                        SNIPPET_MODELS, value=SNIPPET_DEFAULTS[0], label="Model", filterable=True
                    )
                    n_text = gr.Textbox(label="Prompt", value=SNIPPET_DEFAULTS[1], lines=4, max_lines=12)
                    n_method = gr.Radio(
                        [STANDARD_METHOD, CHAT_METHOD], value=SNIPPET_DEFAULTS[2], label="Method"
                    )
                    n_ratio = gr.Dropdown(DOC_RATIOS, value=SNIPPET_DEFAULTS[3], label="Aspect ratio")
                    n_size = gr.Dropdown(
                        OPENAI_SIZES[1:], value=SNIPPET_DEFAULTS[4], label="Size", visible=False
                    )
                    n_quality = gr.Dropdown(
                        ["low", "medium", "high"], value=SNIPPET_DEFAULTS[5], label="Quality", visible=False
                    )
                    n_seconds = gr.Radio(
                        ["4", "6", "8"], value=SNIPPET_DEFAULTS[6], label="Duration (seconds)", visible=False
                    )
                    n_vsize = gr.Dropdown(
                        DOC_VIDEO_SIZES, value=SNIPPET_DEFAULTS[7], label="Video size", visible=False
                    )
                    n_i2v = gr.Checkbox(
                        value=SNIPPET_DEFAULTS[8], label="Image-to-video (input_reference)", visible=False
                    )
                    n_voice = gr.Dropdown(
                        GEMINI_VOICES, value=SNIPPET_DEFAULTS[9], label="Voice",
                        allow_custom_value=True, visible=False,
                    )

                with gr.Column(scale=3, elem_id="panel-9"):
                    with gr.Tabs():
                        with gr.Tab("cURL"):
                            n_curl = gr.Code(_init[0], language="shell", interactive=False, show_label=False)
                        with gr.Tab("Python · requests"):
                            n_req = gr.Code(_init[1], language="python", interactive=False, show_label=False)
                        with gr.Tab("Python · OpenAI SDK"):
                            n_sdk = gr.Code(_init[2], language="python", interactive=False, show_label=False)
                    n_notes = gr.Markdown(_init[3])

            _controls = [n_model, n_text, n_method, n_ratio, n_size, n_quality, n_seconds, n_vsize, n_i2v, n_voice]
            _outs = [n_curl, n_req, n_sdk, n_notes]
            n_model.change(
                on_snip_model, n_model,
                [n_text, n_method, n_ratio, n_size, n_quality, n_seconds, n_vsize, n_i2v, n_voice],
            ).then(make_snippets, _controls, _outs)
            for _c in _controls[1:]:
                _c.change(make_snippets, _controls, _outs)

if __name__ == "__main__":
    demo.queue().launch(theme=THEME, css=CSS)
