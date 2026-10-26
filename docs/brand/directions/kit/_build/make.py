"""Assemble kit/pages.html from template.html + the logo symbols. Run logos.py first."""
import os, json
H = os.path.dirname(os.path.abspath(__file__))
t = open(f'{H}/template.html').read()
t = t.replace('<!--DEFS-->', open(f'{H}/defs.svg').read())
t = t.replace('/*LOGOS*/[]', json.dumps(json.load(open(f'{H}/logos.json'))))
open(os.path.join(os.path.dirname(H), 'pages.html'), 'w').write(t)
print('ok', len(t))
