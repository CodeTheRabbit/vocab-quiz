# 영어 학습 웹앱 (단어 · 독해)

자녀용 영어 학습 앱. 정적 사이트로 GitHub Pages에 배포한다.
사진 판독은 앱이 하지 않는다 — Claude 대화에서 판독·검증한 단어를 이 리포에 데이터로 넣는다.

앱은 홈에서 **단어(Vocabulary) / 독해(Reading)** 두 메뉴로 나뉜다.
- **단어**: DAY별 단어를 카드로 학습(영↔한 섞어 출제). DAY 하나를 골라 바로 시작.
- **독해**: UNIT → 지문(소단원)으로 들어가 카드로 학습(**영→한 고정 · 번호 순서대로**).

## 폴더 구조
```
.
├─ index.html                     # 학습 웹앱 (홈 · 단어 · 독해 · 오답 복습)
├─ paper.html                     # 인쇄용 지필 시험지 (단어 전용)
├─ assets/
│  └─ codetherabbit-logo.svg      # 홈 하단 로고
├─ data/
│  ├─ vocabulary/                 # 단어(DAY)
│  │  ├─ index.json               #   DAY 목록(최신순)
│  │  └─ day09.json ~ day12.json  #   DAY별 단어
│  └─ reading/                    # 독해(UNIT)
│     ├─ index.json               #   UNIT 목록(최신순)
│     └─ unit07.json              #   UNIT별(지문 passages 포함) 단어
├─ scripts/
│  ├─ import_words.py             # words.json  → data/vocabulary/dayNN.json + index
│  └─ import_reading.py           # reading.json → data/reading/unitNN.json + index
└─ docs/
   ├─ IMPLEMENTATION_SPEC.md      # 구현 명세 (먼저 읽을 것)
   ├─ prompt-vocabulary.md        # 단어 사진 → words.json 프롬프트 (모바일 Claude용)
   ├─ prompt-reading.md           # 독해 사진 → reading.json 프롬프트 (모바일 Claude용)
   └─ chime-lab.html              # 출제 종소리 시청·음량 조정 도구
```

## 새 데이터 추가 워크플로 (단어 · 독해 공통)
1. **모바일 Claude 대화**에 단어장/어휘 리스트 **사진**을 첨부하고, 해당 프롬프트를 붙여넣어 JSON을 생성:
   - 단어(DAY): `docs/prompt-vocabulary.md` → `words.json`
   - 독해(UNIT): `docs/prompt-reading.md` → `reading.json`  (한 UNIT = JSON 한 개)
2. 그 JSON을 리포 루트에 저장하고 변환:
   ```
   python scripts/import_words.py words.json       # 단어
   python scripts/import_reading.py reading.json    # 독해
   ```
   → `data/…/…json` 저장 + 각 `index.json` 재생성(최신이 위).
3. 변경분 커밋·푸시 → GitHub Pages 반영 → 자녀 기기에서 자동으로 새 DAY/UNIT이 보인다.
   - 앱의 데이터 fetch에 캐시 무효화(`?v=시각`)가 있어 "커밋하면 바로 반영"된다.

### Claude Code 웹에서 추가할 때
1. 모바일 Claude 앱 대화에서 사진 판독·검증 → JSON 생성.
2. **Claude Code 웹**에서 이 리포로 세션 열기.
3. JSON을 붙여넣고 지시: "`words.json`(또는 `reading.json`)으로 저장하고 import 스크립트 실행 후 커밋·푸시".
4. 웹 세션은 main 직접 push가 차단되어 **브랜치 push + PR 생성**까지 진행됨.
5. GitHub 모바일에서 **PR merge 1탭** → Pages 자동 재배포 → 자녀 기기 즉시 반영.

## 상태 (2026-07-24)
배포 URL: https://codetherabbit.github.io/vocab-quiz/
- **홈 + 단어/독해 2메뉴** 구조. 모든 목록은 단일 선택 — **항목을 탭하면 바로 학습 시작**.
- **단어**: DAY 하나 학습, 영↔한 세션 5:5 + 단어별 세션 간 교대(`vq.dirHist`), 한글 문제엔 종소리.
- **독해**: UNIT→지문, **영→한 고정 · 순서대로**, 항상 영어가 앞면이라 발음 자동. 쿨 배경톤으로 구역 구분.
- **오답 복습**: 단어=DAY별 · 독해=지문별로 **분리 저장**. 각 목록 맨 아래 "최근 항목 오답" 한 줄(오답 있을 때만).
- **인쇄 시험지**(`paper.html`, 단어 전용): DAY 하나씩. 2단은 시험지1·2를 한 장에(정답면이라 잘라서/접어서 배부).
- 확정된 설계 결정은 `docs/IMPLEMENTATION_SPEC.md` 참조.

## 원칙 (지킬 것)
- 백엔드·API 키 없음(정적·무료). 빌드 단계 없음, 외부 라이브러리 없음.
- 판독은 앱 밖(대화 게이트)에서. 데이터엔 원자료 저장, 표기 변환은 표시 단계에서만.
- `data/**/*.json`의 `ko`는 **원자료 그대로 보존** — 품사 박스·개행 같은 표기는 데이터에 굳히지 말 것.
