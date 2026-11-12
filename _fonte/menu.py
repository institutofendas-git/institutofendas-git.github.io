"""Menu de todas as páginas. Nas fontes, o cabeçalho é o marcador <!--MENU:ativo-->.
ativo: 'inicio' | 'final' | 'f:<slug-do-formato>' (página de formato ou de curso daquele formato)."""
import re, rastreio

ABERTO_HREF = '/#aberto'  # com eventos abertos: o evento (se um só) ou '/#aberto'
ABERTO_CLASSE = 'so-campanha'

FORMATOS = [('clubes-do-livro', 'Clubes do livro'), ('minicursos', 'Minicursos'), ('capacitacoes', 'Capacitações'),
            ('grupos-de-estudos', 'Grupos de estudos'), ('cursos', 'Cursos')]
CARET = '<svg class="caret" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>'

CSS = r"""
/* ---------- menu ---------- */
[hidden]{display:none!important}
.topo .mwrap{display:flex;align-items:center;gap:14px;height:64px}
.topo .mwrap .logo{margin-right:auto;display:flex}
.topo nav.nav-desk{display:none}
.mbtn{display:inline-flex;align-items:center;justify-content:center;white-space:nowrap;border:1.5px solid rgba(249,242,222,.55);color:var(--creme);text-decoration:none;font-weight:600;font-size:13.5px;border-radius:999px;padding:9px 16px;line-height:1}
.mbtn:hover{background:var(--creme);color:var(--vinho)}
.burger{width:44px;height:44px;flex:none;display:grid;place-items:center;background:transparent;border:0;color:var(--creme);cursor:pointer;padding:0;margin-right:-8px}
.burger svg{width:26px;height:26px}
.burger .x{display:none}.burger[aria-expanded="true"] .x{display:block}.burger[aria-expanded="true"] .tres{display:none}
.topo nav.menu-painel{display:block;margin:0;font-size:inherit;border-top:1px solid rgba(249,242,222,.14);height:calc(100vh - 64px - env(safe-area-inset-top));height:calc(100dvh - 64px - env(safe-area-inset-top));overflow:auto;overscroll-behavior:contain}
.topo nav.menu-painel[hidden]{display:none}
.topo .menu-painel .wrap{display:block;height:auto}
.menu-painel ul{list-style:none;margin:0;padding:0}
.menu-painel>.wrap>ul{padding:6px 0 18px}
.menu-painel li{border-bottom:1px solid rgba(249,242,222,.1)}
.menu-painel li:last-child{border-bottom:0}
.menu-painel a,.menu-painel .sub-btn{display:flex;align-items:center;gap:10px;width:100%;min-height:54px;padding:12px 0;color:var(--creme);text-decoration:none;font:inherit;font-size:18px;font-weight:600;background:none;border:0;text-align:left;cursor:pointer}
.menu-painel a:hover,.menu-painel .sub-btn:hover{color:#fff}
.menu-painel .on>a,.menu-painel a.on,.menu-painel .sub-btn.on{color:#FF8A80}
.menu-painel .caret{width:18px;height:18px;transition:transform .2s;color:var(--vermelho)}
.menu-painel .sub-btn[aria-expanded="true"] .caret{transform:rotate(180deg)}
.menu-painel .sub{padding:0 0 10px 18px;border-left:2px solid var(--vermelho);margin-left:2px}
.menu-painel .sub[hidden]{display:none}
.menu-painel .sub li{border:0}
.menu-painel .sub a{font-size:16px;font-weight:400;min-height:44px;padding:8px 0;color:#E9DCC2}
.menu-painel .sub a.on{color:#fff;font-weight:600}
.menu-painel .sub a.on::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--vermelho);margin-left:-22px;margin-right:10px}
.menu-painel .tag{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;background:var(--vermelho);color:#fff;border-radius:999px;padding:4px 8px;font-weight:600}
body.menu-aberto{overflow:hidden}
@media(max-width:380px){.mbtn{padding:8px 12px;font-size:12.5px}.topo .mwrap{gap:8px}}
@media(min-width:1000px){
 .burger,.topo nav.menu-painel{display:none!important}
 .topo nav.nav-desk{display:flex;align-items:center;gap:4px;margin:0 8px 0 0;font-size:14.5px}
 .nav-desk>a,.nav-desk summary{color:var(--creme);text-decoration:none;opacity:.85;padding:10px 12px;border-radius:6px;cursor:pointer;display:flex;align-items:center;gap:6px;list-style:none}
 .nav-desk summary::-webkit-details-marker{display:none}
 .topo .nav-desk details{border:0!important}
 .topo .nav-desk summary{font-size:inherit;font-weight:400;line-height:1.2;justify-content:flex-start;gap:6px}
 .topo .nav-desk summary::after{content:none!important;display:none!important}
 .topo .nav-desk .drop a{font-weight:400}.topo .nav-desk .drop a.on{font-weight:600}
 .nav-desk>a:hover,.nav-desk summary:hover,.nav-desk details[open] summary{opacity:1;background:rgba(249,242,222,.08)}
 .nav-desk .on,.nav-desk details.on summary{opacity:1;color:#fff;box-shadow:inset 0 -2px 0 var(--vermelho)}
 .nav-desk .caret{width:15px;height:15px;transition:transform .2s}
 .nav-desk details[open] .caret{transform:rotate(180deg)}
 .nav-desk details{position:relative}
 .nav-desk .drop{position:absolute;top:calc(100% + 8px);left:0;min-width:230px;background:var(--papel);border-radius:8px;padding:8px;box-shadow:0 24px 44px -18px rgba(39,20,22,.45);display:flex;flex-direction:column}
 .nav-desk .drop a{color:var(--escuro);text-decoration:none;padding:10px 12px;border-radius:6px;font-size:15px}
 .nav-desk .drop a:hover{background:#F2EAD6;color:var(--vinho)}
 .nav-desk .drop a.on{color:var(--vinho);font-weight:600;background:#F2EAD6}
}
"""

JS = r"""<script>
(function(){try{if(Date.now()>=Date.parse('2026-12-12T00:00:00-03:00')){document.querySelectorAll('.so-campanha').forEach(function(e){e.remove()});document.querySelectorAll('.pos-campanha').forEach(function(e){e.hidden=false})}}catch(e){}})();
(function(){
  var b=document.querySelector('.burger'),p=document.getElementById('menu-painel');
  function fecha(){if(!p)return;p.hidden=true;b.setAttribute('aria-expanded','false');document.body.classList.remove('menu-aberto')}
  if(b&&p){
    b.addEventListener('click',function(){var abre=p.hidden;p.hidden=!abre;b.setAttribute('aria-expanded',abre?'true':'false');document.body.classList.toggle('menu-aberto',abre)});
    p.querySelectorAll('a').forEach(function(a){a.addEventListener('click',fecha)});
  }
  document.querySelectorAll('.sub-btn').forEach(function(s){s.addEventListener('click',function(){var u=document.getElementById(s.getAttribute('aria-controls'));var abre=u.hidden;u.hidden=!abre;s.setAttribute('aria-expanded',abre?'true':'false')})});
  var d=document.querySelector('.nav-desk details');
  if(d){document.addEventListener('click',function(e){if(d.open&&!d.contains(e.target))d.open=false});d.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){d.open=false})})}
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){fecha();if(d)d.open=false}});
})();
</script>"""


def header(ativo):
    fat = ativo[2:] if ativo.startswith('f:') else None
    on = lambda c: ' class="on"' if c else ''
    sub = ''.join(f'<li><a href="/formatos/{s}/"{on(s == fat)}>{n}</a></li>' for s, n in FORMATOS)
    drop = ''.join(f'<a href="/formatos/{s}/"{on(s == fat)}>{n}</a>' for s, n in FORMATOS)
    if ativo == 'final':
        botao = '<a class="mbtn" href="#combos">Ver combos</a>'
    else:
        botao = f'<a class="mbtn {ABERTO_CLASSE} aberto-agora" href="{ABERTO_HREF}">Aberto agora</a>'
    return f"""<header class="topo">
  <div class="wrap mwrap">
    <a class="logo" href="/"><img src="{{{{of/wm-branco-verm.svg}}}}" alt="Instituto Fendas" width="1830" height="331"></a>
    <nav class="nav-desk" aria-label="Menu">
      <a href="/"{on(ativo == 'inicio')}>Início</a>
      <a href="/#quem-somos">Quem somos</a>
      <details{on(fat)}><summary>Formatos{CARET}</summary><div class="drop">{drop}</div></details>
      <a href="/#eventos">Eventos de 2026</a>
      <a href="/#contato">Contato</a>
    </nav>
    {botao}
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu-painel" aria-label="Abrir o menu"><svg class="tres" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg><svg class="x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
  </div>
  <nav class="menu-painel" id="menu-painel" aria-label="Menu" hidden>
    <div class="wrap"><ul>
      <li><a href="/"{on(ativo == 'inicio')}>Início</a></li>
      <li><a href="/#quem-somos">Quem somos</a></li>
      <li><button class="sub-btn{' on' if fat else ''}" type="button" aria-expanded="{'true' if fat else 'false'}" aria-controls="menu-sub">Formatos{CARET}</button>
        <ul class="sub" id="menu-sub"{'' if fat else ' hidden'}>{sub}</ul></li>
      <li><a href="/#eventos">Eventos de 2026</a></li>
      <li class="so-campanha"><a href="/final-de-ano/"{on(ativo == 'final')}>Final de ano no Fendas <span class="tag">aberto</span></a></li>
      <li><a href="/#contato">Contato</a></li>
    </ul></div>
  </nav>
</header>"""


def aplicar(html):
    m = re.search(r'<!--MENU:([a-z:-]+)-->', html)
    if not m:
        return html
    html = html.replace(m.group(0), header(m.group(1)))
    anim = m.group(1) != 'inicio'
    html = html.replace('</style>', CSS + GERAL_CSS + (ANIM_CSS if anim else '') + '</style>', 1)
    html = html.replace('<style>', HEAD + '<style>', 1)
    html = re.sub(r"@font-face\{font-family:'Syne'[^\n]*\n", '', html)
    html = re.sub(r'<body>', '<body>\n<a class="pular" href="#inicio">Pular para o conteúdo</a>', html, count=1)
    html = html.replace('</body>', JS + GERAL_JS + (ANIM_JS if anim else '') + '\n</body>', 1)
    html = re.sub(r'<span>Instituto Fendas(?: © \d{4})? · CNPJ', '<span>© <span class="ano">2026</span> Instituto Fendas · CNPJ', html)
    html = html.replace('</body>', "<script>(function(){var a=Math.max(2026,new Date().getFullYear());document.querySelectorAll('.ano').forEach(function(e){e.textContent=a})})();</script>\n</body>", 1)
    return rastreio.aplicar(html)


def og(titulo, desc, caminho, alt):
    from html import escape as e
    u = 'https://institutofendas.com.br' + caminho
    return f"""<meta property="og:type" content="website">
<meta property="og:site_name" content="Instituto Fendas">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{u}preview.jpg">
<meta property="og:image:secure_url" content="{u}preview.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(alt)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{u}">
<meta name="description" content="{e(desc)}">"""


def sem_depoimentos(html):
    import re
    return re.sub(r'<section class="sec depo"[^>]*>.*?</section>\s*', '', html, flags=re.S)


HEAD = """<meta name="theme-color" content="#750A21">
<link rel="stylesheet" href="{{FONTES}}">
"""
GERAL_CSS = r"""
/* ---------- geral: acessibilidade e movimento ---------- */
.pular{position:absolute;left:12px;top:-60px;z-index:100;background:var(--creme);color:var(--vinho);padding:10px 14px;border-radius:6px;font-weight:600;text-decoration:none}
.pular:focus{top:12px}
:focus-visible{outline:3px solid var(--vermelho);outline-offset:3px}
.topo :focus-visible,.hero :focus-visible,.fecho :focus-visible,footer :focus-visible{outline-color:var(--creme)}

@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}.rv{opacity:1;transform:none}@view-transition{navigation:none}}
"""
GERAL_JS = ""
# Animações de entrada ao rolar: ligadas em todas as páginas MENOS a inicial (travavam lá; decisão de Ilo, 11/11/2026).
ANIM_CSS = r"""
.rv{opacity:0;transform:translateY(22px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.rv.in{opacity:1;transform:none}
html.js img[loading=lazy]{opacity:0;transition:opacity .5s}html.js img[loading=lazy].ok{opacity:1}
@media(prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}}
"""
ANIM_JS = r"""<script>
(function(){
  document.documentElement.classList.add('js');document.querySelectorAll('img[loading=lazy]').forEach(function(i){if(i.complete)i.classList.add('ok');else{i.addEventListener('load',function(){i.classList.add('ok')});i.addEventListener('error',function(){i.classList.add('ok')})}});
  if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion:reduce)').matches)return;
  var els=document.querySelectorAll('.sec .cab,.fcard,.cards>li,.chips,.tile,.pessoa,.encontros>li,.cert,.card-aberto,.combo,.nome-fenda,.pergs li,.linha-tempo>li,.ensaio,.qs-foto,.chamada,.dobra,.faq details,.passos>li');
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
  els.forEach(function(el,i){if(el.getBoundingClientRect().top<innerHeight*.92)return;el.classList.add('rv');var p=el.previousElementSibling;if(p&&p.classList.contains('rv'))el.style.transitionDelay=(Math.min(i%4,3)*70)+'ms';io.observe(el)});
})();
</script>"""
