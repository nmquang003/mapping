"""Generate local narration MP3s through OpenRouter; never ship credentials.
Edit narration/*.json. Requires OPENROUTER_API_KEY, ffmpeg and ffprobe.
Raw and normalized audio are cached outside dist to avoid repeat API charges.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import shlex
import shutil
import ssl
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = 'https://openrouter.ai/api/v1/audio/speech'


def load_key():
    key = os.environ.get('OPENROUTER_API_KEY', '').strip()
    env_file = ROOT.parents[1]/'.env'
    if not key and env_file.is_file():
        for line in env_file.read_text().splitlines():
            name, separator, value = line.removeprefix('export ').partition('=')
            if separator and name.strip() == 'OPENROUTER_API_KEY':
                parts = shlex.split(value, comments=True)
                key = parts[0] if parts else ''
                break
    if not key:
        raise SystemExit('Set OPENROUTER_API_KEY in the environment or repository .env.')
    return key


def synthesize(region, chapter, key):
    body = {'model': region['model'], 'input': chapter['text'],
            'voice': region['voice'], 'response_format': 'pcm',
            'provider': {'options': {'google-ai-studio': {
                'speech_metadata': {'style': region['style']}}}}}
    context = ssl.create_default_context(cafile='/etc/ssl/cert.pem')
    for attempt in range(3):
        request = urllib.request.Request(ENDPOINT,
            data=json.dumps(body, ensure_ascii=False).encode(),
            headers={'Authorization': 'Bearer '+key, 'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(request, context=context, timeout=180) as response:
                mime = response.headers.get('Content-Type', '').split(';')[0]
                if mime not in ('audio/pcm', 'audio/L16', 'audio/l16', 'audio/wav', 'audio/x-wav', 'application/octet-stream'):
                    raise RuntimeError(f'Unexpected speech response type: {mime}')
                audio = response.read()
                if len(audio) < 10000:
                    raise RuntimeError('Speech response is empty or unexpectedly small.')
                return audio
        except urllib.error.HTTPError as error:
            # Never dump upstream response bodies or credentials into logs.
            if error.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(3*(attempt+1))
                continue
            raise RuntimeError(f'OpenRouter speech failed (HTTP {error.code}).') from None
        except urllib.error.URLError:
            # An ambiguous network timeout may have incurred a charge: no blind retry.
            raise RuntimeError('OpenRouter speech network error; rerun after checking service status.') from None
    raise RuntimeError('Speech generation did not complete.')


def render(job):
    region, chapter, key = job
    settings = {name: region[name] for name in ('provider', 'model', 'voice', 'style')}
    if settings['provider'] != 'openrouter' or not settings['model'].startswith('google/'):
        raise ValueError('This renderer requires an OpenRouter Google TTS configuration.')
    fingerprint = hashlib.sha256(json.dumps([chapter['text'], settings,
        'pcm24k-to-mp3-96k-loudnorm-v2'], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    directory = ROOT/'data/narration'/region['region_id']/chapter['id']
    directory.mkdir(parents=True, exist_ok=True)
    raw = directory/f'{fingerprint}-raw.pcm'
    output = directory/f'{fingerprint}.mp3'
    if not raw.is_file():
        print(f'Generating: {region["region_id"]}/{chapter["id"]}', flush=True)
        audio = synthesize(region, chapter, key)
        temporary = raw.with_suffix('.tmp')
        temporary.write_bytes(audio)
        temporary.replace(raw)
    if not output.is_file():
        with tempfile.TemporaryDirectory(prefix='atlas-narration-') as work:
            normalized = Path(work)/'speech.mp3'
            header = raw.read_bytes()[:12]
            input_format = [] if header[:4] == b'RIFF' and header[8:12] == b'WAVE' else ['-f', 's16le', '-ar', '24000', '-ac', '1']
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *input_format, '-i', str(raw),
                '-af', 'loudnorm=I=-18:TP=-2:LRA=7', '-ar', '44100', '-ac', '1',
                '-b:a', '96k', str(normalized)], check=True)
            shutil.copy2(normalized, output)
    duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(output)], text=True))
    if not 20 <= duration <= 180:
        raise ValueError(f'Unexpected narration duration for {region["region_id"]}/{chapter["id"]}: {duration:.1f}s')
    print(f'Ready: {region["region_id"]}/{chapter["id"]} ({duration:.0f}s)', flush=True)
    target = ROOT/'dist/assets/audio/narration'/region['region_id']/f'{chapter["id"]}.mp3'
    return output, target, {**chapter, 'src':str(target.relative_to(ROOT/'dist')),
        'duration':round(duration, 2), 'script_sha256':fingerprint}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', help='Prepare one region only; does not publish the catalog')
    parser.add_argument('--chapter', help='Prepare one chapter only; does not publish the catalog')
    args = parser.parse_args()
    for program in ['ffmpeg', 'ffprobe']:
        if not shutil.which(program):
            raise SystemExit(f'Missing {program}.')
    key = load_key()
    regions = [json.loads(path.read_text()) for path in sorted((ROOT/'narration').glob('*.json'))]
    catalog, prepared = {}, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for region in regions:
            if args.region and region['region_id'] != args.region:
                continue
            chapters = [c for c in region['chapters'] if not args.chapter or c['id'] == args.chapter]
            results = list(pool.map(render, [(region, c, key) for c in chapters]))
            prepared.extend(results)
            catalog[region['region_id']] = {'name':region['region_name'],
                'voice':region['voice'], 'model':region['model'], 'chapters':[r[2] for r in results]}
    if not prepared:
        raise SystemExit('No matching narration scripts.')
    if args.region or args.chapter:
        for output, _, _ in prepared:
            print(f'Preview: {output}')
        return
    # Publish only after every requested track has generated and decoded successfully.
    for output, target, _ in prepared:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(output, target)
    manifest = ROOT/'dist/narration-catalog.js'
    temporary = manifest.with_suffix('.tmp')
    temporary.write_text('// Generated by scripts/generate_narration.py; edit narration/*.json.\nexport const narrations = '
        +json.dumps(catalog, ensure_ascii=False, separators=(',', ':'))+';\n')
    temporary.replace(manifest)
    print(f'Published {len(prepared)} narration tracks and text/source catalog.')


if __name__ == '__main__':
    main()
