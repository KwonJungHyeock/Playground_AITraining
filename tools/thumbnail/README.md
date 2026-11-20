# 썸네일 텍스트 오버레이

3D 렌더 위에 카테고리 · 제목 · 콜아웃을 얹어 500×500 카드 썸네일을 만든다.
레퍼런스는 운영 중인 `로봇 캘리그래피` 카드 — 그 규칙을 그대로 따른다.

| 규칙 | 값 |
| --- | --- |
| 캔버스 | 500×500 (2x 함께 출력) |
| 틴트 | `#0f142c` 24% + 중앙에서 모서리로 가는 비네트 |
| 하단 | 아래 270px 를 `#0a0f26` 로 떨구는 그라데이션 — 글자 자리 |
| 카테고리 | 앰버 `#ff9a3f` 대문자 + 회색 부제, 자간 `.14em` |
| 제목 | 흰색 800, 38px, 두 줄, 행간 1.2 |
| 콜아웃 | 번호 ①② 앰버 원 + 검정 말풍선, 앰버 점선, 대상에 발광 점 |

## 쓰는 법

```bash
# 1) Pretendard 받기 (리포지토리에 넣지 않는다 — 2.4MB)
BASE=https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/packages/pretendard/dist/web/static/woff2
mkdir -p fonts && for n in ExtraBold Bold SemiBold; do
  curl -fL -o "fonts/$n.woff2" "$BASE/Pretendard-$n.woff2"; done

# 2) 렌더 이미지를 figma/ 에 두고 overlay.js 의 CONFIG 를 채운 뒤
node overlay.js A          # _card_A.html 생성 → 브라우저로 500×500 스크린샷
```

`CONFIG` 의 좌표는 전부 500×500 기준이다. `callouts[].tx/ty` 는 **반드시 장면 속 실제
대상 위**에 찍을 것 — 허공을 가리키면 지시선이 아무 의미가 없다.

## 밑그림(3D 렌더) 만들기

Figma AI 이미지 생성(`gpt-image-2.5-flare`), 파일 `Eduino AI — 콘텐츠 썸네일`.
프롬프트 고정 요소: 밝은 나무 책상 · 약간 위에서 본 3/4 각도 · 무광 3D ·
코랄(#F0473A→#FF8A3D) 포인트 · **글자/숫자/로고 일체 금지**(글자는 이 스크립트가 얹는다).
원본 1024 는 `*-source-1024.png` 로 남긴다.
