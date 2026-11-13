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
.ab h3 span{display:block;font-weight:500;font-size:max(15px,.66em);line-height:1.25;margin-top:6px;color:var(--vinho);opacity:.82}
.ab .ds{padding-top:12px;position:relative}.ab .ds::before{content:"";position:absolute;top:0;left:0;width:34px;height:3px;border-radius:2px;background:var(--vermelho)}
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
.ab[hidden]{display:none!important}
.ab .capas-c{display:grid;grid-template-columns:repeat(5,1fr)}.ab .capas-c span{background-size:cover;background-position:center}.ab .capas-c span:first-child{background-position:center bottom}
.abertos .resto{display:grid;gap:12px;align-content:start}
@media(min-width:700px){.abertos.n2{grid-template-columns:1fr 1fr}}
@media(min-width:900px){.abertos.n1 .ab{grid-template-columns:5fr 7fr}.abertos.n1 .cap{min-height:100%}
 .abertos.n3{grid-template-columns:1.35fr 1fr;align-items:stretch}.abertos.n3 .resto{grid-auto-rows:1fr;align-content:stretch}
 .abertos.n3 .ab.compacto{grid-template-columns:1fr;grid-template-rows:1fr auto}.abertos.n3 .ab.compacto .cap{min-height:140px}.abertos.n3 .ab.compacto .tx{padding:16px 20px}}
"""

JS = r"""<script>
(function(){var hoje=new Date();hoje.setHours(0,0,0,0);var b=document.querySelector('.abertos');if(!b)return;
function d(s){var p=s.split('-');return new Date(+p[0],p[1]-1,+p[2])}
b.querySelectorAll('[data-fim]').forEach(function(a){if(d(a.dataset.fim)<=hoje){a.remove();return}if(!a.dataset.de||d(a.dataset.de)<=hoje)a.hidden=false});
var r=b.querySelector('.resto');if(r&&!r.querySelector('.ab:not([hidden])'))r.remove();
var n=b.querySelectorAll('.ab:not([hidden])').length;if(!n){var s=b.closest('section');if(s)s.remove();document.querySelectorAll('.mbtn.aberto-agora,a[href="#aberto"],a[href="/#aberto"]').forEach(function(x){x.remove()});return}
if(n<3&&b.classList.contains('n3')){var c=b.querySelectorAll('.ab');b.className='abertos n'+n;c.forEach(function(x){x.classList.remove('grande','compacto');x.classList.add(n==1?'grande':'medio');b.appendChild(x)})}
else if(n==1&&b.classList.contains('n2')){b.className='abertos n1';b.querySelectorAll('.ab').forEach(function(x){x.classList.replace('medio','grande')})}})();
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
    """As versões do cartão de um evento aberto, cada uma com a sua janela de datas (troca sozinha no navegador):
    1) antes do primeiro encontro: selo 'Início dd/mm', valor do 1º lote com a data da virada;
    2) do primeiro encontro até o fim das inscrições (regra: 7 dias depois do último encontro): selo 'até dd/mm', valor do lote vigente."""
    import curso, datetime as dt
    c = CURSOS[slug]; i = c['inscricao']; n = len(c['modulos'])
    ini = c['modulos'][0][0]; iso_ini = curso.primeiro_encontro(c).isoformat()
    cert = f"{c['horas'][0]}h"; fim = curso.fim_insc(c); ate = curso.fim_inscricoes(c)
    v1, _ = i['lotes'][0]; valor = f'{v1} até {ini}'; v = i['lotes'][-1][0]
    base = dict(href=f'/eventos/{slug}/', nome=c['nome'], sub=c['sub'], ds=c['chamada'], botao='Quero me inscrever', cap=_cap(c))
    antes = dict(base, de=None, fim=iso_ini, ordem=iso_ini, selo=f'Início {ini}',
                 dados=[('Formato', f"{c['formato']} · {n} {'encontro' if n == 1 else 'encontros'} ao vivo, online", c['formato']),
                        ('Valor', valor, valor), ('Certificação', cert, cert)], linha=f"{c['formato']} · {valor}")
    depois = dict(base, de=iso_ini, fim=fim, ordem=ate.isoformat(), selo=f"até {ate.strftime('%d/%m')}",
                  dados=[('Formato', f"{c['formato']} · {n} {'encontro' if n == 1 else 'encontros'}, online", c['formato']),
                         ('Valor', v, v), ('Certificação', cert, cert)], linha=f"{c['formato']} · {v}")
    hoje = dt.date.today().isoformat()
    return [x for x in (antes, depois) if x['fim'] > hoje]


def _cap(c):
    foco = f' style="object-position:{c["foco"]}"' if c.get('foco') else ''
    return f'<span class="cap"><img src="{{{{{c["img"]}}}}}" alt="" loading="lazy" width="480" height="480"{foco}></span>'


def cartao(it, tipo):
    import datetime as dt
    e = H.escape
    datas = (f' data-de="{it["de"]}"' if it.get('de') else '') + f' data-fim="{it["fim"]}"'
    if it.get('de') and it['de'] > dt.date.today().isoformat(): datas += ' hidden'
    if tipo == 'compacto':
        return (f'<a class="ab compacto" href="{it["href"]}"{datas}>{it["cap"]}<span class="tx"><span class="selo">{it["selo"]}</span>'
                f'<h3>{e(it["nome"])}</h3><span class="linha">{e(it["linha"])}</span></span></a>')
    sub = f':<span>{e(it["sub"])}</span>' if it['sub'] else ''
    dados = ''.join(f'<span><b>{r}</b>{e(g if tipo == "grande" else m)}</span>' for r, g, m in it['dados'])
    return (f'<a class="ab {tipo}" href="{it["href"]}"{datas}>{it["cap"]}<span class="tx"><span class="selo">{it["selo"]}</span>'
            f'<h3>{e(it["nome"])}{sub}</h3><span class="ds">{e(it["ds"])}</span>'
            f'<span class="dados">{dados}</span>'
            f'<span class="ir">{it["botao"]} <span aria-hidden="true">→</span></span></span></a>')


def itens(slugs):
    """Lugares no bloco: cada evento aberto (com as suas versões por data) e cada campanha vigente, pela data mais próxima."""
    import datetime as dt
    hoje = dt.date.today().isoformat()
    lugares = [v for v in (_evento(x) for x in slugs) if v] + [[c] for c in CAMPANHAS if c['fim'] > hoje]
    return sorted(lugares, key=lambda l: l[0]['ordem'])


def _lugar(l, tipo):
    return ''.join(cartao(x, tipo) for x in l)


def bloco(slugs):
    s = itens(slugs)
    if len(s) == 1:
        return f'<div class="abertos n1">{_lugar(s[0], "grande")}</div>'
    if len(s) == 2:
        return f'<div class="abertos n2">{_lugar(s[0], "medio")}{_lugar(s[1], "medio")}</div>'
    return f'<div class="abertos n3">{_lugar(s[0], "grande")}<div class="resto">{"".join(_lugar(x, "compacto") for x in s[1:])}</div></div>'


def abertos():
    return [s for s, c in CURSOS.items() if c.get('status') == 'aberto']
