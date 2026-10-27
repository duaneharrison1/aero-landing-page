"""Bundle pages-round.html into one self-contained file (inline CSS, JS and fonts). Usage: python3 bundle_pages_round.py <out.html>"""
import re, sys, base64, urllib.request
out = sys.argv[1]
h = open("pages-round.html").read()
css = urllib.request.urlopen(urllib.request.Request("https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap", headers={"User-Agent": "Mozilla/5.0 Chrome/120"})).read().decode()
def emb(m):
    d = urllib.request.urlopen(m.group(1)).read()
    return "url(data:font/ttf;base64," + base64.b64encode(d).decode() + ")"
css = re.sub(r"url\((https://[^)]+)\)", emb, css)
h = re.sub(r'<link rel="preconnect"[^>]*>', "", h)
h = re.sub(r'<link href="https://fonts.googleapis[^>]*>', "<style>" + css + "</style>", h)
for f in ["tokens.css", "components.css", "board.css", "pages-round.css"]:
    h = h.replace(f'<link rel="stylesheet" href="{f}">', "<style>" + open(f).read() + "</style>")
for f in ["board.js", "glass-v3.js"]:
    h = h.replace(f'<script src="{f}"></script>', "<script>" + open(f).read().replace("</script>", "<\\/script>") + "</script>")
assert "href=\"tokens.css\"" not in h and "src=\"board.js\"" not in h
open(out, "w").write(h)
print(out, len(h))
