"""Pixels e rastreamento do site. Para ligar, preencher os códigos abaixo e publicar de novo.
Enquanto tudo estiver vazio, nenhum rastreador carrega e não aparece aviso de cookies.

Mede no site: visitas (todas as páginas), visualização de evento e de campanha, clique em
comprar/inscrever (com valor, quando a página mostra o preço) e clique em contato.
A compra em si acontece na Hotmart/Sympla: configurar o mesmo pixel e a mesma tag lá.
"""
import json, re

META_PIXEL = ''          # Gerenciador de Eventos da Meta > Fontes de dados > ID do pixel (só números)
GA4 = ''                 # Google Analytics > Administrador > Fluxos de dados > ID da métrica (G-XXXXXXXXXX)
GOOGLE_ADS = ''          # opcional: AW-XXXXXXXXX, se forem rodar anúncios no Google
GOOGLE_ADS_CHECKOUT = '' # opcional: rótulo da conversão "clique em comprar" no Google Ads
VERIFICACAO = {          # opcional: códigos de verificação de domínio (meta tags)
    'facebook-domain-verification': '',
    'google-site-verification': '',
}

ATIVO = bool(META_PIXEL or GA4 or GOOGLE_ADS)


def head():
    h = ''.join(f'<meta name="{k}" content="{v}">\n' for k, v in VERIFICACAO.items() if v)
    if not ATIVO:
        return h
    cfg = json.dumps({'meta': META_PIXEL, 'ga4': GA4, 'ads': GOOGLE_ADS, 'adsCheckout': GOOGLE_ADS_CHECKOUT})
    # Consentimento começa negado (LGPD); só carrega os scripts depois do "Aceitar".
    return h + f"""<script>
window.FENDAS_RASTREIO={cfg};
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}
gtag('consent','default',{{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500}});
</script>
"""


CSS = r"""
.cookies{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:60;max-width:560px;margin:0 auto;background:var(--escuro);color:var(--creme);border-radius:10px;padding:16px 18px;box-shadow:0 24px 50px -20px rgba(0,0,0,.6);border:1px solid rgba(249,242,222,.25);display:flex;flex-wrap:wrap;gap:12px 16px;align-items:center;font-size:14px;line-height:1.45}
.cookies[hidden]{display:none!important}
.cookies p{flex:1 1 260px;margin:0}.cookies a{color:var(--creme)}
.cookies .bts{display:flex;gap:8px}
.cookies button{font:600 14px/1 'Syne',sans-serif;border-radius:999px;padding:11px 16px;cursor:pointer;border:1.5px solid var(--creme)}
.cookies .sim{background:var(--creme);color:var(--vinho)}.cookies .nao{background:transparent;color:var(--creme)}
.pref-cookies{background:none;border:0;padding:0;color:inherit;font:inherit;text-decoration:underline;cursor:pointer;opacity:.8}
"""

# Sempre ativo: repassa as UTMs da visita para os links da Hotmart/Sympla (atribuição de venda por campanha).
JS_UTM = r"""<script>
(function(){try{var q=new URLSearchParams(location.search),k=['utm_source','utm_medium','utm_campaign','utm_content','utm_term','src','sck'],p={};
k.forEach(function(x){if(q.get(x))p[x]=q.get(x)});try{if(Object.keys(p).length)sessionStorage.setItem('fendas_utm',JSON.stringify(p));else p=JSON.parse(sessionStorage.getItem('fendas_utm')||'{}')}catch(e){}
if(!Object.keys(p).length)return;document.querySelectorAll('a[href*="pay.hotmart.com"],a[href*="sympla.com.br"]').forEach(function(a){var u=new URL(a.href);Object.keys(p).forEach(function(x){if(!u.searchParams.has(x))u.searchParams.set(x,p[x])});a.href=u.toString()})}catch(e){}})();
</script>"""

JS = r"""<div class="cookies" id="cookies" role="dialog" aria-live="polite" aria-label="Cookies" hidden>
  <p>Usamos cookies da Meta e do Google para medir as visitas e melhorar a divulgação dos eventos. <a href="/privacidade/">Saiba mais</a>.</p>
  <div class="bts"><button type="button" class="nao" data-c="0">Recusar</button><button type="button" class="sim" data-c="1">Aceitar</button></div>
</div>
<script>
(function(){
  var C=window.FENDAS_RASTREIO;if(!C)return;var K='fendas_consentimento',box=document.getElementById('cookies'),on=false;
  function ler(){try{return localStorage.getItem(K)}catch(e){return null}}
  function grava(v){try{localStorage.setItem(K,v)}catch(e){}}
  function carrega(src){var s=document.createElement('script');s.async=true;s.src=src;document.head.appendChild(s)}
  function liga(){if(on)return;on=true;
    gtag('consent','update',{ad_storage:'granted',analytics_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'});
    if(C.ga4||C.ads){carrega('https://www.googletagmanager.com/gtag/js?id='+(C.ga4||C.ads));gtag('js',new Date());if(C.ga4)gtag('config',C.ga4);if(C.ads)gtag('config',C.ads)}
    if(C.meta){!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init',C.meta);fbq('track','PageView')}
    var v=document.body.dataset.ver;if(v)ev('ViewContent','view_item',JSON.parse(v));
  }
  function ev(meta,ga,d){d=d||{};if(!on)return;
    if(window.fbq&&meta)fbq('track',meta,{content_name:d.nome,content_category:d.categoria,value:d.valor,currency:d.valor?'BRL':undefined});
    if(C.ga4&&ga)gtag('event',ga,{currency:'BRL',value:d.valor,items:[{item_name:d.nome,item_category:d.categoria,price:d.valor}]});
    if(C.ads&&C.adsCheckout&&meta==='InitiateCheckout')gtag('event','conversion',{send_to:C.ads+'/'+C.adsCheckout,value:d.valor,currency:'BRL'});
  }
  window.fendasEvento=ev;
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a)return;var h=a.href||'';
    if(/pay\.hotmart\.com|sympla\.com\.br/.test(h)||a.dataset.checkout!==undefined){var c=a.closest('.combo'),p=c&&c.querySelector('.preco strong'),val=p?parseFloat(p.textContent.replace(/[^\d,]/g,'').replace(',','.')):undefined;
      var base=document.body.dataset.ver?JSON.parse(document.body.dataset.ver):{};ev('InitiateCheckout','begin_checkout',{nome:c?(c.querySelector('h3')||{}).textContent:base.nome,categoria:c?'Combo':base.categoria,valor:val||base.valor})}
    else if(/instagram\.com|wa\.me|whatsapp|^mailto:/.test(h))ev('Contact','contato',{nome:/instagram/.test(h)?'Instagram':/mailto/.test(h)?'E-mail':'WhatsApp'});
  },true);
  box.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;grava(b.dataset.c);box.hidden=true;if(b.dataset.c==='1')liga()});
  document.addEventListener('click',function(e){if(e.target.closest('.pref-cookies')){box.hidden=false}});
  var s=ler();if(s==='1')liga();else if(s!=='0')box.hidden=false;
})();
</script>"""

RODAPE = '<span><a href="/privacidade/">Privacidade</a> · <button type="button" class="pref-cookies">Preferências de cookies</button></span>'


def aplicar(html):
    """A página pode trazer <!--VER:{json}--> com nome, categoria e valor, para o ViewContent."""
    m = re.search(r'<!--VER:(.*?)-->', html)
    ver = json.loads(m.group(1)) if m else None
    if m: html = html.replace(m.group(0), '')
    html = html.replace('<style>', head() + '<style>', 1)
    html = html.replace('</body>', JS_UTM + '\n</body>', 1)
    if not ATIVO:
        return html
    if ver:
        html = html.replace('<body>', "<body data-ver='" + json.dumps(ver, ensure_ascii=False).replace("'", '&#39;') + "'>", 1)
    html = html.replace('</style>', CSS + '</style>', 1)
    html = html.replace('</span>\n  </div>\n</footer>', '</span>\n    ' + RODAPE + '\n  </div>\n</footer>', 1)
    html = html.replace('</body>', JS + '\n</body>', 1)
    return html
