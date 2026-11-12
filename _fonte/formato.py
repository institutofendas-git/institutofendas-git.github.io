"""Gera as páginas de formato: python3 formato.py -> formato-<slug>-src.html"""
import curso
from curso import CSS, ICONS, ICON_UP, ICON_DOWN, ICON_LOCK, CURSOS, BIOS, esc, card, CARDS_CSS, ORDEM
from dados import FORMATOS, FUNDADORES
from menu import og

MARCA_F = {'clubes-do-livro':('camadas',-8),'minicursos':('explosaao',0),'capacitacoes':('caminhos',-24),'grupos-de-estudos':('intersec',-10),'cursos':('fenda',0)}
ICON_F = {'Encontros': 'stack', 'Carga': 'award', 'Para quem': 'users'}

CSS_F = r"""
.hero-formato>.wrap{grid-template-columns:1fr!important}
.hero-formato .hero-txt{max-width:760px}
.hero-formato .marca{right:-30vw;top:30%;width:min(100vw,520px);opacity:.9}
@media(min-width:900px){.hero-formato .marca{right:-60px;top:46%;width:600px}}
.hero-formato .mais-txt{font-size:16px;line-height:1.6;color:#E9DCC2;max-width:56ch}
@media(min-width:900px){.resumo-3 ul{grid-template-columns:repeat(3,1fr)}}
.outros{display:flex;flex-wrap:wrap;gap:10px}
.outros a{display:inline-flex;align-items:center;gap:8px;padding:12px 18px;border-radius:999px;border:1.5px solid var(--vinho);color:var(--vinho);text-decoration:none;font-weight:600;font-size:15px}
.outros a:hover{background:var(--vinho);color:var(--creme)}
"""


def gerar(fslug, nome, plural, desc, longo, fatos):
    cursos = [s for s in ORDEM if CURSOS[s]['formato_slug'] == fslug]
    resumo = ''.join(f'<li>{ICONS[ICON_F[k]]}<div><span>{k}</span><strong>{esc(v)}</strong></div></li>' for k, v in fatos)
    outros = ''.join(f'<a href="/formatos/{s}/">{esc(p)}</a>' for s, _, p, *_ in FORMATOS if s != fslug)
    cards = ''.join(card(s) for s in cursos)
    n = len(cursos)
    base = open('base.css').read()
    page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(plural)} online em saúde e interseccionalidade, com certificado | Instituto Fendas</title>
{og(plural + " | Instituto Fendas", desc + " Online, ao vivo e gravados, com certificado.", f"/formatos/{fslug}/", plural + " do Instituto Fendas")}
<link rel="icon" href="{{{{of/avatar64.png}}}}">
<style>
@font-face{{font-family:'Syne';font-weight:400;font-display:swap;src:url({{{{syne-latin-400-normal.woff2}}}}) format('woff2')}}
@font-face{{font-family:'Syne';font-weight:600;font-display:swap;src:url({{{{syne-latin-600-normal.woff2}}}}) format('woff2')}}
@font-face{{font-family:'Syne';font-weight:700;font-display:swap;src:url({{{{syne-latin-700-normal.woff2}}}}) format('woff2')}}
{base}
{CSS}
{CARDS_CSS}
{CSS_F}
</style>
</head>
<body>
<!--MENU:f:{fslug}-->
<nav class="trilha" aria-label="Você está em"><div class="wrap"><a href="/">Início</a><span aria-hidden="true">›</span><b>{esc(plural)}</b></div></nav>

<main id="inicio">
<section class="hero hero-formato">
  <img class="marca" src="{{{{of/ic-{MARCA_F[fslug][0]}.svg|#d62929=#A62340}}}}" style="--giro:{MARCA_F[fslug][1]}deg" alt="" aria-hidden="true">
  <div class="wrap">
    <div class="hero-txt">
      <p class="eyebrow">Formato · Instituto Fendas</p>
      <h1>{esc(plural)}</h1>
      <p class="chamada">{esc(desc)}</p>
      <p class="mais-txt">{esc(longo)}</p>
    </div>
  </div>
  <div class="resumo resumo-3"><ul class="wrap">{resumo}</ul></div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="cab"><h2>Eventos de 2026</h2><p>O que aconteceu ao vivo neste formato em 2026. As turmas já foram encerradas. Toque para ver como foi.</p></div>
    <ul class="cards">{cards}</ul>
  </div>
</section>

<section class="sec" style="background:#F2EAD6">
  <div class="wrap">
    <div class="cab"><h2>Outros formatos</h2></div>
    <div class="outros">{outros}</div>
  </div>
</section>
</main>

<footer id="fim">
  <div class="wrap">
    <img src="{{{{of/wm-branco-verm.svg}}}}" alt="Instituto Fendas" width="1830" height="331">
    <span>Instituto Fendas · CNPJ 65.465.820/0001-02 · Fortaleza, CE</span>
  </div>
</footer>

<nav class="setas" aria-label="Navegar pela página">
  <a href="#inicio" aria-label="Voltar ao início">{ICON_UP}</a>
  <a href="#fim" aria-label="Ir para o fim">{ICON_DOWN}</a>
</nav>
<script>
(function(){{var s=document.querySelector('.setas');function u(){{s.classList.toggle('on',window.scrollY>window.innerHeight*0.6)}}window.addEventListener('scroll',u,{{passive:true}});u()}})();
</script>
</body>
</html>"""
    open(f'formato-{fslug}-src.html', 'w').write(page)


if __name__ == '__main__':
    for f in FORMATOS:
        gerar(*f)
