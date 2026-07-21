# 단어 카드 학습 웹앱 (스타터)

자녀용 영어 단어 카드 학습 앱. 정적 사이트로 GitHub Pages에 배포한다.
사진 판독은 앱이 하지 않는다 — Claude 대화에서 판독·검증한 단어를 이 리포에 데이터로 넣는다.

## 폴더 구조
```
.
├─ index.html                  # 학습 웹앱 (카드 학습·오답 복습)
├─ paper.html                  # 인쇄용 지필 시험지 (DAY당 2장, 브라우저 인쇄로 PDF 저장)
├─ data/
│  ├─ index.json               # DAY 목록(최신순) — 앱이 먼저 읽음
│  └─ day09.json ~ day12.json  # DAY별 단어
├─ scripts/
│  └─ import_words.py          # words.json → data/dayNN.json + index 재생성
└─ docs/
   ├─ IMPLEMENTATION_SPEC.md   # 구현 명세 (먼저 읽을 것)
   ├─ mockup.html              # 확정된 UX 프로토타입 (시각/동작 기준)
   └─ chime-lab.html           # 출제 종소리 후보 시청·음량 조정 도구
```

## 새 DAY 추가 워크플로
1. Claude 대화(모바일 가능)에서 단어장 사진을 판독·검증 → `words.json` 생성.
2. 그 words.json을 리포 루트에 두고:
   ```
   python scripts/import_words.py words.json
   ```
   → `data/dayNN.json` 저장 + `data/index.json` 재생성(최신 DAY가 위).
3. 변경분 커밋·푸시. GitHub Pages에 반영되면 자녀 기기에서 새 DAY가 보인다.
   - "바로 반영"을 위해 앱의 데이터 fetch에 캐시 무효화가 있어야 함(명세 7절).

### 모바일에서 추가할 때 (확정 워크플로)
1. 모바일 Claude 앱 대화에서 단어장 사진 판독·검증 → words.json 내용 생성.
2. **Claude Code 웹**(claude.ai/code 또는 모바일 앱 Code 탭)에서 이 리포로 세션 열기.
3. JSON을 프롬프트에 붙여넣고 지시: "words.json으로 저장하고 `python scripts/import_words.py words.json` 실행 후 커밋·푸시".
   - 클라우드 세션에 파일 첨부는 안 됨 — 텍스트 붙여넣기가 표준. 샌드박스에 Python 내장.
4. 웹 세션은 main 직접 push가 차단되어 **브랜치 push + PR 생성**까지 진행됨.
5. GitHub 모바일(앱/웹)에서 **PR merge 1탭** → Pages 자동 재배포 → 자녀 기기 즉시 반영.

## 상태 (2026-07-21)
`index.html` 구현 완료·배포됨 → https://codetherabbit.github.io/vocab-quiz/
- data/*.json fetch + 캐시 무효화, localStorage(설정·누적 오답·마지막 범위·방향 이력), 오답 복습, 발음 속도 설정
- **출제 신호음**: 한글 문제에 상승 3음 종소리('반짝'). 후보 비교는 `docs/chime-lab.html`
- **출제 방향**: 세션 EK:KE 5:5 + 단어별 세션 간 교대(`vq.dirHist`)
- **인쇄 시험지**: `paper.html` — DAY당 2장(시험지1·2), 브라우저 인쇄로 PDF 저장
- 확정된 설계 결정은 `docs/IMPLEMENTATION_SPEC.md` 6절·9절·10절 참조

## 원칙 (지킬 것)
- 백엔드·API 키 없음(정적·무료). 빌드 단계 없음, 외부 라이브러리 없음.
- 판독은 앱 밖(대화 게이트)에서. 데이터엔 원자료 저장, 표기 변환은 표시 단계에서만.
- `dayNN.json`의 `ko`는 **원자료 그대로 보존** — 품사 박스·개행 같은 표기는 데이터에 굳히지 말 것.
  표기 규칙이 바뀌어도 데이터를 다시 만들지 않기 위해서다.
