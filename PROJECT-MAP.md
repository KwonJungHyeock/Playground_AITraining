# PROJECT MAP — Eduino AI

> 이 파일 하나로 프로젝트 전체를 파악한다. 세부 작업 규칙은 `CLAUDE.md`, 기획 의도는 `docs/` 참조.

---

## 1. 한 줄 요약

**설치·가입·서버 없이 브라우저에서 AI를 직접 학습시키고 추론하는 교실용 학습 플랫폼.**
빌드 도구 없는 순수 HTML/CSS/JS 정적 사이트이며, 모든 학습·추론은 TensorFlow.js로 **기기 안에서(On-Device)** 끝난다.

---

## 2. 진입 구조 (가장 먼저 볼 것)

```
                    platform/index.html          ← 배포 루트 (/ → 여기로 리다이렉트)
                    "히어로 한 장" 랜딩
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
      일반 사용자모드                     수업전용 콘솔모드
      modules/index.html                  entry.html
              │                               │
    인공지능 사전진단 (30문항)        체험 / 수업개설 / 수업참여
              │                               │
    6개 코스 → 4단계 대시보드          console/map.html  (A · 스테이지 맵)
    ① 학습 미리보기                    console/cards.html (C · 카드 캐러셀)
    ② 이론 학습                               │
    ③ 실습 퀘스트  ──────────────────────────┘
    ④ 최종 평가                        실습은 stages/ 의 같은 엔진을 공유
```

추가로 **`index.html`(루트)** 은 "직접 제작 트랙 · VISION AI" — `stages/` 엔진을 직접 띄우는 실습 화면이다.
`studio.html` · `explore.html` · `create.html` 은 콘솔로 보내는 **라우터 스텁**(삭제 금지).

---

## 3. 폴더 지도

| 폴더 | 역할 | 핵심 파일 |
| --- | --- | --- |
| `platform/` | 랜딩 · 코스 상세 · 무료 샘플 | `index.html`, `course.html`, `sample.html`, `img/` |
| `modules/` | **일반 사용자모드** — 사전진단 + 6개 코스 | `index.html`, `shared/`, `<코스>/` |
| `console/` | **수업전용 콘솔모드** 허브 (A·C 2안) | `shared.js`(단일 소스), `map.html`, `cards.html` |
| `stages/` | **실습 엔진** — 실제 학습·추론이 도는 곳 | `trainer/`, `studio/`, `apps/`, `submission/`, `admin/`, `core/`, `styles/` |
| `shared/` | 무료·유료 접근 제어 공통 레이어 | `access.js`, `access.css` |
| `models/` | 로컬 호스팅 모델 | `movenet/` |
| `docs/` | 기획·설계·정책 문서 | `PRODUCT-PLAN.md`, `module-architecture.md`, `access-policy.md`, `AWS-BACKEND-NOTES.md` |
| `test/` | Node 테스트 러너 + jsdom | `*.test.mjs`, `manual/` |

### `modules/` 내부 (코스 하나 = 폴더 하나)

```
modules/
├── index.html              사전진단 허브 (6개 course-config 를 수집 스텁으로 읽음)
├── shared/
│   ├── course-dashboard.js/.css   4단계 셸 · 사이드바
│   ├── precheck-hub.js/.css       사전진단 30문항 흐름 · 4단계 결과
│   ├── course-preview.js          동작 미리보기 애니메이션 (단일 소스)
│   ├── base.css · components.css · icons.js
└── <concept|data|text|vision|gesture|life>/
    ├── index.html          코스 셸
    ├── course-config.js    ★ 콘텐츠 단일 소스 (이론 · precheck · quiz · 완주문구)
    ├── app.js              실습 로직
    ├── advanced.js         심화 실습
    └── style.css
```

### `stages/` 내부

| 하위 | 담당 |
| --- | --- |
| `trainer/` | 이미지·음성·동작 분류 학습기 (`trainer.core.js` 가 본체) |
| `studio/` | 만들기 도구 (`maker.js`, `imagelab.js`) |
| `apps/` | 단일 체험 앱 7종 — face · detect · skeleton · filter · colortrack · character-card · idea-board |
| `submission/` | 학생 제출 · 게시판 (`submit.core.js`, `board.js`) |
| `admin/` | 관리자 현황 · 수료증 (`admin.js`, `cert.js`) |
| `core/` | 세션 · 다이얼로그 · 이미지 저장소 · 아이콘 |
| `styles/` | `tokens.css`, `trainer.css`, `stage.css`, `studio.css` |

---

## 4. 기술 스택

- **빌드 없음** — 번들러·프레임워크·트랜스파일 전부 없음. 파일을 그대로 서빙하면 동작
- **TensorFlow.js** (CDN) — MobileNet v2(전이학습) · MoveNet · Speech Commands · COCO-SSD · BlazeFace · BodyPix
- **Electron** 포장 지원 — `npm run app`, `npm run dist`
- **Vercel** 정적 배포 — `vercel.json` 이 `/` → `/platform/index.html` 리다이렉트

```bash
npx serve .          # 로컬 확인 (카메라는 localhost 또는 https 필요)
npm test             # node --test test/*.test.mjs
npm run app          # Electron 데스크톱 앱
```

---

## 5. 데이터 · 상태 (서버 없음)

**백엔드가 없다.** 모든 상태는 브라우저 저장소에만 있고, 기기를 넘지 못한다.

| 키 | 저장소 | 내용 |
| --- | --- | --- |
| `vision_classes` / `vision_roster` | local | 교사가 만든 수업 · 명단 |
| `vision_missions` | local | 수업별 미션 |
| `vision_submissions` | local | 학생 제출물 (이미지 base64 인라인) |
| `vision_recent_joins` · `vision_student_name` | local | 재입장 · 본인 식별 |
| `vision_visited` · `vision_track` | local/session | 콘솔 진행 상태 · 마지막 트랙 |
| `vision_session` · `vos_pass` | session | 현재 역할 · 진입 토큰 |
| `eduino_plan` · `eduino_entitlements` | local | 무료/유료 · 코스 단품 구매 |

- **학습 기록은 저장하지 않는다** — `modules/` 의 사전진단·답안은 화면에만 남는다
- 멀티 기기 공유는 **백엔드 없이는 불가능** (교사 기기에서 만든 수업 코드를 학생 기기가 조회할 수 없음)
- 서버 전환 설계는 `docs/AWS-BACKEND-NOTES.md` 에 정리됨

---

## 6. 설계 원칙 (어기면 리뷰에서 걸린다)

1. **단일 소스** — 같은 데이터를 두 파일에 복붙하지 않는다
   - 코스 콘텐츠·진단 문항 → `modules/<코스>/course-config.js`
   - 콘솔 항목 → `console/shared.js` 의 `TRACKS`
   - 동작 미리보기 → `modules/shared/course-preview.js`
2. **URL 전부 유지** — 외부 링크·북마크가 걸려 있다
3. **지어낸 데이터 금지** — 측정값인 척하는 설계값을 쓰지 않는다
4. **잠금은 표시·이벤트 차단으로만** — 학습 콘텐츠·모델 로직은 건드리지 않는다
5. **CSS 클래스 접두사** — 콘솔 공통은 `v-`, 대시보드는 `dash-`, 사전진단은 `ph-`

---

## 7. 브랜치 · 배포

| 브랜치 | 내용 |
| --- | --- |
| `main` | 초안 |
| `V2` | 외부 개발자 리팩터 반영본 |
| `V3` | 메인 2진입 축소 + 통합 사전진단 (현재 운영 기준) |
| **`V4`** | **신규 — 새 형태의 AI 학습 콘텐츠 작업용** |

- 새 작업은 **반드시 새 브랜치**에서. 기존 브랜치는 그대로 둔다
- 커밋 메시지는 Conventional Commits (`.agents/AGENTS.md`)

---

## 8. 새 콘텐츠를 추가하려면 어디를 건드리나

| 만들려는 것 | 손대는 곳 |
| --- | --- |
| 새 코스 (4단계 대시보드형) | `modules/<새코스>/` 폴더 + `course-dashboard.js` 의 `COURSES` 배열 |
| 코스 내용만 수정 | 해당 `course-config.js` 한 파일 |
| 새 체험 앱 (단일 화면) | `stages/apps/<새앱>.html` |
| 콘솔 트랙 추가 | `console/shared.js` 의 `TRACKS` |
| 사전진단 문항 조정 | `course-config.js` 의 `precheck` + `precheck-hub.js` 의 `PICK` |
| 완전히 새로운 형태 | 기존 셸을 재사용할지부터 결정 — 재사용 안 하면 최상위에 새 폴더 |

> **새 형태의 콘텐츠를 만들 때**: `modules/`(4단계 학습형)와 `console/`(게임형 스테이지) 중
> 어느 셸도 맞지 않으면 억지로 끼워넣지 말고 새 폴더로 시작하되, `shared/access.js` 와
> `stages/core/` 의 세션·저장소는 재사용하는 편이 낫다.

---

## 9. 알려진 제약

- 카메라는 **localhost 또는 HTTPS** 에서만 켜진다
- CDN 의존 — 모델 총 ~45MB를 매번 받는다 (로컬 호스팅 전환 검토 대상, `models/movenet/` 만 로컬)
- 관리자 비밀번호가 **클라이언트에 평문**으로 있다 (`stages/admin/admin.js`) — 서버 전환 시 반드시 해소
- 학생 본인 식별이 **이름 문자열** 기반 → 동명이인 충돌 가능
