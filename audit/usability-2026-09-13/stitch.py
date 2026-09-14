"""stitch.py <dir>  joins every <name>.partNN.png listed in <name>.parts.json into <name>.png
and removes the parts."""
import sys, os, json, glob
from PIL import Image

d = sys.argv[1]
for meta in glob.glob(os.path.join(d, "*.parts.json")):
    info = json.load(open(meta))
    out = meta[:-len(".parts.json")] + ".png"
    full = Image.new("RGB", (info["width"], info["H"]), (255, 255, 255))
    for p in info["parts"]:
        im = Image.open(p["part"]).convert("RGB")
        full.paste(im, (0, p["y"]))
    full.save(out, optimize=True)
    for p in info["parts"]:
        os.remove(p["part"])
    os.remove(meta)
    print(out, full.size)
