"""Archivo de informes semanales del Canal Digital.

Uso:  python3 herramientas/archivo.py [páginas extra...]
1. Lee semanas.json (una entrada por semana publicada; la última es la más reciente).
2. Pone el selector de semana en index.html, en cada semanas/*.html y en las páginas extra.
3. Regenera archivo.html con el resumen de todas las semanas.
Para agregar una semana: copia su página a semanas/<mes>-<semana>.html y a index.html,
agrega su fila al final de semanas.json y corre este script.
"""
import json, re, sys, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
S = json.loads((R/'semanas.json').read_text(encoding='utf-8'))
A, Z = '<!--ARCHIVO-->', '<!--/ARCHIVO-->'

def nav(actual):
    ops = ''.join(f'<option value="{s["archivo"]}"{" selected" if s["semana"]==actual else ""}>Semana {s["semana"]} · {s["fechas"]}</option>' for s in reversed(S))
    return (A + '<div class="arch"><label for="archSel">Ver otra semana</label>'
      f'<select id="archSel">{ops}</select><a id="archLink" href="archivo.html">Archivo de informes</a></div>'
      '<style>.arch{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;width:100%;font-size:14px;color:var(--muted)}'
      '.arch select{font:inherit;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:6px 10px;max-width:100%}'
      '.arch a{color:var(--accent);font-weight:600}</style>'
      '<script>(()=>{const inS=/\\/semanas\\//.test(location.pathname),b=inS?"":"semanas/";'
      'document.getElementById("archLink").href=(inS?"../":"")+"archivo.html";'
      'document.getElementById("archSel").addEventListener("change",e=>{location.href=b+e.target.value})})()</script>' + Z)

def inject(p):
    t = p.read_text(encoding='utf-8')
    m = re.search(r'Canal Digital · Semana (\d+\.\d+)</h1>', t)
    if not m: print('sin semana:', p); return
    t = re.sub(re.escape(A)+'.*?'+re.escape(Z), '', t, flags=re.S)
    i = t.index('<nav class="tabs"'); j = t.rindex('</div>', 0, t.rindex('</header>', 0, i))
    t = t[:j] + nav(m.group(1)) + '\n  ' + t[j:]
    p.write_text(t, encoding='utf-8'); print('selector:', p.name, m.group(1))

for p in [R/'index.html', *sorted((R/'semanas').glob('*.html')), *map(pathlib.Path, sys.argv[1:])]:
    inject(p)

head = (R/'index.html').read_text(encoding='utf-8')
css = head[head.index(':root{'):head.index('*{box-sizing')]
M = lambda v: '$' + f'{round(v):,}'.replace(',', '.')
P = lambda v, d=1: f'{v*100:.{d}f}'.replace('.', ',') + ' %'
X = lambda v: f'{v:.1f}'.replace('.', ',') + '×'
rows = ''
for k, s in enumerate(reversed(S)):
    rows += (f'<tr{" class=cur" if k==0 else ""}><td><a href="semanas/{s["archivo"]}"><b>{s["semana"]}</b></a><small>{s["fechas"]}</small></td>'
      f'<td>{M(s["mahalo"])}</td><td class="{"up" if s["pv"]>=1 else "dn"}">{P(s["pv"])}</td><td>{M(s["shopify"])}</td>'
      f'<td>{s["pedidos"]}</td><td>{P(s["conversion"],2)}</td><td>{M(s["inversion"])}</td><td>{X(s["roas_meta"])}</td><td>{X(s["roas_google"])}</td></tr>')
ult = S[-1]
html = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Archivo Canal Digital</title>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}*{{box-sizing:border-box}}
body{{background:var(--bg);color:var(--ink);font-family:var(--body);margin:0;line-height:1.5}}
.wrap{{max-width:1080px;margin:0 auto;padding:28px 16px 48px}}
h1{{font-family:var(--display);font-size:clamp(26px,5vw,36px);margin:4px 0 6px;letter-spacing:-.015em}}
.eyebrow{{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600}}
p{{color:var(--muted);margin:0 0 20px}} a{{color:var(--accent)}}
.panel{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px;overflow-x:auto}}
table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:14px}}
th,td{{text-align:right;padding:10px 12px;border-bottom:1px solid var(--line);white-space:nowrap}}
th:first-child,td:first-child{{text-align:left}} th{{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}}
td small{{display:block;color:var(--muted)}} tr.cur td{{background:var(--accent-soft)}}
.up{{color:var(--pos)}}.dn{{color:var(--neg)}} .btn{{display:inline-block;margin-bottom:18px;font-weight:600}}
</style></head><body><main class="wrap">
<div class="eyebrow">UB Cuarenta · Canal Digital</div>
<h1>Archivo de informes semanales</h1>
<p>Cada semana publicada queda guardada aquí. Toca la semana para abrir su informe completo.</p>
<a class="btn" href="./">Ver el informe más reciente (semana {ult["semana"]}) →</a>
<div class="panel"><table>
<thead><tr><th>Semana</th><th>Venta Mahalo</th><th>Cumpl. PV</th><th>Venta Shopify</th><th>Pedidos</th><th>Conversión</th><th>Inversión pauta</th><th>ROAS Meta</th><th>ROAS Google</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p style="margin-top:14px;font-size:13px">ROAS según cada plataforma. Venta Mahalo y Shopify con IVA.</p>
</main></body></html>
'''
(R/'archivo.html').write_text(html, encoding='utf-8'); print('archivo.html:', len(S), 'semanas')
