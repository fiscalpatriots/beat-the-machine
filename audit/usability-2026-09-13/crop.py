"""crop.py in.png out.png top height  (crops a vertical band out of a full-page shot)"""
import sys
from PIL import Image
src, dst, top, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
im = Image.open(src)
im.crop((0, top, im.width, min(im.height, top + h))).save(dst)
print(dst, im.size)
