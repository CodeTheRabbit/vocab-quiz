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
├─ manifest.json                  # PWA 매니페스트 (홈화면 앱 이름·아이콘)
├─ sw.js                          # 서비스 워커 (network-first — 코드 자동 갱신·오프라인)
├─ assets/
│  ├─ codetherabbit-logo.svg      # 홈 하단 로고
│  ├─ app-icon.svg                # 파비콘
│  └─ apple-touch-icon.png        # 아이폰 홈화면 아이콘 (180px)
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
   ├─ prompt-vocabulary.md        # 단어 사진 → words.json 판독 규칙
   ├─ prompt-reading.md           # 독해 사진 → reading.json 판독 규칙
   └─ chime-lab.html              # 출제 종소리 시청·음량 조정 도구
```

## 새 데이터 추가 워크플로 (단어 · 독해 공통)

**권장 — Claude Code에 이미지 첨부 한 번으로:**
Claude Code(웹/앱)에서 이 리포 세션을 열고 **사진을 첨부**한 뒤 트리거 한마디면 끝난다.
- `dayNN 만들어줘`(또는 "단어 …") → 단어(Vocabulary)
- `unitNN 만들어줘`(또는 "독해 …") → 독해(Reading)

Claude가 첨부 이미지를 **직접 판독**해서 검증표를 보여주고 → `words.json`/`reading.json` 생성 →
import 스크립트 실행 → 배포까지 수행한다(규칙 전문은 리포 루트 `CLAUDE.md`).
- 번호·제목은 **이미지 머리글에서 읽는다**(예: `DAY 11  Jobs & Work`, `UNIT 07  Arts`). "NN"은 자리표시.
- 별도 모바일 대화에서 미리 판독할 필요 없다(옛 워크플로). 프롬프트 원문은 `docs/prompt-*.md` 참조.

**배포 분기(모드 감지 없음):** 먼저 `main` 직접 push를 시도하고 —
- 성공하면 곧바로 반영(비모바일·직접 권한 있음),
- 차단되면 브랜치 push + **PR 생성** 후 안내 → GitHub 모바일에서 **1탭 merge**(모바일).

앱의 데이터 fetch에 캐시 무효화(`?v=시각`)가 있어 반영되면 자녀 기기에서 바로 보인다.

**수동으로 돌릴 때(참고):**
```
python scripts/import_words.py words.json       # 단어  → data/vocabulary/dayNN.json + index
python scripts/import_reading.py reading.json    # 독해  → data/reading/unitNN.json + index
```
입력 파일 `words.json`·`reading.json`은 `.gitignore` 대상이라 커밋되지 않는다.

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
