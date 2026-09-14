"""Contact sheets for looking at tall full-page shots by eye.
python sheet.py <in.png> <outprefix> <scale> [top] [bottom] [max_h]
Scales the band [top, bottom) of the shot, cuts it into columns of at most max_h pixels
(default 1900), and lays the columns side by side into sheets no wider than 1900 pixels.
Prints the sheet paths."""
import sys
from PIL import Image

src, prefix, scale = sys.argv[1], sys.argv[2], float(sys.argv[3])
im = Image.open(src).convert("RGB")
top = int(sys.argv[4]) if len(sys.argv) > 4 else 0
bottom = int(sys.argv[5]) if len(sys.argv) > 5 else im.height
max_h = int(sys.argv[6]) if len(sys.argv) > 6 else 1900
band = im.crop((0, top, im.width, min(bottom, im.height)))
if scale != 1:
    band = band.resize((max(1, int(band.width * scale)), max(1, int(band.height * scale))), Image.LANCZOS)
cols = []
y = 0
while y < band.height:
    cols.append(band.crop((0, y, band.width, min(band.height, y + max_h))))
    y += max_h
gap = 12
per = max(1, (1900 + gap) // (band.width + gap))
n = 0
for i in range(0, len(cols), per):
    group = cols[i:i + per]
    w = sum(c.width for c in group) + gap * (len(group) - 1)
    h = max(c.height for c in group)
    sheet = Image.new("RGB", (w, h), (60, 60, 60))
    x = 0
    for c in group:
        sheet.paste(c, (x, 0))
        x += c.width + gap
    out = f"{prefix}-{n}.png"
    sheet.save(out)
    print(out, sheet.size)
    n += 1
