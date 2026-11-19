#!/usr/bin/env python3
"""AI 학습·추론 모델 콘텐츠 제품 썸네일 — 500x500, 글자 없음.
   장면: 카메라로 본 대상을 모델이 인식하고, 수집한 샘플과 확신도 게이지를 함께 보여 준다.

   화면 내용은 로컬 0..100 좌표계에 그린 뒤 matrix() 로 화면 평면에 얹는다.
   (y 는 위로 증가 — 화면 평면의 '위' 방향 벡터 V 를 그대로 쓴다)
"""
import os

W = H = 500
out = []
a = out.append

# ── 노트북 기하 ──
P1 = (96, 310)           # 화면 좌하(힌지 왼쪽 끝)
U = (222, -39)           # 화면 가로 방향
V = (30, -171)           # 화면 세로(위) 방향
FWD = (86, 63)           # 힌지 → 앞 (키보드 데크 깊이)

def add(p, *vs):
    x, y = p
    for v in vs:
        x, y = x + v[0], y + v[1]
    return (x, y)

def quad(p, u, v):
    return ' '.join(f'{x:.0f},{y:.0f}' for x, y in (p, add(p, u), add(p, u, v), add(p, v)))

P2 = add(P1, U)
DF1, DF2 = add(P1, FWD), add(P2, FWD)          # 데크 앞쪽 두 모서리
SCREEN_M = f'matrix({U[0]/100},{U[1]/100},{V[0]/100},{V[1]/100},{P1[0]},{P1[1]})'

a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')

a('''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0.4" y2="1">
  <stop offset="0" stop-color="#f4f7fb"/><stop offset="1" stop-color="#e1e7f0"/>
</linearGradient>
<linearGradient id="desk" x1="0" y1="0" x2="0.3" y2="1">
  <stop offset="0" stop-color="#ddb28c"/><stop offset="1" stop-color="#c08f66"/>
</linearGradient>
<linearGradient id="lid" x1="0" y1="0" x2="0.4" y2="1">
  <stop offset="0" stop-color="#eef2f7"/><stop offset="1" stop-color="#c3cbd5"/>
</linearGradient>
<linearGradient id="deck" x1="0.1" y1="0" x2="0.6" y2="1">
  <stop offset="0" stop-color="#f3f6fa"/><stop offset="1" stop-color="#c9d1da"/>
</linearGradient>
<linearGradient id="glass" x1="0" y1="1" x2="0.4" y2="0">
  <stop offset="0" stop-color="#1c202b"/><stop offset="1" stop-color="#0d0f15"/>
</linearGradient>
<linearGradient id="feed" x1="0" y1="0" x2="0.4" y2="1">
  <stop offset="0" stop-color="#3b4252"/><stop offset="1" stop-color="#222734"/>
</linearGradient>
<linearGradient id="coral" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#ff8a3d"/><stop offset="1" stop-color="#f0473a"/>
</linearGradient>
<radialGradient id="shadow" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#2a1d12" stop-opacity="0.36"/>
  <stop offset="1" stop-color="#2a1d12" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#ff7a52" stop-opacity="0.26"/>
  <stop offset="1" stop-color="#ff7a52" stop-opacity="0"/>
</radialGradient>
</defs>''')

# ── 배경 + 책상 ──
a(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
a('<polygon points="0,236 500,120 500,500 0,500" fill="url(#desk)"/>')
a('<polygon points="0,236 500,120 500,129 0,245" fill="#b1815c" opacity="0.45"/>')

# 화면 빛 번짐 + 접지 그림자
a('<ellipse cx="248" cy="232" rx="188" ry="136" fill="url(#glow)"/>')
CEN = ((P1[0]+P2[0]+DF1[0]+DF2[0])/4, (P1[1]+P2[1]+DF1[1]+DF2[1])/4)
a(f'<ellipse cx="{CEN[0]:.0f}" cy="{CEN[1]+24:.0f}" rx="162" ry="44" fill="url(#shadow)"/>')

# ── 데크(키보드 면) + 두께 ──
a(f'<polygon points="{quad(P1, U, FWD)}" fill="url(#deck)"/>')
a(f'<polygon points="{DF1[0]:.0f},{DF1[1]:.0f} {DF2[0]:.0f},{DF2[1]:.0f}'
  f' {DF2[0]:.0f},{DF2[1]+10:.0f} {DF1[0]:.0f},{DF1[1]+10:.0f}" fill="#9fa9b5"/>')
a(f'<polygon points="{P1[0]:.0f},{P1[1]:.0f} {DF1[0]:.0f},{DF1[1]:.0f}'
  f' {DF1[0]:.0f},{DF1[1]+10:.0f} {P1[0]:.0f},{P1[1]+10:.0f}" fill="#8e98a5"/>')
# 트랙패드
a(f'<polygon points="{quad(add(P1, (74, 10), (28, 20)), (58, -10), (26, 19))}"'
  ' fill="#dbe1e8" stroke="#bcc5cf" stroke-width="1"/>')

# ── 화면 ──
a(f'<polygon points="{quad(P1, U, V)}" fill="url(#lid)" stroke="#aab4bf" stroke-width="1.5"/>')
a('<g transform="' + SCREEN_M + '">')
a('<rect x="4" y="7" width="92" height="86" rx="2" fill="url(#glass)"/>')

# 카메라 뷰
a('<rect x="9" y="27" width="48" height="60" rx="1.5" fill="url(#feed)"/>')
a('<ellipse cx="33" cy="36" rx="18" ry="13" fill="#8ea2bb"/>')      # 어깨
a('<circle cx="33" cy="60" r="10" fill="#a0b3c9"/>')                # 머리
a('<rect x="16" y="31" width="34" height="47" fill="none" stroke="#ff6a52" stroke-width="2"/>')
for cx_, cy_ in ((16, 31), (50, 31), (16, 78), (50, 78)):
    a(f'<circle cx="{cx_}" cy="{cy_}" r="2.4" fill="#ff6a52"/>')
a('<line x1="9" y1="66" x2="57" y2="66" stroke="#ff8a3d" stroke-width="1.1" opacity="0.5"/>')

# 수집한 학습 샘플 스트립 (카메라 뷰 아래)
for i in range(3):
    x = 9 + i * 16.5
    a(f'<rect x="{x}" y="13" width="14" height="11" rx="1.2" fill="#2e3542"/>')
    a(f'<circle cx="{x + 7}" cy="19" r="3.4" fill="#7f91a8"/>')
a('<rect x="9" y="13" width="14" height="11" rx="1.2" fill="none" stroke="#ff6a52" stroke-width="1.4"/>')

# 결과 패널 — 도넛 게이지 + 클래스 막대 3개
a('<circle cx="76" cy="62" r="15" fill="none" stroke="#39414f" stroke-width="4"/>')
a('<circle cx="76" cy="62" r="15" fill="none" stroke="url(#coral)" stroke-width="4"'
  ' stroke-linecap="round" stroke-dasharray="82 13" transform="rotate(-92 76 62)"/>')
for i, (yy, wfill) in enumerate(((33, 28), (24, 12), (15, 6))):
    a(f'<rect x="61" y="{yy}" width="30" height="4.5" rx="2.2" fill="#2e3542"/>')
    a(f'<rect x="61" y="{yy}" width="{wfill}" height="4.5" rx="2.2"'
      f' fill="{"url(#coral)" if i == 0 else "#596舎"}"/>'.replace('#596舎', '#5a6473'))
a('</g>')

a('</svg>')

base = os.path.dirname(__file__) or '.'
open(f'{base}/ai-train-infer.svg', 'w').write('\n'.join(out))
print('svg written')
