"""combine.py out.png in1.png in2.png ...  side by side, top aligned, labelled by order"""
import sys
from PIL import Image
out=sys.argv[1]; ims=[Image.open(p).convert('RGB') for p in sys.argv[2:]]
gap=16; w=sum(i.width for i in ims)+gap*(len(ims)-1); h=max(i.height for i in ims)
s=Image.new('RGB',(w,h),(40,40,40)); x=0
for i in ims: s.paste(i,(x,0)); x+=i.width+gap
s.save(out); print(out,s.size)
