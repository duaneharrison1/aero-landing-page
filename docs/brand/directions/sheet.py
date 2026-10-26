import sys
from PIL import Image
d=sys.argv[1]; ids=sys.argv[2].split(','); w=880
ims=[Image.open(f'{d}/shots/{i}.png').convert('RGB') for i in ids]
ims=[i.resize((w,int(i.height*w/i.width))) for i in ims]
rows=(len(ims)+1)//2
hs=[max(ims[r*2+c].height for c in range(2) if r*2+c<len(ims)) for r in range(rows)]
S=Image.new('RGB',(w*2+16,sum(hs)+16*rows),'white');y=0
for r in range(rows):
  for c in range(2):
    k=r*2+c
    if k<len(ims):S.paste(ims[k],(c*(w+16),y))
  y+=hs[r]+16
S.thumbnail((1800,2400));S.save(sys.argv[3],quality=78)
