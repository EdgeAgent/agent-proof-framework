from PIL import Image, ImageDraw, ImageFont
import os
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(BASE,"docs/assets"); os.makedirs(OUT,exist_ok=True)
def font(sz,bold=False):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try: return ImageFont.truetype(p,sz)
        except: pass
    return ImageFont.load_default()
def disc(d,cx,cy,r,color): d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=color)
def mark(d,cx,cy,s,color):
    # checkmark in circle: receipt stamp
    d.ellipse([cx-s,cy-s,cx+s,cy+s],outline=color,width=6)
    d.line([(cx-s*0.55,cy),(cx-s*0.15,cy+s*0.45),(cx+s*0.6,cy-s*0.5)],fill=color,width=7)
def icon(path,size,bg=(11,18,32),fg=(45,212,191)):
    im=Image.new("RGB",(size,size),bg); d=ImageDraw.Draw(im); disc(d,size//2,size//2,size*0.42,(20,40,70)); mark(d,size//2,size//2,size*0.24,fg)
    d.text((size//2,size*0.82),"PROOF",font=font(size//10,True),fill=(255,255,255),anchor="mm"); im.save(path)
def hero():
    im=Image.new("RGB",(1200,400),(11,18,32)); d=ImageDraw.Draw(im)
    d.rectangle([0,340,1200,400],fill=(45,212,191)); mark(d,110,170,70,(45,212,191))
    d.text((220,120),"PROOF",font=font(96,True),fill=(255,255,255)); d.text((220,230),"The Agent Receipt Layer",font=font(44,True),fill=(45,212,191))
    d.text((220,290),"Who ran it. What it did. Who approved it. Provable.",font=font(28),fill=(200,210,230))
    d.text((30,358),"Hash-chained  •  Approval-gated  •  Tamper-evident",font=font(24,True),fill=(11,18,32)); im.save(f"{OUT}/hero.png")
def flow(path,title,boxes,sub):
    W,H=1400,460; im=Image.new("RGB",(W,H),(245,247,250)); d=ImageDraw.Draw(im)
    d.text((40,30),title,font=font(36,True),fill=(11,18,32)); d.text((40,75),sub,font=font(22),fill=(80,90,110))
    n=len(boxes); bw=170; gap=(W-80-(bw*n))//(n-1) if n>1 else 0; y=180
    for i,b in enumerate(boxes):
        x=40+i*(bw+gap); d.rounded_rectangle([x,y,x+bw,300],radius=18,fill=(11,18,32)); d.text((x+bw//2,240),b,font=font(20,True),fill=(255,255,255),anchor="mm")
        if i<n-1: d.polygon([(x+bw+5,240),(x+bw+gap-5,225),(x+bw+gap-5,255)],fill=(45,212,191))
    d.rectangle([40,340,W-40,410],fill=(251,191,36)); d.text((W//2,375),"APPROVAL GATE  •  unapproved send / ship / pay / delete / merge = BLOCKED",font=font(22,True),fill=(11,18,32),anchor="mm"); im.save(path)
icon(f"{OUT}/icon.png",512); icon(f"{OUT}/favicon.png",64); hero()
flow(f"{OUT}/workflow.png","HOW A RUN BECOMES PROOF",["RUN","STEP","HASH","GATE","RECEIPT","VERIFY","CLIENT PROOF"],"Every step links to the previous hash. Change one word and verification fails.")
flow(f"{OUT}/architecture.png","ARCHITECTURE",["CLI","RECEIPT","CHAIN","GATE","TRUST","PROOF PAGE"],"Mock agents today. Real runners next. Receipt, chain, gate, and trust are real.")
print("assets done")
