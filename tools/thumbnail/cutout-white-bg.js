/* 흰 배경 제품컷에서 차를 따낸다. 순백(#ffffff)이라 휘도 임계로 충분하고,
   경계는 임계 구간을 두어 부드럽게 깎는다(계단현상 방지).
   file:// 캔버스 오염을 피하려고 이미지는 data URI 로 넣는다. */
const fs = require('fs');
const { chromium } = require('playwright');
(async () => {
  const src = 'data:image/png;base64,' + fs.readFileSync('car_src.png').toString('base64');
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage();
  await p.setContent('<body style="margin:0"></body>');
  const out = await p.evaluate(async (src) => {
    const im = new Image(); im.src = src; await im.decode();
    const c = document.createElement('canvas');
    c.width = im.naturalWidth; c.height = im.naturalHeight;
    const x = c.getContext('2d'); x.drawImage(im, 0, 0);
    const d = x.getImageData(0, 0, c.width, c.height), a = d.data;
    const HI = 250, LO = 216;          // HI 이상 완전투명, LO 이하 완전불투명
    for (let i = 0; i < a.length; i += 4) {
      const lum = Math.min(a[i], a[i + 1], a[i + 2]);   // 가장 어두운 채널 기준
      if (lum >= HI) a[i + 3] = 0;
      else if (lum > LO) a[i + 3] = Math.round(255 * (HI - lum) / (HI - LO));
    }
    x.putImageData(d, 0, 0);
    return c.toDataURL('image/png');
  }, src);
  fs.writeFileSync('car_cut.png', Buffer.from(out.split(',')[1], 'base64'));
  await b.close();
  console.log('car_cut.png written');
})();
