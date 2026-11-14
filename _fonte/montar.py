"""Monta o artefato navegável em ./artefato (arquivos soltos, links relativos, imagens e fontes em assets/)."""
import os, re, glob, shutil, menu, ativos, curso
D = 'artefato'
shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
# página de demonstração: evento com inscrições abertas (só no artefato)
curso.CURSOS['exemplo-inscricoes-abertas'] = dict(curso.CURSOS['gestao-do-sofrimento'], status='aberto', demo=True,
    inscricao=dict(url='#inscricao', lotes=[('R$ 59,90', 'até o primeiro encontro'), ('R$ 69,90', 'depois')], pagamento='Cartão e Pix, pela plataforma de inscrição.'))
curso.MARCAS['exemplo-inscricoes-abertas'] = curso.MARCAS['gestao-do-sofrimento']
curso.gerar('exemplo-inscricoes-abertas'); del curso.CURSOS['exemplo-inscricoes-abertas']
pares = [('home4-src.html', 'index.html'), ('src.html', 'final-de-ano.html')]
pares += [(f, 'evento-' + f[6:].replace('-src', '')) for f in sorted(glob.glob('curso-*-src.html'))]
pares += [(f, f.replace('-src', '')) for f in sorted(glob.glob('formato-*-src.html'))]
pares += [(f, f.replace('-src', '')) for f in sorted(glob.glob('tema-*-src.html'))]
TOPO = "<script>(function(){function t(){try{if(!location.hash){window.scrollTo(0,0);document.documentElement.scrollIntoView({block:'start'})}}catch(e){}}try{if('scrollRestoration' in history)history.scrollRestoration='manual'}catch(e){}t();window.addEventListener('load',t);window.addEventListener('pageshow',t)})();</script>"
def rel(h):
    h = re.sub(r'href="/"', 'href="index.html"', h)
    h = re.sub(r'href="/(#[^"]+)"', r'href="index.html\1"', h)
    h = re.sub(r'href="/final-de-ano/(#[^"]*)?"', lambda m: f'href="final-de-ano.html{m.group(1) or ""}"', h)
    h = re.sub(r'href="/formatos/([a-z-]+)/"', r'href="formato-\1.html"', h)
    h = re.sub(r'href="/eventos/([a-z-]+)/"', r'href="evento-\1.html"', h)
    h = re.sub(r'href="/temas/([a-z-]+)/"', r'href="tema-\1.html"', h)
    return h.replace('</body>', TOPO + '\n</body>', 1)
for src, out in pares:
    h = menu.sem_depoimentos(menu.aplicar(open(src).read()))
    h = rel(ativos.resolver(h, 'assets/', D))
    open(f'{D}/{out}', 'w').write(h)
os.remove('curso-exemplo-inscricoes-abertas-src.html')
ok = set(os.listdir(D))
for f in sorted(ok):
    if not f.endswith('.html'): continue
    t = open(f'{D}/{f}').read()
    for l in re.findall(r'href="([^"#:]+\.html)', t):
        if l not in ok: print('QUEBRADO', f, l)
    for l in re.findall(r'href="(/[^"]*)"', t): print('ABSOLUTO', f, l)
    if '{{' in t or 'base64' in t: print('RESTO', f)
    print(f, len(t) // 1024, 'KB')
print('assets', len(os.listdir(D + '/assets')), sum(os.path.getsize(f'{D}/assets/{x}') for x in os.listdir(D + '/assets')) // 1024, 'KB')
