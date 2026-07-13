# 단어 카드 학습 웹앱 (스타터)

자녀용 영어 단어 카드 학습 앱. 정적 사이트로 GitHub Pages에 배포한다.
사진 판독은 앱이 하지 않는다 — Claude 대화에서 판독·검증한 단어를 이 리포에 데이터로 넣는다.

## 폴더 구조
```
.
├─ index.html                  # 학습 웹앱 (Claude Code에서 mockup 기반으로 구현)
├─ data/
│  ├─ index.json               # DAY 목록(최신순) — 앱이 먼저 읽음
│  ├─ day09.json               # DAY별 단어
│  └─ day10.json
├─ scripts/
│  └─ import_words.py          # words.json → data/dayNN.json + index 재생성
└─ docs/
   ├─ IMPLEMENTATION_SPEC.md   # 구현 명세 (먼저 읽을 것)
   └─ mockup.html              # 확정된 UX 프로토타입 (시각/동작 기준)
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

### 모바일에서 추가할 때
- Claude Code는 데스크탑. 폰에서 넣을 때는 **GitHub 모바일 웹에서 파일 커밋**(붙여넣기)으로 처리.
- 즉석 시연만 필요하면 앱에 붙여넣기 입력(관리자용)을 두는 방안도 있음(선택).

## 다음 할 일 (Claude Code)
`docs/IMPLEMENTATION_SPEC.md`를 기준으로 `index.html`을 구현한다.
`docs/mockup.html`의 UX·스타일을 그대로 이식하되, 다음을 실제로 붙인다:
- data/*.json **fetch**(현재 mockup은 데이터가 인라인) + 캐시 무효화
- **localStorage** 저장(설정·오답·마지막 범위)
- 실기기 발음/레이아웃 확인

## 원칙 (지킬 것)
- 백엔드·API 키 없음(정적·무료).
- 판독은 앱 밖(대화 게이트)에서. 데이터엔 원자료 저장, 표기 변환은 표시 단계에서만.
- 인쇄 시험지 파이프라인과 데이터 공유 — dayNN.json의 `ko`를 임의로 가공하지 말 것.
