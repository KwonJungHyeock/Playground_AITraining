#!/usr/bin/env python3
"""AI 영상처리 · 학습·추론 콘텐츠 제품 썸네일 — 500x500, 글자 없음.

   "사람 얼굴 하나에 박스 하나" 로 좁게 읽히지 않게, 영상이 **처리되는 것** 자체를 보여 준다.
     ① 본 화면 = 처리 결과 — 픽셀 격자 위에 윤곽선과 특징점
     ② 왼쪽 위 인셋 = 원본 영상 — 처리 전/후가 한 장에 같이 있다
     ③ 대상 셋 + 인식 박스·라벨 → 한 장면에서 여러 대상을 동시에 분석
   비교 슬라이더로 가르면 걸친 대상이 반쪽으로 잘려 인셋 방식으로 간다.
"""
import os

W = H = 500
out = []
a = out.append

FX, FY, FW, FH, FR = 36, 96, 428, 308, 22        # 본 영상 프레임
GND = 356                                         # 바닥선
IX, IY, IW, IH = 58, 118, 132, 96                 # 원본 인셋

# 대상 셋 — 박스가 겹치지 않도록 가로로 벌린다
CUP = dict(x=112, y=262, w=70, h=GND - 262)
BALL = dict(cx=258, cy=312, r=40)
BOOK = dict(x=342, y=254, w=78, h=GND - 254)
BOXES = [(CUP['x'] - 11, CUP['y'] - 11, CUP['w'] + 22, CUP['h'] + 22),
         (BALL['cx'] - BALL['r'] - 11, BALL['cy'] - BALL['r'] - 11, BALL['r'] * 2 + 22, BALL['r'] * 2 + 22),
         (BOOK['x'] - 11, BOOK['y'] - 11, BOOK['w'] + 22, BOOK['h'] + 22)]

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

a(f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0.45" y2="1">
  <stop offset="0" stop-color="#fbfcfe"/><stop offset="1" stop-color="#e5eaf2"/>
</linearGradient>
<linearGradient id="proc" x1="0" y1="0" x2="0.4" y2="1">
  <stop offset="0" stop-color="#1a2440"/><stop offset="1" stop-color="#0a0e1b"/>
</linearGradient>
<linearGradient id="raw" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#f4e7d7"/><stop offset="1" stop-color="#e8d5be"/>
</linearGradient>
<linearGradient id="coral" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#ff8a3d"/><stop offset="1" stop-color="#f0473a"/>
</linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#ff7a52" stop-opacity="0.13"/>
  <stop offset="1" stop-color="#ff7a52" stop-opacity="0"/>
</radialGradient>
<filter id="drop" x="-25%" y="-25%" width="150%" height="150%">
  <feDropShadow dx="0" dy="16" stdDeviation="17" flood-color="#17202e" flood-opacity="0.24"/>
</filter>
<filter id="dropS" x="-40%" y="-40%" width="180%" height="180%">
  <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#060a14" flood-opacity="0.55"/>
</filter>
<clipPath id="frame"><rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="{FR}"/></clipPath>
<clipPath id="inset"><rect x="{IX}" y="{IY}" width="{IW}" height="{IH}" rx="9"/></clipPath>
</defs>''')

a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
a('<ellipse cx="250" cy="250" rx="248" ry="238" fill="url(#glow)"/>')
a(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="{FR}" fill="#0a0e1b" filter="url(#drop)"/>')

def cup_path(w=3, color='#7fd4ff'):
    c = CUP
    a(f'<path d="M{c["x"]},{c["y"]} L{c["x"] + 6},{c["y"] + c["h"]} L{c["x"] + c["w"] - 6},{c["y"] + c["h"]}'
      f' L{c["x"] + c["w"]},{c["y"]} Z" fill="none" stroke="{color}" stroke-width="{w}"/>')
    a(f'<ellipse cx="{c["x"] + c["w"] / 2}" cy="{c["y"]}" rx="{c["w"] / 2}" ry="10"'
      f' fill="none" stroke="{color}" stroke-width="{w}"/>')
    a(f'<path d="M{c["x"] + c["w"]},{c["y"] + 20} q 24,10 0,36" fill="none"'
      f' stroke="{color}" stroke-width="{w}"/>')

# ── ① 본 화면 = 처리 결과 ──
a('<g clip-path="url(#frame)">')
a(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" fill="url(#proc)"/>')
# 픽셀 격자 — 영상이 숫자 격자로 바뀐다
a('<g stroke="#31406b" stroke-width="1">')
for gx in range(FX, FX + FW, 20):
    a(f'<line x1="{gx}" y1="{FY}" x2="{gx}" y2="{FY + FH}"/>')
for gy in range(FY, FY + FH, 20):
    a(f'<line x1="{FX}" y1="{gy}" x2="{FX + FW}" y2="{gy}"/>')
a('</g>')
a(f'<line x1="{FX}" y1="{GND}" x2="{FX + FW}" y2="{GND}" stroke="#5b74a8" stroke-width="2"/>')

# 윤곽선 — 추출된 형태
cup_path()
a(f'<circle cx="{BALL["cx"]}" cy="{BALL["cy"]}" r="{BALL["r"]}" fill="none" stroke="#7fd4ff" stroke-width="3"/>')
a(f'<rect x="{BOOK["x"]}" y="{BOOK["y"]}" width="{BOOK["w"]}" height="{BOOK["h"]}" rx="3"'
  ' fill="none" stroke="#7fd4ff" stroke-width="3"/>')

# 특징점 — 윤곽 위에 찍히는 점
for px, py in ((CUP['x'], CUP['y']), (CUP['x'] + CUP['w'], CUP['y']),
               (CUP['x'] + 6, GND), (CUP['x'] + CUP['w'] - 6, GND),
               (BALL['cx'], BALL['cy'] - BALL['r']), (BALL['cx'] - BALL['r'], BALL['cy']),
               (BALL['cx'] + BALL['r'], BALL['cy']), (BALL['cx'], BALL['cy'] + BALL['r']),
               (BOOK['x'], BOOK['y']), (BOOK['x'] + BOOK['w'], BOOK['y']),
               (BOOK['x'], GND), (BOOK['x'] + BOOK['w'], GND)):
    a(f'<circle cx="{px}" cy="{py}" r="3.4" fill="#aee6ff"/>')

# ③ 인식 박스 + 라벨 태그
for bx, by, bw, bh in BOXES:
    a(f'<rect x="{bx}" y="{by - 19}" width="44" height="15" rx="4" fill="url(#coral)"/>')
    a(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="4" fill="none"'
      ' stroke="url(#coral)" stroke-width="4"/>')
    for px, py in ((bx, by), (bx + bw, by), (bx, by + bh), (bx + bw, by + bh)):
        a(f'<circle cx="{px}" cy="{py}" r="4.5" fill="#ff6a52"/>')
a('</g>')

# ── ② 원본 인셋 — 처리 전 영상 ──
a(f'<g filter="url(#dropS)">')
a(f'<rect x="{IX - 4}" y="{IY - 4}" width="{IW + 8}" height="{IH + 8}" rx="12" fill="#ffffff"/>')
a('</g>')
a('<g clip-path="url(#inset)">')
a(f'<rect x="{IX}" y="{IY}" width="{IW}" height="{IH}" fill="url(#raw)"/>')
a(f'<rect x="{IX}" y="{IY + 64}" width="{IW}" height="{IH - 64}" fill="#c7a582"/>')
a(f'<path d="M{IX + 22},{IY + 34} L{IX + 25},{IY + 64} L{IX + 45},{IY + 64} L{IX + 48},{IY + 34} Z"'
  ' fill="#eef3f8"/>')
a(f'<ellipse cx="{IX + 35}" cy="{IY + 34}" rx="13" ry="4.5" fill="#6b4a33"/>')
a(f'<circle cx="{IX + 72}" cy="{IY + 52}" r="13" fill="#5a9ae8"/>')
a(f'<rect x="{IX + 94}" y="{IY + 32}" width="22" height="32" rx="2" fill="#3fa06f"/>')
a('</g>')

a('</svg>')

base = os.path.dirname(__file__) or '.'
open(f'{base}/ai-train-infer.svg', 'w').write('\n'.join(out))
print('svg written')
