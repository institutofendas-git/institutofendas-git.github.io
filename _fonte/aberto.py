"""Bloco 'Inscrições abertas' montado a partir dos eventos com status 'aberto' (regras em site-do-instituto.md
e modelo aprovado em modelo-cartoes-inscricoes-abertas.html). Ordem pela data de início; cada cartão some
sozinho no dia do primeiro encontro."""
import html as H
from curso import CURSOS

CSS = r"""
.abertos{display:grid;gap:14px}
.ab{position:relative;display:grid;background:var(--papel);border-radius:8px;overflow:hidden;box-shadow:0 22px 40px -30px rgba(39,20,22,.55);text-decoration:none;color:inherit;transition:transform .18s,box-shadow .18s}
.ab:hover{transform:translateY(-3px);box-shadow:0 28px 44px -26px rgba(39,20,22,.6)}
.ab .cap{position:relative;background:var(--vinho);min-height:190px}
.ab .cap img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ab .tx{padding:clamp(18px,2.6vw,30px);display:flex;flex-direction:column;gap:10px;min-width:0}
.ab .selo{align-self:flex-start;background:var(--vermelho);color:#fff;font-size:12px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;border-radius:999px;padding:6px 12px}
.ab h3{font-size:clamp(22px,2.6vw,30px);line-height:1.15;color:var(--vinho)}
.ab h3 span{display:block;font-weight:400;font-size:.62em;margin-top:4px;color:var(--escuro)}
.ab .ds{font-size:16px;line-height:1.5;color:var(--texto)}
.ab .dados{display:flex;flex-wrap:wrap;gap:10px 24px;border-top:1.5px solid var(--linha);padding-top:12px;margin-top:2px;font-size:14px;color:var(--verde)}
.ab .dados b{display:block;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--vermelho);margin-bottom:2px}
.ab .dados span{color:var(--escuro)}
.ab .ir{align-self:flex-start;margin-top:4px;display:inline-flex;align-items:center;gap:8px;background:var(--vermelho);color:#fff;font-weight:600;font-size:15px;border-radius:999px;padding:11px 18px}
.ab:hover .ir{background:#B91F1F}
.ab.compacto{grid-template-columns:96px 1fr}
.ab.compacto .cap{min-height:96px}
.ab.compacto .tx{padding:14px 16px;gap:6px}
.ab.compacto .selo{font-size:10.5px;padding:4px 9px}
.ab.compacto h3{font-size:18px}.ab.compacto h3 span{display:none}
.ab.compacto .linha{font-size:13.5px;color:var(--verde)}
.ab.medio .cap{min-height:170px}
.ab.medio h3{font-size:clamp(20px,2.2vw,26px)}
.ab .capas-c{display:grid;grid-template-columns:repeat(5,1fr)}.ab .capas-c span{background-size:cover;background-position:center}.ab .capas-c span:first-child{background-position:center bottom}
.abertos .resto{display:grid;gap:12px;align-content:start}
@media(min-width:700px){.abertos.n2{grid-template-columns:1fr 1fr}}
@media(min-width:900px){.abertos.n1 .ab{grid-template-columns:5fr 7fr}.abertos.n1 .cap{min-height:100%}
 .abertos.n3{grid-template-columns:1.35fr 1fr;align-items:stretch}.abertos.n3 .resto{grid-auto-rows:1fr;align-content:stretch}
 .abertos.n3 .ab.compacto{grid-template-columns:1fr;grid-template-rows:1fr auto}.abertos.n3 .ab.compacto .cap{min-height:140px}.abertos.n3 .ab.compacto .tx{padding:16px 20px}}
"""

JS = r"""<script>
(function(){var hoje=new Date();hoje.setHours(0,0,0,0);var b=document.querySelector('.abertos');if(!b)return;
b.querySelectorAll('[data-fim]').forEach(function(a){var p=a.dataset.fim.split('-');if(new Date(+p[0],p[1]-1,+p[2])<=hoje)a.remove()});
var r=b.querySelector('.resto');if(r&&!r.children.length)r.remove();
var n=b.querySelectorAll('[data-fim]').length;if(!n){var s=b.closest('section');if(s)s.remove();document.querySelectorAll('.mbtn.aberto-agora,a[href="#aberto"],a[href="/#aberto"]').forEach(function(x){x.remove()});return}
if(n<3&&b.classList.contains('n3')){var c=b.querySelectorAll('.ab');b.className='abertos n'+n;c.forEach(function(x){x.classList.remove('grande','compacto');x.classList.add(n==1?'grande':'medio');b.appendChild(x)})}
else if(n==1&&b.classList.contains('n2')){b.className='abertos n1';b.querySelector('.ab').classList.replace('medio','grande')}})();
</script>"""


# Campanhas que entram no bloco como mais um cartão (com as datas em que somem sozinhas).
CAMPANHAS = [dict(
    href='/final-de-ano/', fim='2026-12-12', ordem='2026-12-11', selo='até 11/12', nome='Final de ano no Fendas', sub='',
    ds='As gravações de sete eventos realizados em 2026, reunidas em cinco combos: relações raciais, gênero, sexualidade, interseccionalidade e política.',
    dados=[('Formato', 'aulas gravadas + materiais', 'aulas gravadas + materiais'), ('Desconto', '25%', '25%'), ('Acesso', 'até 31/01/2027', 'até 31/01/2027')],
    linha='5 combos · 25% de desconto', botao='Conhecer os combos',
    cap='<span class="cap capas-c" aria-hidden="true">' + ''.join(
        f'<span style="background-image:url({{{{thumbs/{t}.webp}}}})"></span>' for t in ('raciais', 'genero', 'sexualidade', 'intersec', 'raciais-genero')) + '</span>',
)]


def _evento(slug):
    """Dados do cartão de um evento aberto. Antes de começar: selo 'Início dd/mm', some no primeiro encontro.
    Vendendo depois de começar (inscricao['ate']): selo 'até dd/mm', valor do lote vigente, some no dia seguinte ao fim das inscrições."""
    import curso
    c = CURSOS[slug]; i = c['inscricao']; n = len(c['modulos'])
    ano = (dict(c['fatos']).get('Datas') or dict(c['fatos']).get('Data'))[-4:]
    ini = c['modulos'][0][0]; iso_ini = f"{ano}-{ini[3:5]}-{ini[:2]}"
    cert = f"{c['horas'][0]}h"
    if i.get('ate'):
        ate = i['ate']; v = i['lotes'][-1][0]
        return dict(href=f'/eventos/{slug}/', fim=curso.fim_insc(c), ordem=f"{ate[6:]}-{ate[3:5]}-{ate[:2]}", selo=f'até {ate[:5]}',
                    nome=c['nome'], sub=c['sub'], ds=c['chamada'], botao='Ver o evento',
                    dados=[('Formato', f"{c['formato']} · {n} {'encontro gravado' if n == 1 else 'encontros gravados'}, online", c['formato']),
                           ('Valor', v, v), ('Certificação', cert, cert)],
                    linha=f"{c['formato']} · {v}", cap=_cap(c))
    v, _ = i['lotes'][0]; valor = f'{v} até {ini}'
    return dict(href=f'/eventos/{slug}/', fim=iso_ini, ordem=iso_ini, selo=f'Início {ini}', nome=c['nome'], sub=c['sub'], ds=c['chamada'],
                botao='Ver o evento', dados=[('Formato', f"{c['formato']} · {n} {'encontro' if n == 1 else 'encontros'} ao vivo, online", c['formato']),
                                             ('Valor', valor, valor), ('Certificação', cert, cert)],
                linha=f"{c['formato']} · {valor}", cap=_cap(c))


def _cap(c):
    return f'<span class="cap"><img src="{{{{{c["img"]}}}}}" alt="" loading="lazy" width="480" height="480"></span>'


def cartao(it, tipo):
    e = H.escape
    if tipo == 'compacto':
        return (f'<a class="ab compacto" href="{it["href"]}" data-fim="{it["fim"]}">{it["cap"]}<span class="tx"><span class="selo">{it["selo"]}</span>'
                f'<h3>{e(it["nome"])}</h3><span class="linha">{e(it["linha"])}</span></span></a>')
    sub = f'<span>{e(it["sub"])}</span>' if it['sub'] else ''
    dados = ''.join(f'<span><b>{r}</b>{e(g if tipo == "grande" else m)}</span>' for r, g, m in it['dados'])
    return (f'<a class="ab {tipo}" href="{it["href"]}" data-fim="{it["fim"]}">{it["cap"]}<span class="tx"><span class="selo">{it["selo"]}</span>'
            f'<h3>{e(it["nome"])}{sub}</h3><span class="ds">{e(it["ds"])}</span>'
            f'<span class="dados">{dados}</span>'
            f'<span class="ir">{it["botao"]} <span aria-hidden="true">→</span></span></span></a>')


def itens(slugs):
    """Eventos abertos + campanhas ainda vigentes, pela data mais próxima (início ou fim das inscrições)."""
    import datetime as dt
    hoje = dt.date.today().isoformat()
    todos = [_evento(x) for x in slugs] + [c for c in CAMPANHAS if c['fim'] > hoje]
    return sorted([x for x in todos if x['fim'] > hoje], key=lambda x: x['ordem'])


def bloco(slugs):
    s = itens(slugs)
    if len(s) == 1:
        return f'<div class="abertos n1">{cartao(s[0], "grande")}</div>'
    if len(s) == 2:
        return f'<div class="abertos n2">{cartao(s[0], "medio")}{cartao(s[1], "medio")}</div>'
    return f'<div class="abertos n3">{cartao(s[0], "grande")}<div class="resto">{"".join(cartao(x, "compacto") for x in s[1:])}</div></div>'


def abertos():
    return [s for s, c in CURSOS.items() if c.get('status') == 'aberto']
