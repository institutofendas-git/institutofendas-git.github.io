"""Gera a página de um curso do Instituto Fendas a partir de um dicionário de dados.
Uso: python3 curso.py <slug>  ->  curso-<slug>-src.html  (depois build.py)"""
import sys, html, re, json

BIOS = {
 'rodrigo': ('Rodrigo Bandeira', 'CRP 11/17651', 'Psicólogo (UFC). Mestrando em Saúde Coletiva (UECE). Residência em Cancerologia (ICC). Especialista em Sexologia e em Gênero e Sexualidade. Gestalt-terapeuta individual e de relacionamentos.'),
 'ilo': ('Francisco Ilo', 'CRP 11/17085', 'Psicólogo (UFC). Especialista em Terapia de Aceitação e Compromisso (FGE-SP). Psicoterapia individual e de relacionamentos, com formação em Terapia Sexual.'),
 'milena': ('Milena Raposo', 'CRP 11/19635', 'Psicóloga (UFC). Mestranda em Saúde Pública (UFC). Residência em Neonatologia (ESP-CE). Especialista em Psicologia Hospitalar. Terapeuta Comportamental Contextual.'),
 'gabriel': ('Gabriel da Silva', 'CRP 11/18611', 'Psicólogo (UFC). Especialista em Equidade na Gestão do Trabalho e da Educação no SUS (HAOC). Residência em Cancerologia (ESP-CE). Terapeuta Comportamental Contextual.'),
}

CURSOS = {
 'gestao-do-sofrimento': dict(
  formato='Grupo de estudos', formato_plural='Grupos de estudos', formato_slug='grupos-de-estudos',
  nome='A Gestão do Sofrimento', sub='neoliberalismo, cultura e despatologização',
  img='fotos/c-gestao.webp',
  chamada='Como conflitos sociais acabam convertidos em déficits individuais e queixas medicalizáveis, e como sustentar uma escuta que articule clínica e crítica social.',
  chamada_longa='Quatro encontros para ler o sofrimento psíquico de hoje a partir da sociedade do cansaço, do tecnofeudalismo, da cultura do autocuidado e da crítica psiquiátrica.',
  status='encerrado', encerrado_em='06/10/2026',
  combos=['intersec'],
  fatos=[('Datas','15, 22 e 29/09 e 06/10/2026'),('Horário','terças, 19h30 às 21h'),('Encontros','4 ao vivo, de 1h30'),('Carga','15h/a: 6h ao vivo + 9h de estudo'),('Onde','online, pelo Google Meet')],
  sobre=['O grupo de estudos propõe uma análise crítica e situada dos atravessamentos culturais, econômicos e tecnológicos que moldam o sofrimento psíquico hoje. A partir do diálogo entre obras sobre a sociedade do cansaço, o tecnofeudalismo e a crítica psiquiátrica, investiga a autoexploração pelo desempenho, os impactos subjetivos do capital-nuvem, a mercantilização do autocuidado e os limites dos enquadres diagnósticos.',
         'É um espaço de debate sobre como conflitos sociopolíticos são convertidos em déficits individuais e queixas medicalizáveis, com subsídios para escutas clínicas contextualizadas e práticas de cuidado despatologizadoras.'],
  aviso='É um grupo de estudos: a discussão parte de leituras, não é uma aula expositiva.',
  publico='Estudantes e profissionais das áreas da saúde e das ciências humanas.',
  objetivo='Compreender o neoliberalismo como modo de gestão e produção do sofrimento psíquico, fomentando práticas de cuidado pautadas na repolitização do mal-estar e na despatologização da existência.',
  especificos=['Compreender a racionalidade neoliberal como economia moral e como os imperativos de desempenho e a "empresa de si" reconfiguram os afetos e o sofrimento.',
               'Analisar as matrizes psicológicas do discurso mercantil e os limites da liberdade negativa, reconhecendo a coerção internalizada e o esvaziamento da alteridade.',
               'Examinar as mutações da psiquiatria contemporânea, do desmonte das categorias clínicas tradicionais às tecnologias de aprimoramento de si e à hipótese depressiva.',
               'Desenvolver subsídios ético-políticos para intervenções despatologizadoras, fortalecendo a escuta da singularidade e a articulação entre clínica e crítica social.'],
  modulos=[('15/09','A sociedade do cansaço: desempenho e autoexploração',['Do paradigma disciplinar ao imperativo da positividade e da autoeficácia','O sujeito como senhor e escravo de si na busca por produtividade','Esgotamento, depressão e burnout como colapsos da exigência de rendimento','A erosão da pausa e novas formas de recusa e descanso coletivo']),
           ('22/09','Tecnofeudalismo: capital-nuvem e subjetividade algorítmica',['O capital-nuvem como dispositivo de modificação de comportamento e extração de dados','O trabalho gratuito dos usuários e a vigilância algorítmica sobre o trabalho precarizado','Feudos digitais: a renda no lugar do lucro','A captura da atenção, a fabricação do desejo e a erosão da autonomia']),
           ('29/09','Cultura do autocuidado e individualização do sofrimento',['A indústria do wellness e a saúde como mercadoria','O cuidado convertido em dever ético individual e gestão de si','Vulnerabilidades estruturais lidas como falhas de disciplina pessoal','Do consumo à coletividade: redes solidárias de apoio']),
           ('06/10','Despatologização: psiquiatria e sofrimento',['A crítica à hipermedicalização e à redução da vida a enquadres psiquiátricos','O sofrimento ético-político como reação legítima às violências do meio social','A vida além do rótulo: a narrativa singular do sujeito','Parâmetros éticos e clínicos para acolher a dor sem estigmatizá-la'])],
  modulo_label='Encontro',
  metodologia=['Discussões teóricas e em grupo','Leitura de material complementar','Avaliação de feedback'],
  prazos=[('15/09','início e materiais'),('06/10','último encontro e formulário'),('06/11','fim do acesso e do certificado')],
  horas=(15,6),
  facilitadores=['rodrigo','milena','gabriel','ilo'],
 ),
}

from menu import og
from dados import BIOS_EXTRA, NOVOS, COMBOS, FORMATOS, FUNDADORES
BIOS.update(BIOS_EXTRA)
CURSOS.update(NOVOS)
import os

MARCAS = {'conversas-interseccionais':('intersec',-6),'fendas-no-cuidado':('fenda',0),'red-pill':('explosaao',12),'canetas-emagrecedoras':('olho',-10),
 'gestao-do-sofrimento':('camadas',0),'cuidado-nas-encruzilhadas':('caminhos',-28),'corpos-vulnerados':('feixe_luz',-14),'do-armario-a-liberdade':('feixe_luz',18),
 'corpos-vinculos-e-violencias':('intersec',14),'pacto-da-branquitude':('olho',8)}

DEPOIMENTOS = [('Ana Beatriz Lima','psicóloga · Grupo de estudos A Gestão do Sofrimento'),('Carlos Eduardo Nunes','estudante de enfermagem · Curso Red Pill'),('Juliana Freitas','assistente social · Capacitação Corpos Vulnerados'),('Marcos Vinícius Rocha','psicólogo · Clube do livro O Pacto da Branquitude'),('Patrícia Moura','enfermeira · Minicurso Cuidado nas Encruzilhadas')]
LOREM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante venenatis dapibus, posuere velit aliquet. Donec ullamcorper nulla non metus auctor fringilla, vestibulum id ligula porta felis euismod semper.'

FAQ = [('Não consigo assistir ao vivo. Posso me inscrever?','Pode. Os encontros são gravados e ficam numa pasta do Google Drive por um período. Dá para assistir depois ou rever para continuar os estudos.'),
 ('É cobrada frequência?','Não. Como as aulas podem ser assistidas depois, não há controle de presença. O certificado depende do formulário de feedback, disponibilizado no encerramento.'),
 ('O acesso às gravações é para sempre?','Não. Todo evento do Instituto tem uma data de encerramento. Depois dela, as gravações e a emissão do certificado deixam de estar disponíveis.'),
 ('Os cursos são reconhecidos pelo MEC?','São cursos livres, modalidade amparada pela Lei nº 9.394/1996, pelo Decreto nº 5.154/2004 e pelos artigos 205 e 206 da Constituição, que não exige reconhecimento do MEC.')]

ICON_UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 15l6-6 6 6"/></svg>'
ICON_DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>'
ICON_LOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>'

ICONS = {
 'cal':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
 'clock':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>',
 'stack':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="m3 13 9 5 9-5"/></svg>',
 'award':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="5.5"/><path d="M8.5 13.5 7 21l5-2.5 5 2.5-1.5-7.5"/></svg>',
 'screen':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4.5" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 16.5V20"/></svg>',
 'users':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6.5 6.5 0 0 1 3.5 6"/></svg>',
 'play':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><rect x="3" y="4.5" width="18" height="15" rx="2"/><path d="m10 9 5 3-5 3V9Z"/></svg>',
 'book':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5v-15Z"/><path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H20v3H6.5"/></svg>',
}
ICON_FATOS = {'Data':'cal','Datas':'cal','Horário':'clock','Encontros':'stack','Carga':'award','Onde':'screen'}

CSS = r"""
/* ---------- página de curso ---------- */
body{font-size:16px}
.sec{padding:clamp(52px,8vw,96px) 0}
.cab{margin-bottom:clamp(22px,4vw,40px)}
.cab h2{font-size:clamp(28px,4.4vw,48px)}
.trilha{background:var(--vinho);color:var(--bege);border-top:1px solid rgba(249,242,222,.12)}
.trilha .wrap{padding-top:9px;padding-bottom:9px;display:flex;flex-wrap:wrap;align-items:baseline;column-gap:8px;row-gap:2px;font-size:12.5px;line-height:1.4}
.trilha a{color:var(--creme);text-decoration:none;opacity:.8}.trilha a:hover{opacity:1;text-decoration:underline}
.trilha span{opacity:.6}
.trilha b{font-weight:600;color:var(--creme)}
/* abertura */
.hero{color:var(--creme);background:var(--fresta);position:relative;overflow:hidden}
.hero>.wrap,.hero>.resumo{position:relative;z-index:1}
.hero .marca{position:absolute;z-index:0;pointer-events:none;right:-22vw;top:42%;width:min(115vw,620px);transform:translateY(-50%) rotate(var(--giro,0deg))}
@media(min-width:900px){.hero .marca{right:auto;left:46%;top:58%;width:620px}}
.hero>.wrap{padding-top:22px;padding-bottom:clamp(36px,6vw,72px);display:grid;gap:22px}
.hero-txt{display:flex;flex-direction:column;gap:14px}
.hero .eyebrow{color:var(--bege)}
.hero h1{font-size:clamp(34px,6vw,68px);color:#fff}
.hero h1 span{display:block;font-weight:400;font-size:.5em;line-height:1.25;margin-top:8px;color:#F2E4CB}
.hero .chamada{font-size:clamp(16px,1.7vw,19px);color:#F2E4CB;max-width:46ch}
.selo-status{align-self:flex-start;display:inline-flex;gap:8px;align-items:center;background:rgba(249,242,222,.14);border:1px solid rgba(249,242,222,.35);color:var(--creme);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;border-radius:999px;padding:7px 13px}
.selo-status svg{width:14px;height:14px}
.capa{aspect-ratio:4/3;border-radius:6px;position:relative;overflow:hidden;background:var(--vinho);box-shadow:0 26px 44px -30px rgba(0,0,0,.7)}
@media(min-width:900px){.hero>.wrap{grid-template-columns:1.2fr .8fr;align-items:center;column-gap:48px;padding-top:44px}.hero-txt{grid-column:1;grid-row:1}.capa{grid-column:2;grid-row:1;aspect-ratio:1;width:min(100%,440px);justify-self:end}}
.capa img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.selo-status.aberto{background:var(--creme);color:var(--vinho);border-color:var(--creme)}.selo-status.aberto::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--vermelho)}
.inscricao .preco{font-size:15px}.inscricao .preco b{display:inline;font-size:22px;color:var(--vinho)}
.demo{background:#FFF3C4;color:#5B4300;font-size:13.5px;font-weight:600;text-align:center;padding:9px 16px}
/* resumo */
.resumo{background:var(--escuro);color:var(--creme)}
.resumo ul{list-style:none;margin:0 auto;padding-top:22px;padding-bottom:22px;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.resumo li{display:flex;gap:10px;align-items:flex-start;background:rgba(249,242,222,.06);border-radius:6px;padding:12px}
.resumo li:last-child:nth-child(odd){grid-column:1/-1}
.resumo svg{width:22px;height:22px;flex:none;color:var(--vermelho);margin-top:1px}
.resumo span{display:block;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--bege)}
.resumo strong{display:block;font-size:14.5px;line-height:1.3;margin-top:3px}
@media(min-width:900px){.resumo ul{grid-template-columns:repeat(5,1fr);gap:14px;padding-top:26px;padding-bottom:26px}.resumo li:last-child:nth-child(odd){grid-column:auto}}
/* inscrição */
.inscricao{background:#F2EAD6}
.inscricao .wrap{padding-top:22px;padding-bottom:22px;display:flex;flex-direction:column;gap:14px}
.inscricao .st{display:flex;gap:12px;align-items:flex-start}
.inscricao .st svg{width:22px;height:22px;flex:none;color:var(--vinho);margin-top:2px}
.inscricao p{font-size:15px;color:var(--texto)}
.inscricao p b{display:block;color:var(--vinho);font-size:16px}
.botoes{display:flex;flex-wrap:wrap;gap:10px}
.botoes .btn{flex:1 1 220px;text-align:center;line-height:1.25;min-width:0}
.btn-fechado{background:#D9CDB5;color:#6B6555;cursor:not-allowed;gap:8px}
.btn-fechado svg{width:16px;height:16px;flex:none}
.btn-fechado:hover{transform:none}
@media(min-width:1100px){.inscricao .wrap{flex-direction:row;align-items:center;justify-content:space-between;gap:32px}.inscricao .st{max-width:46ch}.botoes{flex:none;flex-wrap:nowrap}.botoes .btn{flex:none;white-space:nowrap}}
/* encontros */
.trilho{background:var(--verde);color:var(--creme)}
.trilho .cab h2{color:#fff}.trilho .cab p{color:#E6DCC6}
.encontros{list-style:none;margin:0;padding:0;display:grid;gap:10px;counter-reset:e}
.encontro{background:rgba(249,242,222,.08);border:1px solid rgba(249,242,222,.22);border-radius:6px}
.encontro summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:44px 1fr 20px;gap:12px;align-items:center;padding:16px}
.encontro summary::-webkit-details-marker{display:none}
.encontro .num{width:44px;height:44px;border-radius:50%;background:var(--creme);color:var(--vinho);display:grid;place-items:center;font-weight:700;font-size:17px}
.encontro small{display:block;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--bege)}
.encontro h3{font-size:17px;line-height:1.28;color:#fff;margin-top:3px}
.encontro .mais{width:20px;height:20px;background:linear-gradient(var(--creme),var(--creme)) center/100% 2px no-repeat,linear-gradient(var(--creme),var(--creme)) center/2px 100% no-repeat;transition:transform .2s}
.encontro[open] .mais{transform:rotate(45deg)}
.encontro ul{margin:0;padding:0 18px 18px 72px;display:flex;flex-direction:column;gap:7px;font-size:14.5px;color:#EFE6D2}
@media(min-width:900px){.encontros{grid-template-columns:repeat(2,1fr);gap:14px}.encontro h3{font-size:19px}.encontro summary{padding:20px}.encontro ul{padding:0 22px 22px 78px}}
/* em resumo: para quem, como funciona, o que recebe */
.tres{display:grid;gap:12px}
.tile{background:var(--papel);border-radius:6px;padding:20px;display:flex;flex-direction:column;gap:10px;border-top:4px solid var(--vermelho)}
.tile svg{width:28px;height:28px;color:var(--vermelho)}
.tile h3{font-size:18px;color:var(--vinho)}
.tile p{font-size:15px;color:var(--texto)}
.tile ul{margin:0;padding-left:18px;font-size:14.5px;color:var(--texto);display:flex;flex-direction:column;gap:5px}
@media(min-width:860px){.tres{grid-template-columns:repeat(3,1fr);gap:16px}}
/* sobre e objetivos */
.sobre-c{display:grid;gap:22px}
.sobre-c .intro{font-size:clamp(17px,1.8vw,20px);line-height:1.5;color:var(--escuro);max-width:60ch}
.aviso{border-left:4px solid var(--vermelho);background:var(--papel);padding:12px 16px;border-radius:0 6px 6px 0;font-size:14.5px;color:var(--escuro)}
.dobra{border-top:1.5px solid var(--linha)}
.dobra:last-child{border-bottom:1.5px solid var(--linha)}
.dobra summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 0;font-size:17px;font-weight:600;color:var(--vinho)}
.dobra summary::-webkit-details-marker{display:none}
.dobra summary::after{content:"";flex:none;width:18px;height:18px;background:linear-gradient(var(--vermelho),var(--vermelho)) center/100% 2px no-repeat,linear-gradient(var(--vermelho),var(--vermelho)) center/2px 100% no-repeat;transition:transform .2s}
.dobra[open] summary::after{transform:rotate(45deg)}
.dobra .corpo{padding:0 0 20px;display:flex;flex-direction:column;gap:12px;font-size:15.5px;color:var(--texto);max-width:64ch}
.dobra ol{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:8px}
.dobra .geral{font-weight:600;color:var(--escuro)}
/* quem conduz */
.pessoas{display:grid;gap:12px}
.pessoa{display:grid;grid-template-columns:84px 1fr;gap:14px;background:var(--papel);border-radius:6px;overflow:hidden}
.pessoa .foto{position:relative;min-height:110px;background:var(--linha)}.pessoa .foto img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center top}
.pessoa .sem-foto{background:var(--bege);display:grid;place-items:center}.pessoa .sem-foto span{font-size:26px;font-weight:700;color:var(--vinho);opacity:.6}
.btn-vinho-linha{border:1.5px solid var(--vinho);color:var(--vinho);background:transparent}.fecho .btn-vinho-linha{border-color:var(--creme);color:var(--creme)}
.pessoa .txt{padding:14px 16px 14px 0;display:flex;flex-direction:column;gap:5px}
.pessoa h3{font-size:17px;color:var(--vinho)}
.pessoa p{font-size:13.5px;line-height:1.45;color:var(--texto)}
.pessoa small{font-size:11.5px;color:var(--verde)}
@media(min-width:800px){.pessoas{grid-template-columns:repeat(2,1fr);gap:16px}.pessoa{grid-template-columns:120px 1fr}.pessoa h3{font-size:19px}.pessoa p{font-size:14px}}
/* certificado e prazos */
.cert{display:grid;gap:22px}
.carga{background:var(--vinho);color:var(--creme);border-radius:6px;padding:22px;display:flex;flex-direction:column;gap:14px}
.carga .total{font-size:44px;font-weight:700;line-height:1;color:#fff}
.carga .total small{font-size:15px;font-weight:600;margin-left:6px;color:var(--bege)}
.barra-h{display:flex;height:12px;border-radius:999px;overflow:hidden;background:rgba(249,242,222,.2)}
.barra-h i{display:block;background:var(--vermelho)}
.legenda{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13.5px}
.legenda span::before{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;background:rgba(249,242,222,.45);vertical-align:-1px}
.legenda span:first-child::before{background:var(--vermelho)}
.passos{list-style:none;margin:0;padding:0;display:grid;gap:10px;counter-reset:p}
.passos li{counter-increment:p;display:grid;grid-template-columns:40px 1fr;gap:12px;align-items:center;background:var(--papel);border-radius:6px;padding:14px}
.passos li::before{content:counter(p);width:40px;height:40px;border-radius:50%;background:var(--vermelho);color:#fff;display:grid;place-items:center;font-weight:700}
.passos b{display:block;font-size:15px;color:var(--vinho)}
.passos span{font-size:13.5px;color:var(--texto)}
.prazos{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.prazos li{background:var(--papel);border-radius:6px;padding:12px;border-top:3px solid var(--vermelho)}
.prazos b{display:block;color:var(--vinho);font-size:14px}
.prazos span{display:block;font-size:12px;line-height:1.35;color:var(--texto);margin-top:4px}
.cert h3{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--verde);margin-bottom:10px}
@media(min-width:900px){.cert{grid-template-columns:.8fr 1.2fr;gap:28px;align-items:start}.passos{grid-template-columns:repeat(3,1fr)}.passos li{grid-template-columns:1fr;align-items:start}}
/* depoimentos */
.depo{background:#F2EAD6}
.depo .topo-dep{display:flex;justify-content:space-between;align-items:flex-end;gap:16px}
.exemplo{align-self:flex-start;display:inline-block;background:#FFF3C4;color:#5B4300;font-size:12px;font-weight:600;border-radius:999px;padding:5px 11px}
.setas-car{display:none;gap:8px}
.setas-car button{width:46px;height:46px;border-radius:50%;border:1.5px solid var(--vinho);background:transparent;color:var(--vinho);display:grid;place-items:center;cursor:pointer}
.setas-car button:hover{background:var(--vinho);color:var(--creme)}
.setas-car svg{width:20px;height:20px}
.depos{display:grid;grid-auto-flow:column;grid-auto-columns:86%;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-behavior:smooth;padding-bottom:6px;margin:0 calc(-1*var(--pad));padding-left:var(--pad);padding-right:var(--pad);scroll-padding:0 var(--pad);scrollbar-width:none}
.depos::-webkit-scrollbar{display:none}
.depos figure{scroll-snap-align:start;margin:0;background:var(--papel);border-radius:6px;padding:22px;display:flex;flex-direction:column;justify-content:space-between;gap:18px;border-top:4px solid var(--vermelho)}
.depos blockquote{margin:0;font-size:15px;line-height:1.6;color:var(--texto)}
.depos blockquote::before{content:"“";display:block;font-size:44px;line-height:.6;color:var(--vermelho);margin-bottom:6px}
.depos figcaption{display:flex;gap:12px;align-items:center}
.avatar{width:52px;height:52px;flex:none;border-radius:50%;background:var(--bege) center/cover no-repeat;display:grid;place-items:center;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--escuro)}
.depos figcaption b{display:block;color:var(--vinho);font-size:15px}
.depos figcaption span{display:block;font-size:12.5px;line-height:1.35;color:var(--verde);margin-top:2px}
.pontos{display:flex;justify-content:center;gap:8px;margin-top:16px}
.pontos i{width:8px;height:8px;border-radius:50%;background:var(--linha);transition:background .2s,width .2s}
.pontos i.on{background:var(--vermelho);width:22px;border-radius:999px}
@media(min-width:700px){.depos{grid-auto-columns:calc((100% - 2*var(--pad) - 14px)/2)}}
@media(min-width:1000px){.depos{grid-auto-columns:calc((100% - 2*var(--pad) - 28px)/3)}.setas-car{display:flex}}
@media(min-width:1180px){.depos{grid-auto-columns:calc((1180px - 2*var(--pad) - 28px)/3);margin:0 calc((1180px - 100vw)/2 - var(--pad));padding-left:calc((100vw - 1180px)/2 + var(--pad));padding-right:calc((100vw - 1180px)/2 + var(--pad));scroll-padding:0 calc((100vw - 1180px)/2 + var(--pad))}}
/* faq */
.faq details{border-top:1.5px solid var(--linha)}
.faq details:last-child{border-bottom:1.5px solid var(--linha)}
.faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px 0;font-size:16.5px;line-height:1.3;font-weight:600}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"";flex:none;width:18px;height:18px;background:linear-gradient(var(--vermelho),var(--vermelho)) center/100% 2px no-repeat,linear-gradient(var(--vermelho),var(--vermelho)) center/2px 100% no-repeat;transition:transform .2s}
.faq details[open] summary::after{transform:rotate(45deg)}
.faq details>div{padding:0 0 18px;font-size:15px;color:var(--texto);max-width:64ch}
/* fecho */
.fecho{background:var(--vermelho);color:#fff;position:relative;overflow:hidden}
.fecho .wrap{position:relative;z-index:1;display:flex;flex-direction:column;gap:18px;align-items:stretch}
.fecho h2{font-size:clamp(28px,4.4vw,48px);max-width:18ch}
.fecho p{font-size:16px;color:#FFE9E4;max-width:48ch}
.fecho .btn-fechado{background:rgba(255,255,255,.18);color:#fff}
.fecho .explosao{position:absolute;right:-70px;bottom:-90px;width:clamp(220px,36vw,420px);pointer-events:none}
@media(min-width:700px){.fecho .wrap{align-items:flex-start}}
footer span{line-height:1.6}
@media(max-width:899px){footer{padding-bottom:calc(96px + env(safe-area-inset-bottom))}}
/* barra fixa no celular */
.barra{position:fixed;left:0;right:0;bottom:0;z-index:30;padding:10px max(16px,env(safe-area-inset-left)) calc(10px + env(safe-area-inset-bottom));background:rgba(39,20,22,.96);display:flex;align-items:center;gap:12px;color:var(--creme);transform:translateY(110%);transition:transform .25s}
.barra.on{transform:none}
.barra small{font-size:12.5px;line-height:1.3;flex:1}
.barra small b{display:block;color:#fff;font-size:13.5px}
.barra .btn{padding:12px 16px;min-height:44px;font-size:14px;white-space:nowrap}
body.com-barra .setas{bottom:calc(86px + env(safe-area-inset-bottom))}
@media(min-width:900px){.barra{display:none}body.com-barra .setas{bottom:calc(16px + env(safe-area-inset-bottom))}}
"""

def esc(t): return html.escape(t, quote=False)

CARDS_CSS = r""".cards{list-style:none;margin:0;padding:0;display:grid;gap:14px}
.cards li{display:flex}.cards a{flex:1;display:grid;grid-template-columns:104px 1fr;background:var(--papel);border-radius:6px;overflow:hidden;text-decoration:none;color:inherit;box-shadow:0 18px 34px -30px rgba(39,20,22,.5);transition:transform .18s,box-shadow .18s}
.cards a:hover{transform:translateY(-4px);box-shadow:0 28px 40px -24px rgba(39,20,22,.55)}
.cards .simb{position:relative;min-height:130px;background:var(--linha)}.cards .simb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cards small b{color:var(--vermelho)}
.cards .info{padding:16px 18px;display:flex;flex-direction:column;gap:6px}
.cards small{font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--verde)}
.cards h3{font-size:18px;line-height:1.25;color:var(--vinho);font-weight:400}
.cards h3 b{font-weight:700}
.cards .com{font-size:13px;color:var(--verde)}
.cards .ver{margin-top:auto;align-self:flex-start;display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:600;color:var(--vermelho);border:1.5px solid var(--vermelho);border-radius:999px;padding:8px 14px;line-height:1;transition:background .18s,color .18s}
.cards a:hover .ver,.cards a:focus-visible .ver{background:var(--vermelho);color:#fff}
@media(min-width:700px){.cards a{grid-template-columns:170px 1fr}.cards .simb{min-height:170px}}
@media(min-width:1050px){.cards{grid-template-columns:repeat(2,1fr)}}
"""
ORDEM = ['conversas-interseccionais', 'red-pill', 'do-armario-a-liberdade', 'corpos-vinculos-e-violencias', 'pacto-da-branquitude',
         'corpos-vulnerados', 'canetas-emagrecedoras', 'gestao-do-sofrimento', 'cuidado-nas-encruzilhadas', 'fendas-no-cuidado']  # cronológica
MESES = {'01': 'jan', '02': 'fev', '03': 'mar', '04': 'abr', '05': 'mai', '06': 'jun', '07': 'jul', '08': 'ago', '09': 'set', '10': 'out', '11': 'nov', '12': 'dez'}
SETA = '<span aria-hidden="true">→</span>'

def periodo(c):
    datas = dict(c['fatos']).get('Datas') or dict(c['fatos']).get('Data')
    return f"{MESES[c['modulos'][0][0][3:5]]} de {datas[-4:]}"

def quem(c):
    f = c['facilitadores']
    if f == FUNDADORES: return 'Com os quatro fundadores'
    nomes = [BIOS[k][0] for k in f]
    return 'Com ' + (nomes[0] if len(nomes) == 1 else ', '.join(nomes[:-1]) + ' e ' + nomes[-1])

def situacao(c): return '<b>inscrições abertas</b>' if c.get('status') == 'aberto' else 'encerrado'

def card(slug, desc=False):
    c = CURSOS[slug]
    sub = f': {esc(c["sub"])}' if c['sub'] and c['formato'] != 'Clube do livro' else ''
    d = f'<p class="desc">{esc(c["chamada"])}</p>' if desc else ''
    return (f'<li data-formato="{c["formato_slug"]}"><a href="/eventos/{slug}/"><span class="simb"><img src="{{{{{c["img"]}}}}}" alt="" loading="lazy" decoding="async" width="480" height="480"></span>'
            f'<div class="info"><small>{esc(c["formato"].lower())} · {periodo(c)} · {situacao(c)}</small><h3><b>{esc(c["nome"])}</b>{sub}</h3>'
            f'<p class="com">{quem(c)}</p>{d}<span class="ver">{"Ver o evento" if c.get("status") == "aberto" else "Ver como foi"} {SETA}</span></div></a></li>')

def relacionados(slug, n=3):
    c = CURSOS[slug]; outros = [s for s in ORDEM if s != slug and s in CURSOS]
    def nota(s):
        o = CURSOS[s]
        return (-2 * len(set(o.get('combos', [])) & set(c.get('combos', []))) - (o['formato_slug'] == c['formato_slug']), abs(ORDEM.index(s) - ORDEM.index(slug)) if slug in ORDEM else 0)
    return sorted(outros, key=nota)[:n]

def jsonld(slug, c):
    import json
    datas = dict(c['fatos']).get('Datas') or dict(c['fatos']).get('Data')
    ano = datas[-4:]; dias = re.findall(r'(\d{2})/(\d{2})', datas); soltos = re.findall(r'\b(\d{2})(?=[ ,]| e)', datas)
    ini = c['modulos'][0][0]; fim = c['modulos'][-1][0]
    iso = lambda d: f"{ano}-{d[3:5]}-{d[0:2]}"
    d = {"@context": "https://schema.org", "@type": "EducationEvent", "name": f"{c['formato']} {c['nome']}" + (f": {c['sub']}" if c['sub'] else ''),
         "description": c['chamada'], "startDate": iso(ini), "endDate": iso(fim), "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
         "eventStatus": "https://schema.org/EventScheduled", "location": {"@type": "VirtualLocation", "url": f"https://institutofendas.com.br/eventos/{slug}/"},
         "image": f"https://institutofendas.com.br/eventos/{slug}/preview.jpg",
         "organizer": {"@type": "Organization", "name": "Instituto Fendas", "url": "https://institutofendas.com.br/"},
         "performer": [{"@type": "Person", "name": BIOS[k][0]} for k in c['facilitadores']]}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'


def gerar(slug):
    c = CURSOS[slug]
    nome, sub = c['nome'], c['sub']
    resumo = ''.join(f'<li>{ICONS[ICON_FATOS.get(k,"cal")]}<div><span>{k}</span><strong>{esc(v)}</strong></div></li>' for k, v in c['fatos'])
    combo_btn = combo_txt = combo_barra = ''
    cs = [COMBOS[k] for k in c.get('combos', [])]
    if len(cs) == 1:
        cn, cu = cs[0]
        combo_btn = f'<a class="btn btn-vermelho" href="{cu}">Gravação no combo {esc(cn)}</a>'
        combo_txt = f'A gravação desta turma está no combo {esc(cn)} do Final de ano no Fendas, até 11/12.'
        combo_barra = f'<a class="btn btn-vermelho" href="{cu}">Ver gravação</a>'
    elif cs:
        nomes = ', '.join(n for n, _ in cs[:-1]) + ' e ' + cs[-1][0]
        combo_btn = f'<a class="btn btn-vermelho" href="/final-de-ano/#combos">Ver os combos com a gravação</a>'
        combo_txt = f'A gravação desta turma está nos combos {esc(nomes)} do Final de ano no Fendas, até 11/12.'
        combo_barra = f'<a class="btn btn-vermelho" href="/final-de-ano/#combos">Ver gravação</a>'
    ig_btn = '<a class="btn btn-vinho-linha" href="https://instagram.com/institutofendas">Acompanhar no Instagram</a>'
    ig_txt = 'Esta turma não tem gravação à venda. Os próximos eventos são anunciados no Instagram do Instituto.'
    ig_barra = '<a class="btn btn-vermelho" href="https://instagram.com/institutofendas">Instagram</a>'
    ig_fecho = ' Acompanhe o Instituto para saber dos próximos eventos.'
    ig_small = 'turma de ' + c['encerrado_em'][-4:]
    def t(a, b): return f'<span class="so-campanha">{a}</span><span class="pos-campanha" hidden>{b}</span>' if cs else b
    def bt(a, b): return (a.replace('class="btn', 'class="so-campanha btn', 1) + b.replace('class="btn', 'hidden class="pos-campanha btn', 1)) if cs else b
    combo_txt = t(combo_txt, ig_txt)
    fecho_txt = t(' A gravação segue disponível no Final de ano no Fendas, até 11/12.', ig_fecho)
    barra_small = t('gravação no Final de ano', ig_small)
    combo_btn_fecho = bt(combo_btn.replace('btn-vermelho', 'btn-creme'), ig_btn)
    combo_btn = bt(combo_btn, ig_btn)
    combo_barra = bt(combo_barra, ig_barra)
    aberto = c.get('status') == 'aberto'
    fechado = f'<span class="btn btn-fechado" aria-disabled="true">{ICON_LOCK}Inscrições encerradas</span>'
    selo = f'<span class="selo-status">{ICON_LOCK}turma encerrada em {c["encerrado_em"]}</span>'
    insc = f'<div class="st">{ICON_LOCK}<p><b>Inscrições encerradas</b>{combo_txt.strip()}</p></div><div class="botoes">{fechado}{combo_btn}</div>'
    fecho = f'<h2>Esta turma já aconteceu.</h2><p>As inscrições estão encerradas.{fecho_txt}</p><div class="botoes">{fechado}{combo_btn_fecho}</div>'
    barra = f'<small><b>Inscrições encerradas</b>{barra_small}</small>' + combo_barra.replace(' href=', ' tabindex="-1" href=')
    demo = ''
    if aberto:
        i = c['inscricao']; (v1, q1) = i['lotes'][0]
        lotes = '<br>'.join(f'<b>{v}</b> {q}' for v, q in i['lotes'])
        selo = '<span class="selo-status aberto">inscrições abertas</span>'
        insc = f'<div class="st">{ICONS["cal"]}<p class="preco"><b style="display:block;font-size:16px">Inscrições abertas</b>{lotes}<br>{esc(i["pagamento"])}</p></div><div class="botoes"><a class="btn btn-vermelho" href="{i["url"]}">Inscrever-se</a></div>'
        fecho = f'<h2>Começa em {c["modulos"][0][0]}.</h2><p>{v1} {q1}. Encontros ao vivo, com gravação e certificado de {c["horas"][0]}h.</p><div class="botoes"><a class="btn btn-creme" href="{i["url"]}">Inscrever-se</a></div>'
        barra = f'<small><b>{v1}</b>{q1}</small><a class="btn btn-vermelho" tabindex="-1" href="{i["url"]}">Inscrever-se</a>'
        if c.get('demo'): demo = '<div class="demo">Demonstração: como fica a página de um evento com inscrições abertas. Datas, valores e link são de exemplo.</div>'
    rel = ''.join(card(s) for s in relacionados(slug))
    intro = esc(c['chamada_longa']) if c.get('chamada_longa') else esc(c['sobre'][0])
    resto = ''.join(f'<p>{esc(p)}</p>' for p in (c['sobre'] if c.get('chamada_longa') else c['sobre'][1:]))
    aviso = f'<p class="aviso">{esc(c["aviso"])}</p>' if c.get('aviso') else ''
    esp = ''.join(f'<li>{esc(e)}</li>' for e in c['especificos'])
    encontros = ''.join(f'<li><details class="encontro"><summary><span class="num">{i+1}</span><div><small>{c["modulo_label"] if len(c["modulos"])==1 else c["modulo_label"]+" "+str(i+1)} · {d}</small><h3>{esc(t)}</h3></div><span class="mais" aria-hidden="true"></span></summary><ul>{"".join(f"<li>{esc(x)}</li>" for x in its)}</ul></details></li>' for i, (d, t, its) in enumerate(c['modulos']))
    met = ''.join(f'<li>{esc(m)}</li>' for m in c['metodologia'])
    prazos = ''.join(f'<li><b>{d}</b><span>{esc(t)}</span></li>' for d, t in c['prazos'])
    def foto(k):
        if os.path.exists(f'fotos/p-{k}.webp'):
            return f'<div class="foto"><img src="{{{{fotos/p-{k}.webp}}}}" alt="{BIOS[k][0]}" loading="lazy" decoding="async" width="640" height="800"></div>'
        ini = ''.join(w[0] for w in BIOS[k][0].split() if w[0].isupper())[:2]
        return f'<div class="foto sem-foto" role="img" aria-label="Espaço para a foto de {BIOS[k][0]}"><span>{ini}</span></div>'
    pessoas = ''.join(f'<div class="pessoa">{foto(k)}<div class="txt"><h3>{BIOS[k][0]}</h3><p>{BIOS[k][2]}</p><small>{BIOS[k][1]}</small></div></div>' for k in c['facilitadores'])
    depos = ''.join(f'<figure><blockquote>{LOREM}</blockquote><figcaption><div class="avatar" role="img" aria-label="Espaço para a foto">foto</div><div><b>{n}</b><span>{q}</span></div></figcaption></figure>' for n, q in DEPOIMENTOS)
    faq = ''.join(f'<details><summary>{esc(q)}</summary><div><p>{esc(a)}</p></div></details>' for q, a in FAQ)
    faq += '<details><summary>Ainda tenho dúvida. Com quem falo?</summary><div><p>Com a equipe do Instituto, pelo Instagram <a href="https://instagram.com/institutofendas">@institutofendas</a> ou pelo e-mail <a href="mailto:institutofendas@gmail.com">institutofendas@gmail.com</a>.</p></div></details>'
    titulo = f'{nome}: {sub}' if sub else nome
    carga = dict(c['fatos']).get('Carga','')
    base = open('base.css').read()
    page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(nome)}: {esc(c["formato"].lower())} online com certificado | Instituto Fendas</title>
{og(titulo + " | Instituto Fendas", c["chamada"] + f" {c['formato']} online, ao vivo e gravado, com certificado de {c['horas'][0]}h.", f"/eventos/{slug}/", c["formato"] + " " + nome)}
<link rel="icon" href="{{{{of/avatar64.png}}}}">
<style>
@font-face{{font-family:'Syne';font-weight:400;font-display:swap;src:url({{{{syne-latin-400-normal.woff2}}}}) format('woff2')}}
@font-face{{font-family:'Syne';font-weight:600;font-display:swap;src:url({{{{syne-latin-600-normal.woff2}}}}) format('woff2')}}
@font-face{{font-family:'Syne';font-weight:700;font-display:swap;src:url({{{{syne-latin-700-normal.woff2}}}}) format('woff2')}}
{base}
{CSS}
{CARDS_CSS}
@media(min-width:1050px){{.cards.tres-col{{grid-template-columns:repeat(3,1fr)}}.cards.tres-col a{{grid-template-columns:1fr;grid-template-rows:auto 1fr}}.cards.tres-col .simb{{min-height:0;aspect-ratio:16/10}}}}
</style>
{jsonld(slug, c)}
</head>
<body>
<!--MENU:f:{c["formato_slug"]}-->
<nav class="trilha" aria-label="Você está em"><div class="wrap"><a href="/">Início</a><span aria-hidden="true">›</span><a href="/formatos/{c["formato_slug"]}/">{esc(c["formato_plural"])}</a><span aria-hidden="true">›</span><b>{esc(nome)}</b></div></nav>

<!--VER:{json.dumps(dict(nome=c["formato"]+" "+nome, categoria=c["formato"], valor=(float(c["inscricao"]["lotes"][0][0].replace("R$","").replace(".","").replace(",",".")) if aberto else None)), ensure_ascii=False)}-->
<main id="inicio">
{demo}<section class="hero">
  <img class="marca" src="{{{{of/ic-{MARCAS[slug][0]}.svg|#d62929=#A62340}}}}" style="--giro:{MARCAS[slug][1]}deg" alt="" aria-hidden="true">
  <div class="wrap">
    <div class="capa"><img src="{{{{{c["img"]}}}}}" alt="{esc(nome)}" width="480" height="480" fetchpriority="high"></div>
    <div class="hero-txt">
      <p class="eyebrow">{esc(c["formato"])} · Instituto Fendas</p>
      <h1>{esc(nome)}<span>{esc(sub)}</span></h1>
      <p class="chamada">{esc(c["chamada"])}</p>
      {selo}
    </div>
  </div>
  <div class="resumo"><ul class="wrap">{resumo}</ul></div>
</section>

<section class="inscricao" id="inscricao">
  <div class="wrap">
    {insc}
  </div>
</section>

<section class="sec trilho">
  <div class="wrap">
    <div class="cab"><h2>O que se estuda</h2><p>{"1 encontro. Toque para ver os temas." if len(c["modulos"])==1 else f"{len(c['modulos'])} encontros. Toque em cada um para ver os temas."}</p></div>
    <ol class="encontros">{encontros}</ol>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="tres">
      <article class="tile">{ICONS["users"]}<h3>Para quem é</h3><p>{esc(c["publico"])}</p></article>
      <article class="tile">{ICONS["screen"]}<h3>Como funciona</h3><ul>{"".join(f"<li>{x}</li>" for x in c.get("como", ["Encontros ao vivo pelo Google Meet","Gravação em até 2 dias úteis","Avisos pelo grupo de WhatsApp"]))}</ul></article>
      <article class="tile">{ICONS["book"]}<h3>Metodologia</h3><ul>{met}</ul></article>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap sobre-c">
    <div class="cab" style="margin-bottom:0"><h2>Sobre o evento</h2></div>
    <p class="intro">{intro}</p>
    {aviso}
    <div>
      <details class="dobra"><summary>Ler a apresentação completa</summary><div class="corpo">{resto}</div></details>
      <details class="dobra"><summary>Objetivos</summary><div class="corpo"><p class="geral">{esc(c["objetivo"])}</p><ol>{esp}</ol></div></details>
    </div>
  </div>
</section>

<section class="sec" style="background:#F2EAD6">
  <div class="wrap">
    <div class="cab"><h2>Quem conduz</h2></div>
    <div class="pessoas">{pessoas}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="cab"><h2>Certificado</h2></div>
    <div class="cert">
      <div class="carga"><div class="total">{c["horas"][0]}h<small>de certificado</small></div><div class="barra-h"><i style="width:{round(100*c["horas"][1]/c["horas"][0])}%"></i></div><div class="legenda"><span>{c["horas"][1]}h ao vivo</span><span>{c["horas"][0]-c["horas"][1]}h de estudo</span></div></div>
      <div>
        <h3>Como receber</h3>
        <ol class="passos"><li><div><b>Participe</b><span>ao vivo ou pela gravação</span></div></li><li><div><b>Preencha o formulário</b><span>entregue no último encontro</span></div></li><li><div><b>Receba por e-mail</b><span>em até 10 dias úteis</span></div></li></ol>
        <h3 style="margin-top:22px">Prazos desta turma</h3>
        <ol class="prazos" style="grid-template-columns:repeat({len(c["prazos"])},1fr)">{prazos}</ol>
      </div>
    </div>
  </div>
</section>

<section class="sec depo">
  <div class="wrap">
    <div class="cab topo-dep" style="max-width:none;flex-direction:row"><div style="display:flex;flex-direction:column;gap:12px"><span class="exemplo">exemplo · textos e fotos provisórios</span><h2>Depoimentos</h2><p>De quem passou pelos grupos e cursos do Instituto.</p></div>
      <div class="setas-car"><button type="button" data-dir="-1" aria-label="Anterior">{ICON_UP.replace('M6 15l6-6 6 6','M15 6l-6 6 6 6')}</button><button type="button" data-dir="1" aria-label="Próximo">{ICON_UP.replace('M6 15l6-6 6 6','M9 6l6 6-6 6')}</button></div></div>
    <div class="depos" id="depos">{depos}</div>
    <div class="pontos" aria-hidden="true">{''.join('<i></i>' for _ in DEPOIMENTOS)}</div>
  </div>
</section>

<section class="sec" style="background:#F2EAD6">
  <div class="wrap">
    <div class="cab"><h2>Outros eventos</h2><p>Para continuar o estudo por temas vizinhos.</p></div>
    <ul class="cards tres-col">{rel}</ul>
  </div>
</section>

<section class="sec faq">
  <div class="wrap">
    <div class="cab"><h2>Perguntas frequentes</h2></div>
    <div>{faq}</div>
  </div>
</section>

<section class="sec fecho">
  <img class="explosao" src="{{{{of/ic-explosaao.svg|#d62929=#B91F1F}}}}" alt="" aria-hidden="true">
  <div class="wrap">
    {fecho}
  </div>
</section>
</main>

<footer id="fim">
  <div class="wrap">
    <img src="{{{{of/wm-branco-verm.svg}}}}" alt="Instituto Fendas" width="1830" height="331">
    <span>Instituto Fendas · CNPJ 65.465.820/0001-02 · Fortaleza, CE</span>
  </div>
</footer>

<div class="barra" aria-hidden="true">{barra}</div>

<nav class="setas" aria-label="Navegar pela página">
  <a href="#inicio" aria-label="Voltar ao início">{ICON_UP}</a>
  <a href="#fim" aria-label="Ir para o fim">{ICON_DOWN}</a>
</nav>
<script>
(function(){{
  var s=document.querySelector('.setas'),b=document.querySelector('.barra'),ins=document.getElementById('inscricao');
  if(window.matchMedia('(min-width:900px)').matches){{document.querySelectorAll('.encontro').forEach(function(d){{d.open=true}})}}
  var insVis=true;
  function u(){{var y=window.scrollY;s.classList.toggle('on',y>window.innerHeight*0.8);var on=!insVis&&y>200&&(window.innerHeight+y<document.body.scrollHeight-300);b.classList.toggle('on',on);document.body.classList.toggle('com-barra',on)}}
  var car=document.getElementById('depos'),pts=document.querySelectorAll('.pontos i');
  function passo(){{var f=car.querySelector('figure');return f?f.getBoundingClientRect().width+14:300}}
  document.querySelectorAll('.setas-car button').forEach(function(bt){{bt.addEventListener('click',function(){{car.scrollBy({{left:passo()*+bt.dataset.dir,behavior:'smooth'}})}})}});
  function marca(){{var i=Math.round(car.scrollLeft/passo());pts.forEach(function(p,k){{p.classList.toggle('on',k===i)}})}}
  if(car){{car.addEventListener('scroll',marca,{{passive:true}});marca()}}
  if('IntersectionObserver' in window&&ins){{new IntersectionObserver(function(e){{insVis=e[0].isIntersecting;u()}}).observe(ins)}}
  window.addEventListener('scroll',u,{{passive:true}});u();
}})();
</script>
</body>
</html>"""
    open(f'curso-{slug}-src.html', 'w').write(page)

if __name__ == '__main__':
    for sl in (sys.argv[1:] or CURSOS):
        gerar(sl)
