"""Monta o site real em ../site-v2 (depois copiado para o clone do repositório).
Caminhos: /eventos/<slug>/, /formatos/<slug>/, /final-de-ano/, /assets/. /cursos/<slug>/ redireciona para /eventos/<slug>/."""
import os, re, shutil, glob, sys, menu, ativos, rastreio
R = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/site-v2'
U = 'https://institutofendas.com.br'
shutil.rmtree(R, ignore_errors=True); os.makedirs(R)
pares = [('home4-src.html', 'index.html'), ('src.html', 'final-de-ano/index.html')]
pares += [(f, 'eventos/%s/index.html' % f[6:-9]) for f in sorted(glob.glob('curso-*-src.html'))]
pares += [(f, 'formatos/%s/index.html' % f[8:-9]) for f in sorted(glob.glob('formato-*-src.html'))]
pares += [(f, 'temas/%s/index.html' % f[5:-9]) for f in sorted(glob.glob('tema-*-src.html'))]
if rastreio.ATIVO: pares.append(('privacidade-src.html', 'privacidade/index.html'))
urls = []
# Ícone com endereço fixo e tamanho múltiplo de 48: é o que o Google pede para mostrar na busca.
ICONES = '<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/favicon-192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="/apple-touch-icon.png">'
icones = lambda h: re.sub(r'<link rel="icon"[^>]*>', ICONES, h, count=1)
for src, out in pares:
    h = icones(ativos.resolver(menu.sem_depoimentos(menu.aplicar(open(src).read())), '/assets/', R))
    assert '{{' not in h and 'noindex' not in h, out
    os.makedirs(os.path.dirname(f'{R}/{out}') or R, exist_ok=True)
    open(f'{R}/{out}', 'w').write(h)
    urls.append('/' + out.replace('index.html', ''))
    if out.startswith(('eventos/', 'formatos/', 'temas/')):
        p = 'previas/' + {'eventos/': 'curso-', 'formatos/': 'formato-', 'temas/': 'tema-'}[out[:out.index('/') + 1]] + out.split('/')[1] + '.jpg'
        shutil.copy(p, f'{R}/{os.path.dirname(out)}/preview.jpg')
    if out.startswith('eventos/'):  # endereço antigo continua funcionando
        sl = out.split('/')[1]; os.makedirs(f'{R}/cursos/{sl}')
        open(f'{R}/cursos/{sl}/index.html', 'w').write(f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Instituto Fendas</title><link rel="canonical" href="{U}/eventos/{sl}/"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=/eventos/{sl}/"><script>location.replace("/eventos/{sl}/"+location.hash)</script></head><body><a href="/eventos/{sl}/">Continuar</a></body></html>')
shutil.copytree('figurinhas', f'{R}/figurinhas')  # ferramenta interna, fora do sitemap e dos buscadores
shutil.copy('preview.jpg', f'{R}/final-de-ano/preview.jpg'); shutil.copy('preview-home.jpg', f'{R}/preview.jpg')
for f in ('favicon.ico', 'favicon-192.png', 'apple-touch-icon.png'): shutil.copy('of/' + f, f'{R}/{f}')
open(f'{R}/CNAME', 'w').write('institutofendas.com.br\n'); open(f'{R}/.nojekyll', 'w').write('')
open(f'{R}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\nDisallow: /_fonte/\nDisallow: /figurinhas/\nSitemap: {U}/sitemap.xml\n')
open(f'{R}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{U}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
h404 = icones(ativos.resolver(menu.aplicar(open('404-src.html').read()), '/assets/', R))
open(f'{R}/404.html', 'w').write(h404)
tot = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(R) for f in fs)
print(len(urls), 'páginas;', tot // 1024, 'KB no total;', 'html:', ', '.join(f"{u} {os.path.getsize(R + u + 'index.html') // 1024}KB" for u in urls[:4]))
