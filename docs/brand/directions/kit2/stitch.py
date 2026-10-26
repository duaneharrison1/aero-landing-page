"""Stacks screenshot parts vertically: stitch.py out.png part1.png part2.png ..."""
import sys
from PIL import Image
ims = [Image.open(f) for f in sys.argv[2:]]
out = Image.new('RGB', (ims[0].width, sum(i.height for i in ims)), 'white')
y = 0
for i in ims:
    out.paste(i, (0, y)); y += i.height
out.save(sys.argv[1], optimize=True)
