import struct,sys
def read_dat(b):
    assert b[:4]==b'DAT\0',b[:4]
    n,ofs_off,ext_off,name_off,size_off=struct.unpack_from('>5I',b,4)
    offs=struct.unpack_from('>%dI'%n,b,ofs_off); sizes=struct.unpack_from('>%dI'%n,b,size_off)
    nl=struct.unpack_from('>I',b,name_off)[0]
    names=[b[name_off+4+i*nl:name_off+4+(i+1)*nl].split(b'\0')[0].decode() for i in range(n)]
    return [(names[i],b[offs[i]:offs[i]+sizes[i]]) for i in range(n)]
if __name__=='__main__':
    for p in sys.argv[1:]:
        b=open(p,'rb').read(); fs=read_dat(b); print(p.split('/')[-1],len(fs))
        for nm,d in fs: print('  ',nm,len(d),d[:4])
