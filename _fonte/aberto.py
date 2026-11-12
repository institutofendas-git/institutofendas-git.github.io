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
.abertos .resto{display:grid;gap:12px;align-content:start}
@media(min-width:700px){.abertos.n2{grid-template-columns:1fr 1fr}}
@media(min-width:900px){.abertos.n1 .ab{grid-template-columns:5fr 7fr}.abertos.n1 .cap{min-height:100%}
 .abertos.n3{grid-template-columns:1.35fr 1fr;align-items:stretch}.abertos.n3 .resto{grid-auto-rows:1fr;align-content:stretch}
 .abertos.n3 .ab.compacto{grid-template-columns:1fr;grid-template-rows:1fr auto}.abertos.n3 .ab.compacto .cap{min-height:140px}.abertos.n3 .ab.compacto .tx{padding:16px 20px}}
"""

JS = r"""<script>
(function(){var hoje=new Date();hoje.setHours(0,0,0,0);var b=document.querySelector('.abertos');if(!b)return;
b.querySelectorAll('[data-ini]').forEach(function(a){var p=a.dataset.ini.split('-');if(new Date(+p[0],p[1]-1,+p[2])<=hoje)a.remove()});
var n=b.querySelectorAll('[data-ini]').length;if(!n){var s=b.closest('section');if(s)s.remove();document.querySelectorAll('.mbtn.aberto-agora').forEach(function(x){x.remove()})}})();
</script>"""


def _info(slug):
    c = CURSOS[slug]
    ini = c['modulos'][0][0]
    ano = (dict(c['fatos']).get('Datas') or dict(c['fatos']).get('Data'))[-4:]
    v, _ = c['inscricao']['lotes'][0]
    n = len(c['modulos'])
    return dict(c=c, ini=ini, iso=f"{ano}-{ini[3:5]}-{ini[:2]}", valor=f'{v} até {ini}',
                fmt=f"{c['formato']} · {n} {'encontro' if n == 1 else 'encontros'} ao vivo, online", cert=f"{c['horas'][0]}h")


def cartao(slug, tipo):
    i = _info(slug); c = i['c']; e = H.escape
    sub = f'<span>{e(c["sub"])}</span>' if c['sub'] else ''
    img = f'<span class="cap"><img src="{{{{{c["img"]}}}}}" alt="" loading="lazy" width="480" height="480"></span>'
    if tipo == 'compacto':
        return (f'<a class="ab compacto" href="/eventos/{slug}/" data-ini="{i["iso"]}">{img}<span class="tx"><span class="selo">Início {i["ini"]}</span>'
                f'<h3>{e(c["nome"])}</h3><span class="linha">{e(c["formato"])} · {i["valor"]}</span></span></a>')
    fmt = e(c['formato']) if tipo == 'medio' else e(i['fmt'])
    return (f'<a class="ab {tipo}" href="/eventos/{slug}/" data-ini="{i["iso"]}">{img}<span class="tx"><span class="selo">Início {i["ini"]}</span>'
            f'<h3>{e(c["nome"])}{sub}</h3><span class="ds">{e(c["chamada"])}</span>'
            f'<span class="dados"><span><b>Formato</b>{fmt}</span><span><b>Valor</b>{i["valor"]}</span><span><b>Certificação</b>{i["cert"]}</span></span>'
            f'<span class="ir">Ver o evento <span aria-hidden="true">→</span></span></span></a>')


def bloco(slugs):
    s = sorted(slugs, key=lambda x: _info(x)['iso'])
    if len(s) == 1:
        return f'<div class="abertos n1">{cartao(s[0], "grande")}</div>'
    if len(s) == 2:
        return f'<div class="abertos n2">{cartao(s[0], "medio")}{cartao(s[1], "medio")}</div>'
    return f'<div class="abertos n3">{cartao(s[0], "grande")}<div class="resto">{"".join(cartao(x, "compacto") for x in s[1:])}</div></div>'


def abertos():
    return [s for s, c in CURSOS.items() if c.get('status') == 'aberto']
