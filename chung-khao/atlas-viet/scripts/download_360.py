"""Archive public panorama media and declarative metadata; never execute source JS.

Only downloads the three requested tours. Re-running verifies and reuses files
recorded in inventory.json. Media stay outside dist until integration is approved.
"""
import concurrent.futures
import hashlib
import json
import re
import ssl
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1] / "data" / "360-tours"
CONTEXT = ssl.create_default_context()
if Path("/etc/ssl/cert.pem").exists():
    CONTEXT = ssl.create_default_context(cafile="/etc/ssl/cert.pem")
ALLOWED_HOSTS = {"vietnam.travel", "www.airpano.com"}


def fetch(url):
    if urlparse(url).hostname not in ALLOWED_HOSTS:
        raise ValueError(f"Unexpected host: {url}")
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Referer": url})
            with urllib.request.urlopen(request, context=CONTEXT, timeout=60) as response:
                if urlparse(response.url).hostname not in ALLOWED_HOSTS:
                    raise ValueError(f"Unexpected redirect: {response.url}")
                return response.read(), response.headers.get_content_type()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    inventory_path = ROOT / "inventory.json"
    previous = {}
    if inventory_path.exists():
        previous = {item["path"]: item for item in json.loads(inventory_path.read_text())["files"]}
    jobs, files, failures, tours = {}, [], [], []

    def queue(tour, base, relative):
        if ".." in Path(relative).parts or relative.startswith("/"):
            raise ValueError(relative)
        path = f"{tour}/{relative}"
        jobs[path] = urljoin(base, relative)
        return path

    def source(tour, url, filename):
        content, mime = fetch(url)
        path = f"{tour}/source/{filename}"
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        files.append({"path": path, "url": url, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(), "content_type": mime})
        return content.decode("utf-8", errors="replace")

    # Store the original HTML/JS as inert .txt files. Do not mirror executables,
    # trackers or proprietary players. Extract the JSON definitions without eval.
    tour = "ninh-binh"
    base = "https://vietnam.travel/sites/default/files/360Tour/NinhBinh/"
    html = source(tour, base + "index.htm", "index.htm.txt")
    script = source(tour, base + "script.js", "script.js.txt")
    definitions = json.JSONDecoder().raw_decode(script.split('"definitions":', 1)[1].lstrip())[0]
    write_json(ROOT / tour / "source" / "definitions.json", definitions)
    refs = set(re.findall(r'''["']((?:media|loading)/[^"']+\.(?:jpg|jpeg|png|mp3|ogg|mp4|webm))["']''', script + html))
    for ref in sorted(refs):
        queue(tour, base, ref)
    objects = list(walk(definitions))
    titles = {}
    for obj in objects:
        if obj.get("class") == "HotspotPanoramaOverlayArea":
            target = re.search(r"this\.(panorama_[A-Z0-9_]+)", obj.get("click", ""))
            if target and obj.get("toolTip"):
                titles.setdefault(target.group(1), obj["toolTip"])
    scenes = []
    for obj in objects:
        if obj.get("class") != "Panorama":
            continue
        scene_id = obj["id"]
        frames = obj.get("frames", [])
        levels = frames[0]["sphere"]["levels"]
        scenes.append({"id": scene_id, "title": titles.get(scene_id, scene_id), "projection": "equirectangular", "hfov": obj["hfov"], "vfov": obj["vfov"], "preview": f'{tour}/{obj["thumbnailUrl"]}', "images": [{"path": f'{tour}/{level["url"]}', "width": level["width"], "height": level["height"]} for level in levels], "adjacent_scenes": obj.get("adjacentPanoramas", []), "overlays": frames[0].get("overlays", [])})
    tours.append({"id": tour, "title": "Ninh Bình", "source_url": base + "index.htm", "credit": "Vietnam.travel — Ninh Binh in 360", "rights": "No redistribution license verified; retain original credits and confirm rights before public hosting.", "source_security_note": "Original HTML includes a hidden BrowserUpdate.exe iframe. Stored as inert text only; no executable or source player was downloaded or executed.", "scenes": scenes})

    for tour, slug, title in [("ha-noi", "hanoi-vietnam", "Hà Nội"), ("ha-long", "halong-bay-vietnam", "Hạ Long")]:
        page = f"https://www.airpano.com/360photo/{slug}/"
        base = f"https://www.airpano.com/files/{slug}/"
        source(tour, page, "page.html.txt")
        xml = source(tour, base + "tour_hi.xml", "tour_hi.xml")
        source(tour, base + "tour_low.xml", "tour_low.xml")
        tree = ET.fromstring(xml)
        scenes = []
        settings = tree.find("tourSettings")
        for key, value in settings.attrib.items():
            if key.endswith("file") and key.startswith("sound"):
                for filename in value.split("|"):
                    queue(tour, base, settings.get("soundsurl", "sounds/") + filename)
        for scene in tree.findall("scene"):
            preview = scene.find("preview").get("url").replace("%CURRENTXML%/", "")
            queue(tour, base, preview)
            variants = {}
            for cube in scene.findall("image//cube"):
                pattern = cube.get("url").replace("%CURRENTXML%/", "")
                quality = pattern.split("/")[1]
                variants[quality] = {face: queue(tour, base, pattern.replace("%s", face)) for face in ["f", "b", "l", "r", "u", "d"]}
            latitude, longitude = float(scene.get("lat")), float(scene.get("lng"))
            coordinates_valid = 8 <= latitude <= 24 and 102 <= longitude <= 110
            scenes.append({"id": scene.get("name"), "title": scene.get("titleeng"), "projection": "cubemap", "preview": f"{tour}/{preview}", "variants": variants, "coordinates": {"latitude": latitude, "longitude": longitude, "plausible_for_vietnam": coordinates_valid}, "view": scene.find("view").attrib, "hotspots": [item.attrib for item in scene.findall("hotspot")]})
        tours.append({"id": tour, "title": title, "source_url": page, "embed_url": f"https://www.airpano.com/embed.php?3D={slug}", "credit": "Courtesy of www.AirPano.com", "rights": "Official page provides iframe embed with attribution; permission for redistributing downloaded media has not been verified.", "sound_credits": settings.attrib, "scenes": scenes})

    print(f"Discovered {sum(len(t['scenes']) for t in tours)} scenes, {len(jobs)} media files", flush=True)

    def download(item):
        path, url = item
        target = ROOT / path
        old = previous.get(path)
        if old and old["url"] == url and target.exists():
            content = target.read_bytes()
            if hashlib.sha256(content).hexdigest() == old["sha256"]:
                return old
        content, mime = fetch(url)
        suffix = target.suffix.lower()
        if suffix in {".jpg", ".jpeg"} and not content.startswith(b"\xff\xd8\xff"):
            raise ValueError("Invalid JPEG response")
        if suffix == ".png" and not content.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Invalid PNG response")
        if suffix in {".mp3", ".ogg"} and (mime.startswith("text/") or content.lstrip().startswith(b"<")):
            raise ValueError("Invalid audio response")
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".part")
        temporary.write_bytes(content)
        temporary.replace(target)
        return {"path": path, "url": url, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(), "content_type": mime}

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(download, item): item for item in jobs.items()}
        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            path, url = futures[future]
            try:
                files.append(future.result())
            except Exception as error:
                failures.append({"path": path, "url": url, "error": str(error)})
                print(f"Failed: {path}: {error}", flush=True)
            if count % 30 == 0 or count == len(jobs):
                print(f"Media {count}/{len(jobs)}; failures={len(failures)}", flush=True)
                write_json(inventory_path, {"files": sorted(files, key=lambda item: item["path"]), "failures": failures})

    for item in tours:
        item["download_status"] = "complete" if not any(f["path"].startswith(item["id"] + "/") for f in failures) else "partial"
        write_json(ROOT / item["id"] / "tour.json", item)
    write_json(ROOT / "manifest.json", {"downloaded_at": datetime.now(timezone.utc).isoformat(), "scope": "Public panorama media and metadata; original player runtime is excluded.", "tours": tours})
    write_json(inventory_path, {"files": sorted(files, key=lambda item: item["path"]), "failures": failures})
    print(json.dumps({"scenes": {t["id"]: len(t["scenes"]) for t in tours}, "files": len(files), "bytes": sum(f["bytes"] for f in files), "failures": len(failures)}, ensure_ascii=False), flush=True)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
