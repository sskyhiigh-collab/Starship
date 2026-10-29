import numpy as np, struct
from PIL import Image
TAB=[[2,8],[5,17],[9,29],[13,42],[18,60],[24,80],[33,106],[47,183]]
def _ext4(x): return (x<<4)|x
def _ext5(x): return (x<<3)|(x>>2)
def dec_block(w):  # w: 64-bit standard ETC1 value (big-endian order bits)
    out=np.zeros((4,4,3),np.int32)
    diff=(w>>33)&1; flip=(w>>32)&1
    t1=(w>>37)&7; t2=(w>>34)&7
    if diff:
        r=(w>>59)&31; g=(w>>51)&31; b=(w>>43)&31
        dr=((w>>56)&7); dg=((w>>48)&7); db=((w>>40)&7)
        dr=dr-8 if dr>3 else dr; dg=dg-8 if dg>3 else dg; db=db-8 if db>3 else db
        c1=(_ext5(r),_ext5(g),_ext5(b)); c2=(_ext5(r+dr),_ext5(g+dg),_ext5(b+db))
    else:
        c1=(_ext4((w>>60)&15),_ext4((w>>52)&15),_ext4((w>>44)&15))
        c2=(_ext4((w>>56)&15),_ext4((w>>48)&15),_ext4((w>>40)&15))
    for x in range(4):
        for y in range(4):
            i=x*4+y
            lsb=(w>>i)&1; msb=(w>>(i+16))&1
            sub = (y>=2) if flip else (x>=2)
            c=c2 if sub else c1; t=TAB[t2 if sub else t1]
            m=t[lsb]; m=-m if msb else m
            out[y,x]=[min(255,max(0,c[k]+m)) for k in range(3)]
    return out
def decode(data,W,H,alpha=True):
    img=np.zeros((H,W,4),np.uint8); p=0; bs=16 if alpha else 8
    for ty in range(0,H,8):
        for tx in range(0,W,8):
            for (bx,by) in ((0,0),(4,0),(0,4),(4,4)):
                if alpha:
                    a=struct.unpack_from('<Q',data,p)[0]; p+=8
                else: a=None
                w=struct.unpack_from('<Q',data,p)[0]; p+=8
                rgb=dec_block(w)
                X=tx+bx; Y=ty+by
                img[Y:Y+4,X:X+4,:3]=rgb
                if alpha:
                    for x in range(4):
                        for y in range(4):
                            v=(a>>((x*4+y)*4))&15; img[Y+y,X+x,3]=v*17
                else: img[Y:Y+4,X:X+4,3]=255
    return img
