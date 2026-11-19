#!/usr/bin/env python3
"""AI 학습·추론 모델 콘텐츠 제품 썸네일 — 500x500, 글자 없음.

   읽히는 순서를 셋으로만 줄인다.
     ① 뒤에 겹쳐진 사진 더미  → 모아 둔 학습 데이터
     ② 앞 사진의 코랄 인식 괄호 → 지금 추론 중인 대상
     ③ 오른쪽 아래 큰 게이지   → 확신도
   기기(노트북·책상)는 뺀다. 작은 크기에서 주제를 가리기만 한다.
"""
import os

W = H = 500
out = []
a = out.append

CX, CY = 236, 227                      # 앞 카드 중심
CW, CH = 248, 262                      # 앞 카드 크기
GX, GY, GR = 374, 353, 56              # 게이지 디스크

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

a('''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0.45" y2="1">
  <stop offset="0" stop-color="#fbfcfe"/><stop offset="1" stop-color="#e6ebf3"/>
</linearGradient>
<linearGradient id="photo" x1="0" y1="0" x2="0.4" y2="1">
  <stop offset="0" stop-color="#3d4659"/><stop offset="1" stop-color="#232a38"/>
</linearGradient>
<linearGradient id="subject" x1="0" y1="0" x2="0.3" y2="1">
  <stop offset="0" stop-color="#b9c8dc"/><stop offset="1" stop-color="#8296b2"/>
</linearGradient>
<linearGradient id="coral" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#ff8a3d"/><stop offset="1" stop-color="#f0473a"/>
</linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#ff7a52" stop-opacity="0.16"/>
  <stop offset="1" stop-color="#ff7a52" stop-opacity="0"/>
</radialGradient>
<filter id="drop" x="-30%" y="-30%" width="160%" height="160%">
  <feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#1b2433" flood-opacity="0.22"/>
</filter>
<filter id="dropS" x="-40%" y="-40%" width="180%" height="180%">
  <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#1b2433" flood-opacity="0.26"/>
</filter>
<clipPath id="front">
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22"/>
</clipPath>
</defs>'''.replace('{x}', str(CX - CW // 2)).replace('{y}', str(CY - CH // 2))
       .replace('{w}', str(CW)).replace('{h}', str(CH)))

a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
a('<ellipse cx="250" cy="250" rx="240" ry="230" fill="url(#glow)"/>')

# ── ① 뒤에 겹친 사진 더미 (학습 데이터) ──
for ang, dx, dy, fill in ((-11, -16, -10, '#ced7e3'), (-5.5, -8, -5, '#e3e9f1')):
    a(f'<g transform="rotate({ang} {CX} {CY}) translate({dx} {dy})" filter="url(#drop)">')
    a(f'<rect x="{CX - CW//2}" y="{CY - CH//2}" width="{CW}" height="{CH}" rx="22"'
      f' fill="#ffffff" stroke="#d3dae4" stroke-width="1"/>')
    a(f'<rect x="{CX - CW//2 + 10}" y="{CY - CH//2 + 10}" width="{CW - 20}" height="{CH - 20}"'
      f' rx="14" fill="{fill}"/>')
    a('</g>')

# ── ② 앞 사진 — 지금 추론 중인 대상 ──
a(f'<g transform="rotate(3 {CX} {CY})">')
a(f'<rect x="{CX - CW//2}" y="{CY - CH//2}" width="{CW}" height="{CH}" rx="22"'
  f' fill="url(#photo)" filter="url(#drop)"/>')
a('<g clip-path="url(#front)">')
# 대상: 머리 + 어깨 실루엣
a(f'<ellipse cx="{CX}" cy="{CY + 104}" rx="96" ry="80" fill="url(#subject)"/>')
a(f'<circle cx="{CX}" cy="{CY - 20}" r="53" fill="url(#subject)"/>')
a('</g>')

# 인식 괄호 — 네 모서리 L 자
BX, BY, BW, BH = CX - 86, CY - 92, 172, 196
L, SW = 40, 9
for (px, py, sx, sy) in ((BX, BY, 1, 1), (BX + BW, BY, -1, 1),
                         (BX, BY + BH, 1, -1), (BX + BW, BY + BH, -1, -1)):
    a(f'<path d="M{px},{py + sy * L} L{px},{py} L{px + sx * L},{py}" fill="none"'
      f' stroke="url(#coral)" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"/>')
a('</g>')

# ── ③ 확신도 게이지 ──
a(f'<circle cx="{GX}" cy="{GY}" r="{GR}" fill="#ffffff" filter="url(#dropS)"/>')
a(f'<circle cx="{GX}" cy="{GY}" r="{GR - 15}" fill="none" stroke="#e4e9f1" stroke-width="12"/>')
a(f'<circle cx="{GX}" cy="{GY}" r="{GR - 15}" fill="none" stroke="url(#coral)" stroke-width="12"'
  f' stroke-linecap="round" stroke-dasharray="214 43" transform="rotate(-90 {GX} {GY})"/>')
# 가운데 체크 — 판정이 끝났다는 신호
a(f'<path d="M{GX - 15},{GY + 1} L{GX - 4},{GY + 12} L{GX + 16},{GY - 12}" fill="none"'
  f' stroke="#f0473a" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')

a('</svg>')

base = os.path.dirname(__file__) or '.'
open(f'{base}/ai-train-infer.svg', 'w').write('\n'.join(out))
print('svg written')
