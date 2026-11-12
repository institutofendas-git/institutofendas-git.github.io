"""Troca os {{caminho|a=b}} das fontes por arquivos em assets/ (nome com hash), em vez de embutir em base64.
resolver(html, prefixo, pasta_saida) -> html"""
import re, os, io, hashlib
from PIL import Image
_cache = {}
def _arquivo(spec, pasta):
    if spec in _cache: return _cache[spec]
    if spec == 'FONTES':
        import base64
        css = ''.join("@font-face{font-family:'Syne';font-weight:%d;font-style:normal;font-display:block;src:url(data:font/woff2;base64,%s) format('woff2')}\n" % (w, base64.b64encode(open(f'assets/syne-latin-{w}-normal.woff2', 'rb').read()).decode()) for w in (400, 600, 700))
        nome = 'fontes.' + hashlib.sha1(css.encode()).hexdigest()[:8] + '.css'
        os.makedirs(f'{pasta}/assets', exist_ok=True); open(f'{pasta}/assets/{nome}', 'w').write(css); _cache[spec] = nome; return nome
    name, _, rep = spec.partition('|')
    p = name if '/' in name else 'assets/' + name
    base, ext = os.path.splitext(os.path.basename(p))
    if ext == '.svg':
        t = open(p).read()
        for pair in filter(None, rep.split(',')):
            a, b = pair.split('='); t = re.sub(re.escape(a), b, t, flags=re.I)
        t = re.sub(r'<\?xml[^>]*\?>\s*', '', t); t = re.sub(r'>\s+<', '><', t)
        data = t.encode()
    elif ext in ('.woff2', '.webp', '.jpg'):
        data = open(p, 'rb').read()
    else:
        im = Image.open(p); b = io.BytesIO()
        (im if im.mode == 'RGBA' else im.convert('RGB')).save(b, 'WEBP', quality=86); data = b.getvalue(); ext = '.webp'
    nome = f'{base}.{hashlib.sha1(data).hexdigest()[:8]}{ext}'.replace(' ', '-')
    os.makedirs(f'{pasta}/assets', exist_ok=True)
    open(f'{pasta}/assets/{nome}', 'wb').write(data)
    _cache[spec] = nome
    return nome
def resolver(html, prefixo, pasta):
    return re.sub(r'\{\{([^}]+)\}\}', lambda m: prefixo + _arquivo(m.group(1), pasta), html)
