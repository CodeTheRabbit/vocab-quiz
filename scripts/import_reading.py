#!/usr/bin/env python3
"""
판독·검증을 통과한 reading.json(UNIT 형식)을 웹앱 데이터로 변환한다.
- 각 UNIT을 data/reading/unitNN.json 으로 저장
- data/reading/index.json 을 data/reading 폴더 기준으로 재생성(최신 UNIT이 위)

입력 reading.json 형식 (사진 판독 산출물):
{ "unit": "UNIT 07  Arts",
  "passages": [ { "title": "Glass Harmonica", "words": [["en","뜻"], ...] }, ... ] }
여러 UNIT을 한 번에: { "units": [ {위 형식}, ... ] }

사용: python scripts/import_reading.py reading.json
주의: 같은 번호의 unitNN.json 이 있으면 덮어쓴다(재출제가 아니라 데이터 갱신).

Vocabulary의 import_words.py 와 같은 방식 — 차이는 UNIT>지문(passages) 계층뿐이다.
`ko`(뜻)는 원자료 그대로 저장한다(품사 박스·개행 같은 표기는 표시 단계에서만).
"""
import sys, os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "reading")

def unit_num(title):
    m = re.search(r'UNIT\s*0*(\d+)', title, re.I)
    if not m:
        raise SystemExit(f"제목에서 UNIT 번호를 찾을 수 없음: {title!r}")
    return int(m.group(1))

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "reading.json"
    data = json.load(open(src, encoding="utf-8"))
    units = data["units"] if "units" in data else [data]
    os.makedirs(DATA, exist_ok=True)
    for u in units:
        title = u.get("unit", u.get("title", "UNIT")).strip()
        num = unit_num(title)
        sub = re.sub(r'UNIT\s*\d+\s*', '', title).strip()
        passages = []
        for i, p in enumerate(u["passages"], start=1):
            words = [{"en": e, "ko": k} for e, k in p["words"]]
            passages.append({"id": i, "title": p["title"].strip(), "words": words})
        obj = {"id": num, "title": title, "subtitle": sub, "passages": passages}
        fname = f"unit{num:02d}.json"
        json.dump(obj, open(os.path.join(DATA, fname), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        total = sum(len(p["words"]) for p in passages)
        print(f"  data/reading/{fname}  ({len(passages)}지문 · {total}단어)")
    rebuild_index()

def rebuild_index():
    units = []
    for path in glob.glob(os.path.join(DATA, "unit*.json")):
        u = json.load(open(path, encoding="utf-8"))
        total = sum(len(p["words"]) for p in u["passages"])
        units.append({"id": u["id"], "file": os.path.basename(path),
                      "title": u["title"], "subtitle": u.get("subtitle", ""),
                      "passages": len(u["passages"]), "count": total})
    units.sort(key=lambda x: x["id"], reverse=True)  # 최신이 위
    json.dump({"units": units}, open(os.path.join(DATA, "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"  data/reading/index.json  ({len(units)} UNIT, 최신순)")

if __name__ == "__main__":
    main()
