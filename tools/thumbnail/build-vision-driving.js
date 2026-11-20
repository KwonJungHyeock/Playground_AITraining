/* AI 영상처리 주행 썸네일 조립
   트랙 배경(생성) + 제품컷(따낸 차) + 인식 궤적 + 공통 오버레이 규격.
   좌표는 전부 500x500 기준. */
const fs = require('fs');
const { chromium } = require('playwright');

const b64 = f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64');
const font = f => 'data:font/woff2;base64,' + fs.readFileSync(f).toString('base64');

// 차 배치 — 트랙 선 위에 올린다
const CAR = { left: 95, top: 118, w: 210 };
// 차 앞쪽(좌하단)으로 이어지는 선을 따라가는 인식 궤적
const PATH_FRONT = 'M 2,382 C 44,368 92,344 140,306';
const PATH_BACK = 'M 298,200 C 348,180 398,150 458,120';

const CFG = {
  eyebrow: { amber: 'VISION AI', rest: ' · 영상처리 주행' },
  title: ['카메라로 길을 읽는', 'AI 자율주행'],
  callouts: [
    { n: '1', text: '카메라가 길을 봐요', px: 252, py: 116, tx: 146, ty: 230 },
    { n: '2', text: '선을 따라 달려요', px: 20, py: 284, tx: 118, ty: 318 },
  ],
};

const html = `<style>
@font-face{font-family:P;src:url(${font('fonts/ExtraBold.woff2')})format('woff2');font-weight:800}
@font-face{font-family:P;src:url(${font('fonts/Bold.woff2')})format('woff2');font-weight:700}
html,body{margin:0;padding:0;overflow:hidden}
.t{position:relative;width:500px;height:500px;overflow:hidden;font-family:P,sans-serif;
   -webkit-font-smoothing:antialiased;background:#fff}
.bg{position:absolute;inset:0;width:500px;height:500px;display:block}
.car{position:absolute;left:${CAR.left}px;top:${CAR.top}px;width:${CAR.w}px;display:block}
/* 따낼 때 같이 사라진 접지 그림자를 다시 깐다 */
.sh{position:absolute;left:118px;top:270px;width:184px;height:50px;border-radius:50%;
    background:radial-gradient(50% 50%,rgba(40,30,20,.62),rgba(40,30,20,0) 70%);filter:blur(6px)}

.tint{position:absolute;inset:0;background:#0f142c;opacity:.24}
.vig{position:absolute;inset:0;
  background:radial-gradient(118% 92% at 50% 34%,rgba(15,20,44,0) 30%,rgba(15,20,44,.62) 72%,rgba(10,15,38,.92) 100%)}
.foot{position:absolute;inset:auto 0 0 0;height:270px;
  background:linear-gradient(180deg,rgba(10,15,38,0) 0%,rgba(10,15,38,.74) 44%,rgba(10,15,38,.96) 72%,#0a0f26 100%)}

.pill{position:absolute;display:inline-flex;align-items:center;gap:7px;height:30px;padding:0 12px 0 7px;
  border-radius:9px;background:rgba(6,10,26,.9);border:1px solid rgba(255,255,255,.18);
  box-shadow:0 6px 18px rgba(0,0,0,.45);white-space:nowrap}
.pill i{width:17px;height:17px;border-radius:50%;background:#ff9a3f;color:#231200;
  font-size:11px;font-weight:800;font-style:normal;display:grid;place-items:center;line-height:1}
.pill span{color:#fff;font-size:12.5px;font-weight:700;letter-spacing:-.01em}
.dot{position:absolute;width:9px;height:9px;border-radius:50%;background:#ffb168;
  box-shadow:0 0 0 5px rgba(255,154,63,.26),0 0 16px 5px rgba(255,154,63,.5)}
svg.lay{position:absolute;inset:0;width:500px;height:500px;pointer-events:none}

.copy{position:absolute;left:30px;bottom:30px;right:30px}
.eyebrow{font-size:13px;font-weight:800;letter-spacing:.14em;margin-bottom:11px;color:rgba(255,255,255,.62)}
.eyebrow b{color:#ff9a3f;font-weight:800}
.title{color:#fff;font-size:38px;font-weight:800;line-height:1.2;letter-spacing:-.035em;
  text-shadow:0 2px 18px rgba(0,0,0,.5)}
</style>
<div class="t">
  <img class="bg" src="${b64('figma/track.png')}">

  <!-- 인식한 주행 궤적 — 차 앞쪽 선 위에 얹는다 -->
  <svg class="lay">
    ${[PATH_FRONT, PATH_BACK].map(d => `
    <path d="${d}" fill="none" stroke="#ff8a3d" stroke-width="20" stroke-linecap="round" opacity=".38"/>
    <path d="${d}" fill="none" stroke="#ff9a3f" stroke-width="5" stroke-linecap="round"
          stroke-dasharray="16 13" opacity=".95"/>`).join('')}
  </svg>

  <div class="sh"></div>
  <img class="car" src="${b64('car_cut.png')}">

  <div class="tint"></div><div class="vig"></div><div class="foot"></div>

  <svg class="lay">
    ${CFG.callouts.map(o => `<path d="M${o.px + 16},${o.py + 30} L${o.tx},${o.ty}" stroke="#ffb168"
      stroke-width="2" stroke-dasharray="3 5" stroke-linecap="round" fill="none" opacity=".92"/>`).join('')}
  </svg>
  ${CFG.callouts.map(o => `<div class="pill" style="left:${o.px}px;top:${o.py}px"><i>${o.n}</i><span>${o.text}</span></div>
    <div class="dot" style="left:${o.tx - 4.5}px;top:${o.ty - 4.5}px"></div>`).join('')}

  <div class="copy">
    <div class="eyebrow"><b>${CFG.eyebrow.amber}</b>${CFG.eyebrow.rest}</div>
    <div class="title">${CFG.title.join('<br>')}</div>
  </div>
</div>`;

(async () => {
  const br = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const [s, suf] of [[1, ''], [2, '@2x']]) {
    const p = await br.newPage({ viewport: { width: 500, height: 500 }, deviceScaleFactor: s });
    await p.setContent(html);
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(700);
    await p.screenshot({ path: `car${suf}.png` });
    await p.close();
  }
  await br.close();
  console.log('car.png / car@2x.png');
})();
