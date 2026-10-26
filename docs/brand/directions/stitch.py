# python3 stitch.py out.png a.png b.png c.png d.png  (TL, TR, BL, BR zooms of a 1523x761 viewport at 2x)
import sys
from PIL import Image
o=sys.argv[1]; t=[Image.open(f).convert('RGB') for f in sys.argv[2:6]]
S=Image.new('RGB',(3046,1522),'white')
S.paste(t[0],(0,0));S.paste(t[1],(1522,0));S.paste(t[2],(0,760));S.paste(t[3],(1522,760))
S.save(o);print(o,S.size)
