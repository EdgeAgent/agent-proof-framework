from PIL import Image, ImageDraw, ImageFont
import os
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(BASE,"docs/screenshots"); os.makedirs(OUT,exist_ok=True)
def render(title,src,dst):
    lines=open(src).read().strip().splitlines()
    try: f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",20); fh=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",22)
    except: f=fh=ImageFont.load_default()
    W=1100; H=80+28*len(lines)+20; im=Image.new("RGB",(W,H),(11,18,32)); d=ImageDraw.Draw(im)
    d.text((30,25),title,font=fh,fill=(45,212,191))
    for i,l in enumerate(lines): d.text((30,70+28*i),l[:105],font=f,fill=(230,235,245))
    im.save(dst); open(dst.replace(".png",".txt"),"w").write(open(src).read())
render("PROOF — DEMO RUN","/tmp/proof-demo.txt",f"{OUT}/demo-run.png")
render("PROOF — VERIFY: CHAIN INTACT","/tmp/proof-verify.txt",f"{OUT}/verify-ok.png")
render("PROOF — TAMPER DETECTED","/tmp/proof-tamper.txt",f"{OUT}/tamper-detected.png")
print("screenshots done")
