"""Gera home4-src.html a partir de home3-src.html: eventos em ordem cronológica com filtro, fotos como <img>, blocos pós-campanha."""
import re, json
from curso import card, CARDS_CSS, ORDEM, CURSOS
from dados import FORMATOS
s = open('home3-src.html').read()
def rep(a, b, n=1):
    global s
    assert a in s, a[:70]; s = s.replace(a, b, n)
chips = '<button type="button" class="chip on" data-f="" aria-pressed="true">Todos</button>' + ''.join(
    f'<button type="button" class="chip" data-f="{f[0]}" aria-pressed="false">{f[2]}</button>' for f in FORMATOS)
lista = ''.join(card(x, desc=True) for x in ORDEM)
a = s.index('<ul>', s.index('<section class="sec formacoes"')); b = s.index('</ul>', a) + 5
s = s[:a] + f'<div class="chips" role="group" aria-label="Filtrar por formato">{chips}</div>\n    <ul class="cards" id="lista-eventos">{lista}</ul>' + s[b:]
rep('<section class="sec formacoes" id="formacoes">', '<section class="sec formacoes" id="eventos">')
rep('As turmas abaixo já foram encerradas.</p>', 'Em ordem de data. As turmas abaixo já foram encerradas.</p>')
rep('href="#formacoes"', 'href="#eventos"', 0) if 'href="#formacoes"' in s else None
s = re.sub(r'<div class="foto" style="background-image:url\(({{fotos/p-[a-z]+\.webp}})\)" role="img" aria-label="([^"]+)"></div>',
           r'<div class="foto"><img src="\1" alt="\2" loading="lazy" decoding="async" width="640" height="800"></div>', s)
rep('</style>', CARDS_CSS + '''
.cards .desc{font-size:14.5px;line-height:1.5;color:var(--texto)}
@media(max-width:699px){.cards .desc{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}}
.cards li[hidden]{display:none}
.chips{display:flex;gap:8px;overflow-x:auto;margin:0 calc(-1*var(--pad)) 20px;padding:2px var(--pad) 6px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chip{flex:none;font:600 14px/1 'Syne',sans-serif;padding:11px 16px;border-radius:999px;border:1.5px solid var(--vinho);background:transparent;color:var(--vinho);cursor:pointer;transition:background .15s,color .15s}
.chip:hover{background:#F2EAD6}.chip.on{background:var(--vinho);color:var(--creme)}
@media(min-width:900px){.chips{flex-wrap:wrap;overflow:visible;margin:0 0 26px;padding:0}}
.pessoa .foto{position:relative;background:var(--linha)}.pessoa .foto img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center top}
</style>
<script type="application/ld+json">''' + json.dumps({"@context": "https://schema.org", "@type": "EducationalOrganization", "name": "Instituto Fendas", "alternateName": "Instituto Fendas de Saúde, Cultura e Interseccionalidade", "url": "https://institutofendas.com.br/", "logo": "https://institutofendas.com.br/preview.jpg", "email": "institutofendas@gmail.com", "sameAs": ["https://instagram.com/institutofendas"], "address": {"@type": "PostalAddress", "addressLocality": "Fortaleza", "addressRegion": "CE", "addressCountry": "BR"}}, ensure_ascii=False) + '</script>')
rep('<div class="acoes so-campanha"><a class="btn btn-vermelho" href="#aberto">Ver o que está aberto</a></div>',
    '<div class="acoes so-campanha"><a class="btn btn-vermelho" href="#aberto">Ver o que está aberto</a></div><div class="acoes pos-campanha" hidden><a class="btn btn-vermelho" href="#eventos">Ver os eventos de 2026</a></div>')
rep('<section class="sec" id="o-que-fazemos">', '''<section class="sec aberto pos-campanha" hidden>
  <div class="wrap">
    <div class="cab"><p class="eyebrow" style="color:var(--vermelho);font-weight:600">em breve</p><h2>Os próximos eventos</h2><p>As novas turmas são anunciadas primeiro no Instagram do Instituto.</p></div>
    <a class="btn btn-vermelho" href="https://instagram.com/institutofendas">Acompanhar no Instagram</a>
  </div>
</section>

<section class="sec" id="o-que-fazemos">''')
rep('</script>\n</body>', '''(function(){var cs=document.querySelectorAll('.chip'),ls=document.querySelectorAll('#lista-eventos>li');cs.forEach(function(c){c.addEventListener('click',function(){cs.forEach(function(x){var on=x===c;x.classList.toggle('on',on);x.setAttribute('aria-pressed',on)});ls.forEach(function(l){l.hidden=!!c.dataset.f&&l.dataset.formato!==c.dataset.f})})})})();
</script>
</body>''')
open('home4-src.html', 'w').write(s)
