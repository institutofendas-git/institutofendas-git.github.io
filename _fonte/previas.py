"""Gera as imagens de prévia (1200x630) das páginas de curso e de formato em ./previas/"""
import asyncio, os, html
from playwright.async_api import async_playwright
import curso, formato, tema
from curso import CURSOS
from dados import FORMATOS
B = 'file:///home/claude/fendas/'
os.makedirs('previas', exist_ok=True)
CSS = f"""@font-face{{font-family:S;font-weight:400;src:url({B}assets/syne-latin-400-normal.woff2)}}
@font-face{{font-family:S;font-weight:700;src:url({B}assets/syne-latin-700-normal.woff2)}}
body{{margin:0;width:1200px;height:630px;background:#8E1834;font-family:S;color:#F9F2DE;position:relative;overflow:hidden}}
.marca{{position:absolute;opacity:1}}
.txt{{position:absolute;left:72px;top:64px;bottom:64px;width:{{W}}px;display:flex;flex-direction:column}}
.logo{{height:34px;align-self:flex-start}}
.eb{{margin-top:auto;font-size:20px;letter-spacing:.14em;text-transform:uppercase;color:#C2B299}}
h1{{margin:14px 0 0;font-size:{{F}}px;line-height:1.04;font-weight:700;color:#fff}}
p{{margin:16px 0 0;font-size:28px;line-height:1.25;color:#F2E4CB}}
.capa{{position:absolute;right:72px;top:75px;width:480px;height:480px;border-radius:10px;background-size:cover;background-position:center;box-shadow:0 30px 50px -30px rgba(0,0,0,.7)}}"""
def pag(eb, tit, sub, img=None, ic=None, giro=0):
    W = 520 if img else 760
    F = 64 if len(tit) < 26 else 52 if len(tit) < 40 else 44
    css = CSS.replace('{W}', str(W)).replace('{F}', str(F))
    m = f'<img class="marca" src="{B}of/ic-{ic}.svg" style="right:-80px;top:120px;width:620px;transform:rotate({giro}deg);filter:brightness(.62) saturate(1.1)">' if ic else ''
    c = f'<div class="capa" style="background-image:url({B}{img})"></div>' if img else ''
    return f'<html><head><style>{css}</style></head><body>{m}{c}<div class="txt"><img class="logo" src="{B}of/wm-branco-verm.svg"><div class="eb">{html.escape(eb)}</div><h1>{html.escape(tit)}</h1><p>{html.escape(sub)}</p></div></body></html>'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        jobs = [(f'curso-{s}', pag(c['formato'] + ' · encerrado', c['nome'], c['sub'], img=c['img'])) for s, c in CURSOS.items()]
        jobs += [(f'formato-{f[0]}', pag('Formato', f[2], f[3], ic=formato.MARCA_F[f[0]][0], giro=formato.MARCA_F[f[0]][1])) for f in FORMATOS]
        jobs += [(f"tema-{t['slug']}", pag('Tema', t['nome'], t['chamada'], ic=t['marca'][0], giro=t['marca'][1])) for t in tema.TEMAS]
        for nome, h in jobs:
            open('/tmp/_p.html', 'w').write(h); await pg.goto('file:///tmp/_p.html'); await pg.wait_for_timeout(250)
            await pg.screenshot(path=f'previas/{nome}.jpg', type='jpeg', quality=86)
        await b.close()
asyncio.run(main())
