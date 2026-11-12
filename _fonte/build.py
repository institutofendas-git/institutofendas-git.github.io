import re,base64,io
from PIL import Image
import sys
src=sys.argv[1] if len(sys.argv)>1 else 'src.html'; out=sys.argv[2] if len(sys.argv)>2 else 'final-de-ano-no-fendas.html'
s=open(src).read()
def enc(spec):
    name,_,rep=spec.partition('|')
    p=name if '/' in name else 'assets/'+name
    if p.endswith('.woff2'): return 'data:font/woff2;base64,'+base64.b64encode(open(p,'rb').read()).decode()
    if p.endswith('.svg'):
        t=open(p).read()
        for pair in filter(None,rep.split(',')):
            a,b=pair.split('=')
            t=re.sub(re.escape(a),b,t,flags=re.I)
        return 'data:image/svg+xml;base64,'+base64.b64encode(t.encode()).decode()
    if p.endswith('.webp'):
        return 'data:image/webp;base64,'+base64.b64encode(open(p,'rb').read()).decode()
    if p.endswith('.jpg'):
        return 'data:image/jpeg;base64,'+base64.b64encode(open(p,'rb').read()).decode()
    im=Image.open(p); b=io.BytesIO()
    (im if im.mode=='RGBA' else im.convert('RGB')).save(b,'WEBP',quality=86)
    return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
s=re.sub(r'\{\{([^}]+)\}\}',lambda m:enc(m.group(1)),s)
open(out,'w').write(s); print(len(s))
