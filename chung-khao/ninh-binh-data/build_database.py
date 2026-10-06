"""Build a local SQLite knowledge seed and readable report using Python stdlib."""
import csv
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "seed.json").read_text(encoding="utf-8"))
sources = {s["id"]: s for s in data["sources"]}
assert len(sources) == len(data["sources"])
entities = {data["scope"]["province_id"]} | {p["id"] for p in data["places"]}
for group in ("overview_sections", "places", "facts", "dated_practical_info"):
    ids = [r["id"] for r in data[group]]
    assert len(ids) == len(set(ids)), group
    for record in data[group]:
        for source_id in record["source_ids"]:
            assert source_id in sources, source_id
            assert sources[source_id]["status"] == "source_checked", source_id
        if "entity_id" in record:
            assert record["entity_id"] in entities
        for source_id in record.get("address_source_ids", []):
            assert source_id in sources

# Build a fresh generated DB; source files remain the editable source of truth.
target = ROOT / "ninh_binh.sqlite"
temporary = ROOT / "ninh_binh.build.sqlite"
if temporary.exists():
    raise RuntimeError("Temporary database already exists; inspect it before rebuilding.")
db = sqlite3.connect(temporary)
db.execute("PRAGMA foreign_keys=ON")
db.executescript("""
CREATE TABLE metadata (key TEXT PRIMARY KEY, value_json TEXT NOT NULL);
CREATE TABLE sources (
 id TEXT PRIMARY KEY, title TEXT NOT NULL, publisher TEXT NOT NULL,
 url TEXT NOT NULL, displayed_date TEXT, accessed_on TEXT,
 status TEXT NOT NULL, note TEXT NOT NULL
);
CREATE TABLE entities (id TEXT PRIMARY KEY, name TEXT NOT NULL, kind TEXT NOT NULL);
CREATE TABLE places (
 id TEXT PRIMARY KEY REFERENCES entities(id), category TEXT NOT NULL,
 summary TEXT NOT NULL, status TEXT NOT NULL, current_address TEXT,
 address_status TEXT NOT NULL, latitude REAL, longitude REAL,
 opening_hours TEXT, data_json TEXT NOT NULL
);
CREATE TABLE knowledge (
 id TEXT PRIMARY KEY, entity_id TEXT NOT NULL REFERENCES entities(id),
 kind TEXT NOT NULL, topic TEXT NOT NULL, text TEXT NOT NULL,
 status TEXT NOT NULL, time_basis TEXT, value_json TEXT, unit TEXT,
 data_json TEXT NOT NULL
);
CREATE TABLE knowledge_sources (
 knowledge_id TEXT NOT NULL REFERENCES knowledge(id),
 source_id TEXT NOT NULL REFERENCES sources(id),
 PRIMARY KEY (knowledge_id, source_id)
);
CREATE TABLE place_sources (
 place_id TEXT NOT NULL REFERENCES places(id),
 source_id TEXT NOT NULL REFERENCES sources(id), role TEXT NOT NULL,
 PRIMARY KEY (place_id, source_id, role)
);
CREATE INDEX knowledge_entity_topic ON knowledge(entity_id, topic);
CREATE VIEW chatbot_knowledge AS
 SELECT * FROM knowledge
 WHERE kind IN ('fact', 'overview')
 AND status IN ('source_checked', 'dated_reference');
""")
encode = lambda value: json.dumps(value, ensure_ascii=False)
for key in ("schema_version", "researched_on", "language", "scope", "status_definitions",
            "editorial_guidelines", "chatbot_rules", "research_gaps"):
    db.execute("INSERT INTO metadata VALUES (?, ?)", (key, encode(data[key])))
for s in sources.values():
    db.execute("INSERT INTO sources VALUES (?,?,?,?,?,?,?,?)", tuple(s[k] for k in
               ("id", "title", "publisher", "url", "displayed_date", "accessed_on", "status", "note")))
db.execute("INSERT INTO entities VALUES (?,?,?)", ("ninh-binh", "Ninh Bình", "province"))
for p in data["places"]:
    db.execute("INSERT INTO entities VALUES (?,?,?)", (p["id"], p["name"], "place"))
    db.execute("INSERT INTO places VALUES (?,?,?,?,?,?,?,?,?,?)", (
        p["id"], p["category"], p["summary"], p["status"], p["current_address"],
        p["address_status"], p["latitude"], p["longitude"], p["opening_hours"], encode(p)))
    for role, field in (("content", "source_ids"), ("address", "address_source_ids")):
        for source_id in p.get(field, []):
            db.execute("INSERT INTO place_sources VALUES (?,?,?)", (p["id"], source_id, role))
for group, kind in (("overview_sections", "overview"), ("facts", "fact"),
                    ("dated_practical_info", "practical")):
    for r in data[group]:
        db.execute("INSERT INTO knowledge VALUES (?,?,?,?,?,?,?,?,?,?)", (
            r["id"], r.get("entity_id", "ninh-binh"), kind,
            r.get("topic", r.get("kind", r["id"])), r.get("text", r.get("label", "")),
            r.get("status", "source_checked"), r.get("time_basis", r.get("source_displayed_date")),
            encode(r.get("value")), r.get("unit"), encode(r)))
        for source_id in r["source_ids"]:
            db.execute("INSERT INTO knowledge_sources VALUES (?,?)", (r["id"], source_id))
db.commit()
assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
assert not db.execute("PRAGMA foreign_key_check").fetchall()
db.close()
temporary.replace(target)

with (ROOT / "sources.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(data["sources"][0]))
    writer.writeheader()
    writer.writerows(data["sources"])

def source_links(ids):
    return "; ".join(f'[{i}: {sources[i]["title"]}]({sources[i]["url"]})' for i in ids)

lines = ["# Bộ dữ liệu giới thiệu Ninh Bình", "", "Ngày đọc nguồn: 06/10/2026.", "",
         data["scope"]["coverage_label"], "",
         "Đây là bộ dữ liệu khởi đầu, không phải dữ liệu đầy đủ hoặc cập nhật trực tiếp. "
         "`source_checked` nghĩa là đã đọc nội dung nguồn, không phải mọi dữ kiện được xác minh độc lập.", "",
         "## Tệp dữ liệu", "",
         "- `seed.json`: dữ liệu gốc, có thể nạp vào web hoặc chuyển sang hệ quản trị khác.",
         "- `ninh_binh.sqlite`: database SQLite có bảng entities, places, knowledge, sources và liên kết nguồn.",
         "- `sources.csv`: danh mục liên kết nguồn, mở được trong công cụ bảng tính.",
         "- `build_database.py`: tạo lại SQLite, CSV và tài liệu từ JSON bằng Python chuẩn.", "",
         "Chạy lại: `python3 build_database.py` trong thư mục này. Chỉ sửa seed.json; SQLite là tệp sinh ra.", "",
         "## Nội dung tổng quan có thể sử dụng", ""]
for s in data["overview_sections"]:
    lines += [f'### {s["title"]}', "", s["text"], "", "Nguồn: " + source_links(s["source_ids"]), ""]
lines += ["## Hồ sơ địa danh", ""]
for p in data["places"]:
    lines += [f'### {p["name"]}', "", p["summary"], "",
              "Điểm nổi bật: " + "; ".join(p["highlights"]) + ".", "",
              "Nguồn: " + source_links(p["source_ids"]), "", "Ghi chú dữ liệu: " + p["note"], ""]
lines += ["## Giá và lịch tham khảo, chưa xác nhận hiện hành", "",
          "Không hiển thị các mục này như giá hoặc lịch hôm nay. Ngày đọc nguồn khác ngày có hiệu lực.", "",
          "| Điểm | Nội dung | Giá trị theo nguồn | Ngày nguồn hiển thị |",
          "|---|---|---|---|"]
for r in data["dated_practical_info"]:
    entity_name = next((p["name"] for p in data["places"] if p["id"] == r["entity_id"]), "Ninh Bình")
    lines.append(f'| {entity_name} | {r["label"]} | {r["value"]} {r["unit"] or ""} | {r["source_displayed_date"]} |')
lines += ["", "## Lưu ý khi tích hợp chatbot", ""]
lines += ["- " + rule for rule in data["chatbot_rules"]]
lines += ["", "View `chatbot_knowledge` chỉ lọc nội dung theo trạng thái, chưa thực hiện tìm kiếm hoặc "
          "kiểm soát câu trả lời. Backend vẫn phải lọc phạm vi câu hỏi, lấy nguồn, kiểm tra trích dẫn và xử lý thiếu dữ liệu.", "",
          "Ví dụ truy vấn nguồn cho một dữ kiện:", "", "```sql",
          "SELECT k.text, k.status, k.time_basis, s.title, s.url",
          "FROM chatbot_knowledge k",
          "JOIN knowledge_sources ks ON ks.knowledge_id = k.id",
          "JOIN sources s ON s.id = ks.source_id",
          "WHERE k.entity_id = 'hoa-lu';", "```", "",
          "## Các khoảng trống cần bổ sung", ""]
lines += ["- " + gap for gap in data["research_gaps"]]
lines += ["", "## Danh mục nguồn", ""]
for s in sources.values():
    lines += [f'### {s["id"]} · {s["title"]}', "",
              f'[{s["publisher"]}]({s["url"]}) · Trạng thái: `{s["status"]}`.', "", s["note"], ""]
lines += ["## Nguyên tắc biên tập", ""]
lines += ["- " + rule for rule in data["editorial_guidelines"]]
(ROOT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f'Created {target.name}: {len(data["places"])} places, '
      f'{len(data["facts"])} facts, {len(data["sources"])} source records. Integrity checks passed.')
