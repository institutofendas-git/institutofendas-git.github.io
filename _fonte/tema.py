"""Páginas por tema: python3 tema.py -> tema-<slug>-src.html
Não entram no menu. Existem para quem chega pelo Google, por anúncio ou por link direto.
Os textos saem dos PPPs dos eventos de cada tema; revisar com a equipe antes de publicar."""
import json, re
from curso import CSS, ICON_UP, ICON_DOWN, CURSOS, esc, card, CARDS_CSS, ORDEM
from dados import FORMATOS
from menu import og
import zap

TEMAS = [
 dict(slug='interseccionalidade-na-saude', perguntas=[('Por que somar opressões não basta para entender quem chega ao serviço?', 'conversas-interseccionais'), ('Como gênero, raça, classe e território viram determinantes do processo saúde-doença?', 'fendas-no-cuidado'), ('Quando a violência institucional produz mortes evitáveis?', 'fendas-no-cuidado'), ('Como a lente interseccional muda o atendimento na atenção primária, no hospital e na clínica?', 'conversas-interseccionais')], nome='Interseccionalidade na saúde', marca=('intersec', -8),
  busca='Cursos online sobre interseccionalidade na saúde',
  chamada='Como gênero, raça, sexualidade, classe, território, espiritualidade e capacidade se cruzam no processo saúde-doença-cuidado.',
  texto=['A interseccionalidade nasce das lutas do feminismo negro e chega à saúde como ferramenta de investigação: em vez de somar opressões, ela pergunta como os marcadores sociais se articulam na vida de quem adoece e de quem cuida.',
         'Nos eventos deste tema, o conceito, sua história e seus usos são levados para a atenção primária, o hospital e a clínica particular, com atenção às violências institucionais e às práticas que reconhecem a complexidade de cada pessoa.'],
  topicos=['O conceito, sua história e seus usos', 'Marcadores sociais como determinantes da saúde', 'Violência institucional e mortes evitáveis', 'A lente interseccional na clínica, no hospital e na atenção primária'],
  eventos=['conversas-interseccionais', 'fendas-no-cuidado', 'cuidado-nas-encruzilhadas']),
 dict(slug='relacoes-raciais-e-saude', perguntas=[('O que a branquitude ganha ao se ver sem raça?', 'pacto-da-branquitude'), ('Por que a dor das mulheres negras é tantas vezes desacreditada?', 'cuidado-nas-encruzilhadas'), ('Como o racismo institucional aparece no SUS?', 'cuidado-nas-encruzilhadas'), ('Que alianças silenciosas mantêm as instituições como estão?', 'pacto-da-branquitude')], nome='Relações raciais e saúde', marca=('olho', -6),
  busca='Cursos online sobre relações raciais e saúde',
  chamada='Racismo institucional, branquitude e o cuidado à população negra nos serviços de saúde.',
  texto=['O racismo atravessa o acesso, o diagnóstico e a escuta. Nos serviços de saúde ele aparece nas barreiras de atendimento, nos mitos sobre a dor e nos estereótipos que moldam o sofrimento psíquico.',
         'Os eventos deste tema olham para os dois lados dessa relação: a saúde das mulheres negras, a partir do feminismo negro e da saúde coletiva, e a branquitude como lugar de poder que costuma se ver sem raça.'],
  topicos=['Racismo institucional e epistêmico no SUS', 'Saúde das mulheres negras', 'Branquitude, pacto narcísico e capitalismo racial', 'Práticas de cuidado descolonizadoras'],
  eventos=['pacto-da-branquitude', 'cuidado-nas-encruzilhadas']),
 dict(slug='genero-e-saude', perguntas=[('Como escutar uma mulher em situação de violência sem revitimizá-la?', 'corpos-vulnerados'), ('Por que tantos homens se afastam do autocuidado e da prevenção?', 'red-pill'), ('O que acontece quando a clínica pesa antes de escutar?', 'canetas-emagrecedoras'), ('O que a notificação compulsória pede de quem atende?', 'corpos-vulnerados')], nome='Gênero e saúde', marca=('feixe_luz', -12),
  busca='Cursos online sobre gênero e saúde',
  chamada='Violência contra a mulher, masculinidades e as normas de gênero que atravessam o adoecimento e o cuidado.',
  texto=['As normas de gênero moldam quem adoece, de quê, e quem procura ou evita o cuidado. Elas aparecem na violência contra a mulher, no ideal de virilidade que afasta homens da prevenção e nas pressões estéticas sobre os corpos.',
         'Os eventos deste tema vão do manejo da violência no serviço de saúde, com notificação, rede intersetorial e escuta não revitimizadora, ao estudo das masculinidades e da gordofobia na clínica.'],
  topicos=['Violência contra a mulher e escuta não revitimizadora', 'Patriarcado, masculinidades e ressentimento', 'Corpo, autoimagem e gordofobia', 'Saúde das mulheres negras'],
  eventos=['corpos-vulnerados', 'red-pill', 'canetas-emagrecedoras', 'cuidado-nas-encruzilhadas']),
 dict(slug='sexualidade-e-diversidade', perguntas=[('Sair do armário é aceitar-se?', 'do-armario-a-liberdade'), ('O que o estresse de minorias explica que a ACT sozinha não alcança?', 'do-armario-a-liberdade'), ('Como reconhecer um relacionamento abusivo entre pessoas LGBTQIAPN+?', 'corpos-vinculos-e-violencias'), ('Por que é tão difícil denunciar e romper esses ciclos?', 'corpos-vinculos-e-violencias')], nome='Sexualidade e diversidade', marca=('camadas', -10),
  busca='Cursos online sobre sexualidade e diversidade LGBTQIAPN+ na saúde',
  chamada='Estresse de minorias, homofobia internalizada e os vínculos e violências nas relações LGBTQIAPN+.',
  texto=['A LGBTfobia estrutural não fica do lado de fora do consultório. Ela participa da construção do self, dos vínculos amorosos e das violências que muitas vezes não são reconhecidas pelos modelos cis-heteronormativos.',
         'Os eventos deste tema oferecem subsídios para uma prática afirmativa: da Terapia de Aceitação e Compromisso articulada ao modelo de estresse de minorias às dinâmicas de relações amorosas e abusivas entre pessoas LGBTQIAPN+.'],
  topicos=['Modelo de estresse de minorias e ACT', 'Homofobia internalizada e terapia afirmativa', 'Relações amorosas e abusivas LGBTQIAPN+', 'Acolhimento sem revitimização'],
  eventos=['do-armario-a-liberdade', 'corpos-vinculos-e-violencias']),
 dict(slug='sofrimento-e-sociedade', perguntas=[('Quando o cansaço deixa de ser um problema individual?', 'gestao-do-sofrimento'), ('O que acontece com a subjetividade quando a atenção vira mercadoria?', 'gestao-do-sofrimento'), ('Como a busca pelo padrão de corpo vira sofrimento?', 'canetas-emagrecedoras'), ('O que empurra alguém para a radicalização nas redes?', 'red-pill')], nome='Sofrimento e sociedade', marca=('explosaao', 10),
  busca='Cursos online sobre saúde mental, sofrimento e sociedade',
  chamada='Como conflitos sociais viram queixas individuais, e o que isso pede de uma escuta clínica atenta ao contexto.',
  texto=['Cansaço, desempenho, medicalização, pressões estéticas, radicalização nas redes: boa parte do sofrimento que chega aos serviços de saúde tem origem social, mas costuma ser tratada como falha individual.',
         'Os eventos deste tema discutem a sociedade do cansaço, o tecnofeudalismo, a cultura do autocuidado, a medicalização dos corpos e o ressentimento masculino, com subsídios para práticas despatologizadoras.'],
  topicos=['Neoliberalismo e gestão do sofrimento', 'Medicalização e despatologização', 'Plataformas digitais e subjetividade', 'Sofrimento ético-político'],
  eventos=['gestao-do-sofrimento', 'canetas-emagrecedoras', 'red-pill']),
]

CSS_T = r"""
/* ---------- página de tema: editorial ---------- */
body{background:var(--creme)}
.trilha{background:var(--vinho)}
.abre{position:relative;overflow:hidden;background:var(--creme);padding:clamp(34px,6vw,80px) 0 clamp(40px,7vw,96px)}
.abre .wrap{position:relative;display:grid;gap:36px}
.abre .marca-t{position:absolute;z-index:0;pointer-events:none;width:min(150vw,900px);right:-38vw;top:-8%;opacity:.13;transform:rotate(var(--giro,0deg))}
.abre .txt{position:relative;z-index:1;display:flex;flex-direction:column;gap:18px}
.selo-tema{align-self:flex-start;display:inline-flex;gap:10px;align-items:center;font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--vermelho)}
.selo-tema::before{content:"";width:28px;height:2px;background:var(--vermelho)}
.abre h1{font-size:clamp(44px,9vw,112px);line-height:.95;letter-spacing:-.02em;color:var(--vinho);text-wrap:balance}
.abre h1 em{font-style:normal;color:var(--vermelho)}
.abre .chamada{font-size:clamp(18px,2.1vw,23px);line-height:1.45;color:var(--texto);max-width:34ch}
.fenda-linha{display:block;width:min(100%,520px);height:28px;margin-top:4px}
.colagem{position:relative;z-index:1;height:clamp(250px,62vw,440px)}
.colagem a{position:absolute;width:var(--w,56%);aspect-ratio:1;border-radius:6px;overflow:hidden;box-shadow:0 30px 50px -28px rgba(39,20,22,.55);transform:rotate(var(--r));left:var(--x);top:var(--y);transition:transform .35s cubic-bezier(.2,.7,.2,1),z-index 0s}
.colagem a:hover{transform:rotate(0) scale(1.04);z-index:5}
.colagem img{width:100%;height:100%;object-fit:cover;display:block}
.colagem span{position:absolute;left:10px;bottom:10px;right:10px;font-size:12px;font-weight:600;color:#fff;text-shadow:0 1px 8px rgba(0,0,0,.6);line-height:1.25}
@media(min-width:900px){.abre .wrap{grid-template-columns:1.25fr 1fr;align-items:center;gap:56px}.abre .marca-t{right:-180px;top:-20%;width:900px}.colagem{height:470px}}

.pergs{background:var(--vinho);color:var(--creme);position:relative;overflow:hidden}
.pergs::before{content:"";position:absolute;inset:0;background:var(--rachadura-3) center/cover no-repeat;opacity:.35;pointer-events:none}
.pergs .wrap{position:relative}
.pergs .cab h2{color:#fff}.pergs .cab p{color:#E6DCC6}
.pergs ol{list-style:none;margin:0;padding:0;counter-reset:p}
.pergs li{counter-increment:p;border-top:1.5px solid rgba(249,242,222,.25)}
.pergs li:last-child{border-bottom:1.5px solid rgba(249,242,222,.25)}
.pergs a{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;padding:24px 0;color:inherit;text-decoration:none}
.pergs a::before{content:counter(p,decimal-leading-zero);grid-row:span 2;font-size:14px;font-weight:600;color:#FF8A80;padding-top:8px;letter-spacing:.06em}
.pergs q{quotes:none;font-size:clamp(22px,3.4vw,38px);line-height:1.18;font-weight:600;color:#fff;transition:color .2s}
.pergs small{font-size:13.5px;line-height:1.5;color:#E6DCC6;display:block}
.pergs small b{color:var(--creme);font-weight:600;border-bottom:1.5px solid #FF8A80;transition:border-color .2s}
.pergs a:hover q{color:#FFD9D3}.pergs a:hover small b{border-color:var(--creme)}
@media(min-width:900px){.pergs li:nth-child(even) a{padding-left:12%}.pergs a{padding:30px 0}}

.ensaio{display:grid;gap:26px}
.ensaio>div{display:flex;flex-direction:column;gap:16px}
.ensaio p{font-size:clamp(17px,1.6vw,19px);line-height:1.7;color:var(--texto);max-width:60ch}
.ensaio p:first-of-type::first-letter{float:left;font-size:4.4em;line-height:.82;font-weight:700;color:var(--vermelho);margin:6px 12px 0 0}
.ensaio h2{font-size:clamp(26px,3.4vw,40px);color:var(--vinho);line-height:1.1;max-width:18ch}
@media(min-width:900px){.ensaio{grid-template-columns:.8fr 1.2fr;gap:64px;align-items:start}.ensaio h2{position:sticky;top:96px}}

.linha-tempo{list-style:none;margin:0;padding:0;position:relative}
.linha-tempo::before{content:"";position:absolute;left:9px;top:8px;bottom:8px;width:2px;background:var(--linha)}
.linha-tempo>li{position:relative;padding-left:40px;margin-bottom:22px}
.linha-tempo>li::before{content:"";position:absolute;left:2px;top:6px;width:16px;height:16px;border-radius:50%;background:var(--creme);border:3px solid var(--vermelho)}
.linha-tempo .quando{display:block;font-size:12.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:var(--vermelho);margin-bottom:10px}
.linha-tempo a{display:grid;grid-template-columns:96px 1fr;background:var(--papel);border-radius:8px;overflow:hidden;color:inherit;text-decoration:none;box-shadow:0 18px 34px -30px rgba(39,20,22,.5);transition:transform .18s,box-shadow .18s}
.linha-tempo a:hover{transform:translateX(4px);box-shadow:0 26px 40px -26px rgba(39,20,22,.55)}
.linha-tempo img{width:100%;height:100%;object-fit:cover;display:block;min-height:110px}
.linha-tempo .inf{padding:14px 16px;display:flex;flex-direction:column;gap:5px}
.linha-tempo small{font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--verde)}
.linha-tempo h3{font-size:17px;line-height:1.25;color:var(--vinho);font-weight:400}.linha-tempo h3 b{font-weight:700}
.linha-tempo .ver{margin-top:4px;font-size:13.5px;font-weight:600;color:var(--vermelho)}
@media(min-width:700px){.linha-tempo a{grid-template-columns:150px 1fr}.linha-tempo h3{font-size:19px}}

.segue{background:var(--vermelho);color:#fff;position:relative;overflow:hidden}
.segue .wrap{position:relative;z-index:1;display:flex;flex-direction:column;gap:18px}
.segue h2{font-size:clamp(30px,5vw,58px);line-height:1;max-width:14ch}
.segue p{font-size:17px;color:#FFE9E4;max-width:46ch}
.segue .marca-s{position:absolute;right:-60px;bottom:-80px;width:clamp(240px,40vw,460px);opacity:.5;pointer-events:none}
.segue .outros{display:flex;flex-wrap:wrap;gap:10px}
.segue .outros a{display:inline-flex;align-items:center;padding:12px 18px;border-radius:999px;border:1.5px solid rgba(255,255,255,.7);color:#fff;text-decoration:none;font-weight:600;font-size:15px}
.segue .outros a:hover{background:#fff;color:var(--vermelho)}
.segue .outros a.ig{background:#fff;color:var(--vermelho);border-color:#fff}
"""

POS = [('8%', '0%', '-7deg', '58%'), ('42%', '12%', '6deg', '50%'), ('18%', '44%', '3deg', '48%'), ('50%', '48%', '-4deg', '44%')]


def gerar(t):
    from curso import periodo, quem
    evs = [s for s in ORDEM if s in t['eventos']]
    capas = ''.join(f'<a href="/eventos/{s}/" aria-label="{esc(CURSOS[s]["nome"])}" style="--x:{x};--y:{y};--r:{r};--w:{w}"><img src="{{{{{CURSOS[s]["img"]}}}}}" alt="" width="480" height="480"></a>'
                    for s, (x, y, r, w) in zip(evs, POS))
    pergs = ''.join(f'<li><a href="/eventos/{e}/"><q>{re.sub(r'(\w+-\w+)', r'<span style="white-space:nowrap">\1</span>', esc(q))}</q><small>discutido em <b>{esc(CURSOS[e]["formato"].lower())} {esc(CURSOS[e]["nome"])}</b> →</small></a></li>' for q, e in t['perguntas'])
    texto = ''.join(f'<p>{esc(p)}</p>' for p in t['texto'])
    def item(s):
        c = CURSOS[s]; sub = f': {esc(c["sub"])}' if c['sub'] and c['formato'] != 'Clube do livro' else ''
        return (f'<li><span class="quando">{periodo(c)}</span><a href="/eventos/{s}/"><img src="{{{{{c["img"]}}}}}" alt="" loading="lazy" width="480" height="480">'
                f'<span class="inf"><small>{esc(c["formato"].lower())} · {quem(c).lower().replace("com ", "com ", 1)}</small><h3><b>{esc(c["nome"])}</b>{sub}</h3><span class="ver">Ver como foi →</span></span></a></li>')
    linha = ''.join(item(s) for s in evs)
    formatos = ''.join(f'<a href="/formatos/{s}/">{esc(p)}</a>' for s, _, p, *_ in FORMATOS)
    nome = esc(t['nome']); partes = nome.split(' ', 1)
    h1 = f'{partes[0]} <em>{partes[1]}</em>' if len(partes) > 1 else nome
    ld = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": t['nome'], "description": t['chamada'],
                     "url": f"https://institutofendas.com.br/temas/{t['slug']}/",
                     "isPartOf": {"@type": "WebSite", "name": "Instituto Fendas", "url": "https://institutofendas.com.br/"},
                     "hasPart": [{"@type": "EducationEvent", "name": CURSOS[s]['nome'], "url": f"https://institutofendas.com.br/eventos/{s}/"} for s in evs]}, ensure_ascii=False)
    base = open('base.css').read()
    page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{nome}: cursos online com certificado | Instituto Fendas</title>
{og(t['nome'] + " | Instituto Fendas", t['chamada'] + " Cursos online, ao vivo e gravados, com certificado.", f"/temas/{t['slug']}/", t['nome'])}
<link rel="icon" href="{{{{of/avatar64.png}}}}">
<style>
{base}
{CSS}
{CSS_T}
</style>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<!--MENU:nenhum-->
<nav class="trilha" aria-label="Você está em"><div class="wrap"><a href="/">Início</a><span aria-hidden="true">›</span><b>{nome}</b></div></nav>

<main id="inicio">
<section class="abre">
  <img class="marca-t" src="{{{{of/ic-{t['marca'][0]}.svg}}}}" style="--giro:{t['marca'][1]}deg" alt="" aria-hidden="true">
  <div class="wrap">
    <div class="txt">
      <span class="selo-tema">Tema de estudo</span>
      <h1>{h1}</h1>
      <svg class="fenda-linha" viewBox="0 0 520 28" fill="none" aria-hidden="true"><path d="M0 14H210l14-11 10 22 12-18 8 7H520" stroke="#D62929" stroke-width="2.5" stroke-linejoin="round"/></svg>
      <p class="chamada">{esc(t['chamada'])}</p>
    </div>
    <div class="colagem" aria-label="Eventos sobre o tema">{capas}</div>
  </div>
</section>

<section class="sec pergs">
  <div class="wrap">
    <div class="cab"><h2>Perguntas que este tema faz</h2><p>E onde cada uma foi discutida no Instituto.</p></div>
    <ol>{pergs}</ol>
  </div>
</section>

<section class="sec">
  <div class="wrap ensaio">
    <h2>{esc(t['busca'])}</h2>
    <div>{texto}</div>
  </div>
</section>

<section class="sec" style="background:#F2EAD6">
  <div class="wrap">
    <div class="cab"><h2>O tema em 2026</h2><p>O que já aconteceu ao vivo, em ordem de data.</p></div>
    <ol class="linha-tempo">{linha}</ol>
  </div>
</section>

<section class="sec segue">
  <img class="marca-s" src="{{{{of/ic-{t['marca'][0]}.svg|#d62929=#B91F1F}}}}" alt="" aria-hidden="true">
  <div class="wrap">
    <h2>O tema continua.</h2>
    <p>As próximas turmas são anunciadas primeiro no Instagram. Enquanto isso, dá para conhecer os formatos em que o Instituto trabalha.</p>
    <div class="outros"><a class="ig" href="https://instagram.com/institutofendas">Seguir @institutofendas</a><a href="{zap.link()}">WhatsApp</a>{formatos}</div>
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
    open(f"tema-{t['slug']}-src.html", 'w').write(page)


if __name__ == '__main__':
    for t in TEMAS:
        gerar(t)
