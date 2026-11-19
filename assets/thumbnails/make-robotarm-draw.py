#!/usr/bin/env python3
"""피지컬 AI 학습 콘텐츠 제품 썸네일 — 500x500, 글자 없음.
   장면: 로봇 팔이 커팅 매트 위에 원을 그린다 (AI가 손을 갖는 순간)."""
import math

W = H = 500
out = []
a = out.append

def lerp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)

def unit(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    d = math.hypot(dx, dy)
    return dx / d, dy / d

# ── 매트 네 꼭짓점 (좌 → 상 → 우 → 하) ──
M1, M2, M3, M4 = (236, 356), (386, 288), (484, 388), (334, 456)
MAT = (M1, M2, M3, M4)
matpts = ' '.join(f'{x},{y}' for x, y in MAT)

# ── 그려지는 원 + 펜 접점 ──
CX, CY, CR, CSQ, CROT = 366, 352, 46, 0.46, -24
_r = math.radians(CROT)
_ly = CR * CSQ
PEN_X = CX + (-_ly * math.sin(_r))
PEN_Y = CY + (_ly * math.cos(_r))

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

a('''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0.4" y2="1">
  <stop offset="0" stop-color="#f4f7fb"/><stop offset="1" stop-color="#e1e7f0"/>
</linearGradient>
<linearGradient id="desk" x1="0" y1="0" x2="0.3" y2="1">
  <stop offset="0" stop-color="#ddb28c"/><stop offset="1" stop-color="#c08f66"/>
</linearGradient>
<linearGradient id="tube" x1="0" y1="0" x2="0.25" y2="1">
  <stop offset="0" stop-color="#ffffff"/><stop offset="0.5" stop-color="#eef2f7"/>
  <stop offset="1" stop-color="#c4ccd6"/>
</linearGradient>
<linearGradient id="dark" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#171a1f"/><stop offset="0.4" stop-color="#33373f"/>
  <stop offset="1" stop-color="#14161a"/>
</linearGradient>
<linearGradient id="plate" x1="0" y1="0" x2="0.6" y2="1">
  <stop offset="0" stop-color="#f1f4f8"/><stop offset="1" stop-color="#c8d0d9"/>
</linearGradient>
<linearGradient id="mat" x1="0.1" y1="0" x2="0.6" y2="1">
  <stop offset="0" stop-color="#318a64"/><stop offset="1" stop-color="#1f6546"/>
</linearGradient>
<linearGradient id="pen" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#5fa3ef"/><stop offset="0.45" stop-color="#2f7fe0"/>
  <stop offset="1" stop-color="#1b5cad"/>
</linearGradient>
<radialGradient id="shadow" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#2a1d12" stop-opacity="0.32"/>
  <stop offset="1" stop-color="#2a1d12" stop-opacity="0"/>
</radialGradient>
<clipPath id="matclip"><polygon points="PTS"/></clipPath>
</defs>'''.replace('PTS', matpts))

# ── 배경 + 책상 ──
a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
a('<polygon points="0,236 500,120 500,500 0,500" fill="url(#desk)"/>')
a('<polygon points="0,236 500,120 500,129 0,245" fill="#b1815c" opacity="0.45"/>')

# ── 매트 ──
a('<ellipse cx="358" cy="400" rx="140" ry="60" fill="url(#shadow)"/>')
a(f'<polygon points="{matpts}" fill="url(#mat)"/>')
a('<g clip-path="url(#matclip)" stroke="#63ad8b" stroke-width="1" opacity="0.5">')
for i in range(1, 8):
    t = i / 8
    for p, q in ((lerp(M1, M2, t), lerp(M4, M3, t)), (lerp(M1, M4, t), lerp(M2, M3, t))):
        a(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}"/>')
a('</g>')
a(f'<polygon points="{matpts}" fill="none" stroke="#174d36" stroke-width="2.5"/>')

# ── 그려진 파란 원 ──
a(f'<g transform="translate({CX} {CY}) rotate({CROT}) scale(1 {CSQ})">')
a(f'<circle r="{CR}" fill="none" stroke="#1b5cad" stroke-width="13" opacity="0.35"/>')
a(f'<circle r="{CR}" fill="none" stroke="#2f7fe0" stroke-width="11"/>')
a('</g>')

# ── 베이스 받침판 ──
a('<polygon points="36,340 194,276 284,322 126,388" fill="url(#plate)"/>')
a('<polygon points="36,340 126,388 126,396 36,348" fill="#a6afba"/>')
a('<polygon points="126,388 284,322 284,330 126,396" fill="#b7bfc9"/>')
a('<ellipse cx="162" cy="320" rx="54" ry="20" fill="#1f1a15" opacity="0.16"/>')

# ── 컨트롤러 박스 ──
a('<polygon points="46,272 86,256 114,270 74,287" fill="#3f444d"/>')
a('<polygon points="46,272 74,287 74,320 46,305" fill="#191c21"/>')
a('<polygon points="74,287 114,270 114,303 74,320" fill="#2a2e35"/>')
a('<polygon points="82,296 94,291 94,310 82,315" fill="#464c56"/>')
a('<polygon points="99,289 105,286 105,305 99,308" fill="#464c56"/>')

# ── 로봇 팔 관절 ──
A = (158, 252)   # 어깨 (베이스 상단)
B = (116, 170)   # 상완 꺾임
C = (248,  98)   # 상단 팔꿈치
D = (338, 166)   # 우측 꺾임
E = (376, 238)   # 손목
LINKS = [(A, B, 44), (B, C, 40), (C, D, 36), (D, E, 32)]

def link(p, q, w):
    a(f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="#9aa3ae"'
      f' stroke-width="{w + 3}" stroke-linecap="round" opacity="0.4"/>')
    a(f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" stroke="url(#tube)"'
      f' stroke-width="{w}" stroke-linecap="round"/>')

def band(p, q, dist, w):
    """관절 옆 어두운 분절 띠 — 흰 튜브가 이어 붙은 느낌을 만든다."""
    ux, uy = unit(p, q)
    x1, y1 = p[0] + ux * dist, p[1] + uy * dist
    x2, y2 = p[0] + ux * (dist + 7), p[1] + uy * (dist + 7)
    a(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"'
      f' stroke="#2b2f36" stroke-width="{w + 1}" stroke-linecap="butt"/>')

for p, q, w in LINKS:
    link(p, q, w)

# 관절마다 양쪽 링크에 띠 + 흰 너클
for (p, q, w), (p2, q2, w2) in zip(LINKS, LINKS[1:]):
    band(q, p, 17, w)        # 들어오는 링크 쪽
    band(p2, q2, 17, w2)     # 나가는 링크 쪽
for pt, w in ((B, 44), (C, 40), (D, 36)):
    a(f'<circle cx="{pt[0]}" cy="{pt[1]}" r="{w / 2 + 1}" fill="url(#tube)"/>')
    a(f'<circle cx="{pt[0]}" cy="{pt[1]}" r="{w / 2 + 1}" fill="none" stroke="#b9c1cb" stroke-width="1"/>')

# ── 베이스 (검은 원통) ──
a('<path d="M112,260 L112,312 A48,22 0 0 0 208,312 L208,260 Z" fill="url(#dark)"/>')
a('<ellipse cx="160" cy="260" rx="48" ry="22" fill="#434852"/>')
a('<ellipse cx="160" cy="259" rx="39" ry="17" fill="#383d46"/>')
a('<path d="M124,252 A48,22 0 0 1 196,252" fill="none" stroke="#5c636e" stroke-width="2" opacity="0.7"/>')
a('<path d="M112,296 A48,22 0 0 0 208,296" fill="none" stroke="#0e1013" stroke-width="2" opacity="0.5"/>')

# ── 손목 블록 + 펜 ──
a(f'<path d="M354,234 L398,234 L398,294 A22,10 0 0 1 354,294 Z" fill="url(#dark)"/>')
a('<ellipse cx="376" cy="234" rx="22" ry="10" fill="#4a505a"/>')
a('<rect x="360" y="246" width="32" height="6" rx="3" fill="#565d68"/>')
a('<rect x="360" y="258" width="32" height="6" rx="3" fill="#3d434c"/>')

PT_TOP = 290
a(f'<rect x="{PEN_X - 6.5:.1f}" y="{PT_TOP}" width="13" height="{PEN_Y - 9 - PT_TOP:.1f}" rx="6" fill="url(#pen)"/>')
a(f'<polygon points="{PEN_X - 6.5:.1f},{PEN_Y - 12:.1f} {PEN_X + 6.5:.1f},{PEN_Y - 12:.1f}'
  f' {PEN_X + 2:.1f},{PEN_Y:.1f} {PEN_X - 2:.1f},{PEN_Y:.1f}" fill="#174f96"/>')
a(f'<ellipse cx="{PEN_X:.1f}" cy="{PEN_Y + 1:.1f}" rx="13" ry="5.5" fill="#0f3f22" opacity="0.4"/>')
a(f'<ellipse cx="{PEN_X:.1f}" cy="{PEN_Y:.1f}" rx="7" ry="3" fill="#aed3f8" opacity="0.75"/>')

a('</svg>')

base = __import__('os').path.dirname(__file__) or '.'
open(f'{base}/robotarm-draw.svg', 'w').write('\n'.join(out))
print(f'svg written · pen tip = ({PEN_X:.1f}, {PEN_Y:.1f})')
