"""Ricostruisce tutto partendo dai dati: lista, pagina per claude.ai e app nella radice del repository.

Uso:  python3 sorgenti/aggiorna.py
"""
import hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# 1. dati: le due metà della lista finiscono in fasi.json
for script in ('genera_1971_1998.py', 'genera_1999_oggi.py'):
    r = subprocess.run([sys.executable, '-I', os.path.join(HERE, script)], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f'Errore in {script}:\n{r.stderr}')
    print(script, '→', r.stdout.strip().splitlines()[0])

fasi = json.load(open(os.path.join(HERE, 'fasi.json'), encoding='utf-8'))
ids = [x['id'] for v in fasi.values() for x in v]
dup = sorted({i for i in ids if ids.count(i) > 1})
if dup:
    sys.exit(f'Id duplicati: {dup}')

# 2. pagina per claude.ai: modello + dati
modello = open(os.path.join(HERE, 'modello.html'), encoding='utf-8').read()
assert '/*GEN*/null' in modello
pagina = modello.replace('/*GEN*/null', json.dumps(fasi, ensure_ascii=False, separators=(',', ':')), 1)
open(os.path.join(HERE, 'pagina-claude.html'), 'w', encoding='utf-8').write(pagina)

# 3. app installabile nella radice (font in locale, service worker per l'uso offline)
src = pagina
src = src.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
src = re.sub(r'<link rel="preconnect"[^>]*>\n', '', src)
src = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n', '', src)
src = src.replace(re.search(r'<title>.*?</title>\n', src).group(0), '')
faces = [('Barlow Condensed', 600, 'barlow-condensed-latin-600'), ('Barlow Condensed', 800, 'barlow-condensed-latin-800'),
         ('IBM Plex Sans', 400, 'ibm-plex-sans-latin-400'), ('IBM Plex Sans', 500, 'ibm-plex-sans-latin-500'),
         ('IBM Plex Sans', 600, 'ibm-plex-sans-latin-600'), ('IBM Plex Mono', 500, 'ibm-plex-mono-latin-500')]
ff = '\n'.join(f'@font-face{{font-family:"{n}";font-weight:{w};font-style:normal;font-display:swap;src:url(fonts/{f}-normal.woff2) format("woff2")}}' for n, w, f in faces)
base = ('*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%}'
        ':root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0;-webkit-tap-highlight-color:transparent}[hidden]{display:none!important}')
src = src.replace('<style>\n', '<style>\n' + ff + '\n' + base + '\n', 1)
head = '''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Spider-Man Letture</title>
<meta name="theme-color" content="#f3f4f7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#111318" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Spidey">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
'''
i = src.index('</style>') + len('</style>\n')
html = head + src[:i] + '</head>\n<body>\n' + src[i:]
html = html.rstrip() + '''
<script>
if('serviceWorker' in navigator){window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}))}
</script>
</body>
</html>
'''
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)

manifest = {"name": "Spider-Man Letture", "short_name": "Spidey",
            "description": "Ordine di lettura di Spider-Man con progresso salvato sul dispositivo", "lang": "it",
            "start_url": "./", "scope": "./", "display": "standalone", "background_color": "#f3f4f7", "theme_color": "#c8202b",
            "icons": [{"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
                      {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}
open(os.path.join(ROOT, 'manifest.webmanifest'), 'w', encoding='utf-8').write(json.dumps(manifest, indent=2, ensure_ascii=False))

# il nome della cache cambia da solo quando cambia la pagina: il telefono scarica la versione nuova
version = hashlib.sha1(html.encode('utf-8')).hexdigest()[:10]
files = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/apple-touch-icon.png'] + \
        [f'fonts/{f}-normal.woff2' for _, _, f in faces]
sw = f'''// Cache offline: l'app funziona anche senza connessione dopo la prima apertura
const CACHE='spidey-{version}';
const FILES={json.dumps(files)};
self.addEventListener('install',e=>{{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener('fetch',e=>{{
  if(e.request.method!=='GET')return;
  e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||fetch(e.request).then(res=>{{
    if(res.ok&&new URL(e.request.url).origin===location.origin){{const cp=res.clone();caches.open(CACHE).then(c=>c.put(e.request,cp))}}
    return res}}).catch(()=>caches.match('index.html'))));
}});
'''
open(os.path.join(ROOT, 'sw.js'), 'w', encoding='utf-8').write(sw)
print(f'Fatto: {len(ids)} voci nei dati generati, cache {version}')
