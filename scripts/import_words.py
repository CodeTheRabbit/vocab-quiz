#!/usr/bin/env python3
"""
판독·검증을 통과한 words.json(그룹 형식)을 웹앱 데이터로 변환한다.
- 각 그룹(DAY)을 data/dayNN.json 으로 저장
- data/index.json 을 전체 data 폴더 기준으로 재생성(최신 DAY가 위)

입력 words.json 형식 (기존 파이프라인 산출물 그대로):
{ "groups": [ { "title": "DAY 09  Clothes", "words": [["en","뜻"], ...] }, ... ] }

사용: python scripts/import_words.py words.json
주의: 같은 번호의 dayNN.json 이 있으면 덮어쓴다(재출제가 아니라 데이터 갱신).
"""
import sys, os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "vocabulary")

def day_num(title):
    m = re.search(r'DAY\s*0*(\d+)', title, re.I)
    if not m:
        raise SystemExit(f"제목에서 DAY 번호를 찾을 수 없음: {title!r}")
    return int(m.group(1))

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "words.json"
    data = json.load(open(src, encoding="utf-8"))
    groups = data["groups"] if "groups" in data else [data]
    os.makedirs(DATA, exist_ok=True)
    for g in groups:
        title = g.get("title", "Vocabulary").strip()
        num = day_num(title)
        sub = re.sub(r'DAY\s*\d+\s*', '', title).strip()
        words = [{"en": e, "ko": k} for e, k in g["words"]]
        obj = {"id": num, "title": title, "subtitle": sub, "words": words}
        fname = f"day{num:02d}.json"
        json.dump(obj, open(os.path.join(DATA, fname), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"  data/{fname}  ({len(words)}단어)")
    rebuild_index()

def rebuild_index():
    days = []
    for path in glob.glob(os.path.join(DATA, "day*.json")):
        d = json.load(open(path, encoding="utf-8"))
        days.append({"id": d["id"], "file": os.path.basename(path),
                     "title": d["title"], "subtitle": d.get("subtitle", ""),
                     "count": len(d["words"])})
    days.sort(key=lambda x: x["id"], reverse=True)  # 최신이 위
    json.dump({"days": days}, open(os.path.join(DATA, "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"  data/index.json  ({len(days)} DAY, 최신순)")

if __name__ == "__main__":
    main()
