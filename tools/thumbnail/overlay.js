/* 코스 썸네일 텍스트 오버레이 — 레퍼런스(로봇 캘리그래피) 규칙을 그대로 따른다.
     · 네이비 비네트 + 하단 그라데이션으로 글자 자리를 만든다
     · 앰버 점선 콜아웃 ①② 로 장면의 두 지점을 짚는다
     · 왼쪽 아래: 앰버 카테고리 한 줄 + 흰 큰 제목 두 줄
   좌표는 전부 500x500 기준. */
const CONFIG = {
  A: {
    img: 'figma/A.png',
    eyebrow: { amber: 'VISION AI', rest: ' · 이미지 분류' },
    title: ['내 사진으로 배우는', 'AI 분류기'],
    callouts: [
      { n: '1', text: '내가 모은 사진', px: 20, py: 36, tx: 196, ty: 116 },
      { n: '2', text: 'AI가 알아봐요', px: 262, py: 176, tx: 243, ty: 246 },
    ],
  },
  B: {
    img: 'figma/B.png',
    eyebrow: { amber: 'VISION AI', rest: ' · 이미지 분류' },
    title: ['AI가 스스로', '나누는 법 배우기'],
    callouts: [
      { n: '1', text: '내가 정한 기준', px: 16, py: 38, tx: 66, ty: 238 },
      { n: '2', text: 'AI가 나눠요', px: 302, py: 64, tx: 436, ty: 246 },
    ],
  },
};

const CSS = `
@font-face{font-family:P;src:url(fonts/ExtraBold.woff2)format('woff2');font-weight:800}
@font-face{font-family:P;src:url(fonts/Bold.woff2)format('woff2');font-weight:700}
@font-face{font-family:P;src:url(fonts/SemiBold.woff2)format('woff2');font-weight:600}
html,body{margin:0;padding:0;overflow:hidden}
.t{position:relative;width:500px;height:500px;overflow:hidden;font-family:P,sans-serif;
   -webkit-font-smoothing:antialiased}
.t>img{position:absolute;inset:0;width:500px;height:500px;object-fit:cover;display:block}

/* 네이비 틴트 + 비네트 — 레퍼런스에서 뽑은 값 (모서리 #0f142c, 중앙은 절반만 어둡게) */
.tint{position:absolute;inset:0;background:#0f142c;opacity:.24}
.vig{position:absolute;inset:0;
  background:radial-gradient(118% 92% at 50% 34%,rgba(15,20,44,0) 30%,rgba(15,20,44,.62) 72%,rgba(10,15,38,.92) 100%)}
/* 글자 자리 */
.foot{position:absolute;inset:auto 0 0 0;height:270px;
  background:linear-gradient(180deg,rgba(10,15,38,0) 0%,rgba(10,15,38,.74) 44%,rgba(10,15,38,.96) 72%,#0a0f26 100%)}

/* 콜아웃 */
.pill{position:absolute;display:inline-flex;align-items:center;gap:7px;height:30px;padding:0 12px 0 7px;
  border-radius:9px;background:rgba(6,10,26,.9);border:1px solid rgba(255,255,255,.18);
  box-shadow:0 6px 18px rgba(0,0,0,.45);white-space:nowrap}
.pill i{width:17px;height:17px;border-radius:50%;background:#ff9a3f;color:#231200;
  font-size:11px;font-weight:800;font-style:normal;display:grid;place-items:center;line-height:1}
.pill span{color:#fff;font-size:12.5px;font-weight:700;letter-spacing:-.01em}
.dot{position:absolute;width:9px;height:9px;border-radius:50%;background:#ffb168;
  box-shadow:0 0 0 5px rgba(255,154,63,.26),0 0 16px 5px rgba(255,154,63,.5)}
svg.lines{position:absolute;inset:0;width:500px;height:500px;pointer-events:none}

/* 텍스트 블록 */
.copy{position:absolute;left:30px;bottom:30px;right:30px}
.eyebrow{font-size:13px;font-weight:800;letter-spacing:.14em;margin-bottom:11px;color:rgba(255,255,255,.62)}
.eyebrow b{color:#ff9a3f;font-weight:800}
.title{color:#fff;font-size:38px;font-weight:800;line-height:1.2;letter-spacing:-.035em;
  text-shadow:0 2px 18px rgba(0,0,0,.5)}
`;

function card(c) {
  const lines = c.callouts.map(o => {
    // 말풍선 아래 모서리에서 대상까지 점선
    const sx = o.px + 16, sy = o.py + 30;
    return `<path d="M${sx},${sy} L${o.tx},${o.ty}" stroke="#ffb168" stroke-width="2"
             stroke-dasharray="3 5" stroke-linecap="round" fill="none" opacity=".92"/>`;
  }).join('');
  const pills = c.callouts.map(o =>
    `<div class="pill" style="left:${o.px}px;top:${o.py}px"><i>${o.n}</i><span>${o.text}</span></div>
     <div class="dot" style="left:${o.tx - 4.5}px;top:${o.ty - 4.5}px"></div>`).join('');
  return `<div class="t">
    <img src="${c.img}">
    <div class="tint"></div><div class="vig"></div><div class="foot"></div>
    <svg class="lines">${lines}</svg>
    ${pills}
    <div class="copy">
      <div class="eyebrow"><b>${c.eyebrow.amber}</b>${c.eyebrow.rest}</div>
      <div class="title">${c.title.join('<br>')}</div>
    </div>
  </div>`;
}

const which = process.argv[2];
require('fs').writeFileSync(`_card_${which}.html`,
  `<style>${CSS}</style>${card(CONFIG[which])}`);
console.log('wrote _card_' + which + '.html');
