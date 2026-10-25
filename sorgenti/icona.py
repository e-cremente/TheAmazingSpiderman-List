from PIL import Image, ImageDraw
import sys
def make(size, path):
    S=1024
    im=Image.new('RGB',(S,S),'#c8202b'); d=ImageDraw.Draw(im)
    # pila di albi: due copertine sfalsate
    d.rounded_rectangle((330,250,690,740),24,fill='#8f1219')
    d.rounded_rectangle((290,290,650,780),24,fill='#ffffff')
    # testata e righe della copertina
    d.rectangle((330,330,610,400),fill='#16181d')
    for y in (450,500,550): d.rectangle((330,y,560,y+22),fill='#dde0e7')
    # bollino "letto"
    cx,cy,r=660,700,150
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill='#16181d',outline='#c8202b',width=18)
    d.line([(cx-70,cy+5),(cx-15,cy+60),(cx+75,cy-55)],fill='#ffffff',width=38,joint='curve')
    im.resize((size,size),Image.LANCZOS).save(path)
o=sys.argv[1]
make(512,o+'/icon-512.png'); make(192,o+'/icon-192.png'); make(180,o+'/apple-touch-icon.png')
