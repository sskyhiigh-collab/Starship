import os as _os, sys as _sys; _sys.path.insert(0,_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import paths, os, sys
import zipfile,struct,subprocess,numpy as np,sys,os
sys.path.insert(0,os.path.join(paths.TOOLS,'sf3ds'))
from sf64res import crc64
Z=paths.SF64_O2R
z=zipfile.ZipFile(Z)
SR=32000; LOOP_START=70400; LOOP_END=70400+4200611; EXTRA=2048   # SFA Corneria: 2.2 s intro, 131.27 s loop (measured)
SEQ_ID=2; SEQ_PATH='ast_audio/ast_audio_v1_sequence_E7BC0'
FONT_PATH='ast_audio/custom_corneria_font'
SIDES=['L','R']
SAMPLE={k:f'ast_audio/custom_corneria_sample_{k}' for k in SIDES}; PCM={k:f'ast_audio/custom_corneria_{k}.pcm' for k in SIDES}
SEQ_VOL=int(os.environ.get('SEQ_VOL','0x7F'),0)
GAIN_DB=float(os.environ.get('GAIN_DB','0'))   # plain gain on the source audio (no limiting); 0 = as mastered
# channel volume multiplier (0x80 = 1.0, 0xFF = ~2.0). Volumes are squared by the engine, so 0xFF is ~4x;
# the per-note gain is capped at unity, so this mostly cancels the game's own BGM attenuation.
VOL_MOD=int(os.environ.get('VOL_MOD','0xFF'),0)   # loudness boost; a limiter keeps peaks at -1 dBFS
# 1. audio: mono 32k, trimmed to loop end (+tail), vorbis
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',sys.argv[1],'-ac','2','-ar',str(SR),'-af',f'volume={GAIN_DB}dB','-f','s16le','raw32.raw'],check=True)
st=np.fromfile('raw32.raw','<i2').reshape(-1,2)[:LOOP_END+EXTRA]
nframes=len(st)
files={}
# raw little-endian s16 PCM per side: loaded synchronously (Starship v2.0's threaded .ogg decoder races the mixer and crashes)
for i,k in enumerate(SIDES):
    files[PCM[k]]=np.ascontiguousarray(st[:,i]).astype('<i2').tobytes()
    files[SAMPLE[k]]=f'''<Sample Version="0" Codec="S16" Medium="Ram" bit26="0" Size="{nframes*2}" Path="{PCM[k]}">
    <ADPCMLoop Start="{LOOP_START}" End="{LOOP_END}" Count="4294967295"/>
</Sample>
'''.encode()
INST=''.join(f'''        <Instrument IsValid="true" Loaded="1" NormalRangeLo="0" NormalRangeHi="127" ReleaseRate="208">
            <Envelopes>
                <Envelope Delay="1" Arg="32700"/>
                <Envelope Delay="-1" Arg="0"/>
            </Envelopes>
            <NormalNotesSound Tuning="1.0" SampleRef="{SAMPLE[k]}"/>
        </Instrument>
''' for k in SIDES)
files[FONT_PATH]=f'''<SoundFont Version="0" Num="34" Medium="Cart" CachePolicy="Either" Data1="{0x03FF}" Data2="{(2<<8)|0}" Data3="0">
    <Instruments>
{INST}    </Instruments>
</SoundFont>
'''.encode()
# 2. sequence: one channel, one layer, one endless note on instrument 0 at C4 (pitch 1.0)
def u16(x): return struct.pack('>H',x)
seq=bytearray()
# two channels (hard left / hard right) so each speaker gets the sample at full gain;
# a single centred voice is mixed at ~0.7 x the (squared) channel volume and comes out very quiet
# mute behaviour 0x20 (soften only): while paused the track keeps running at a low volume.
# Any behaviour that stops or freezes notes (0x40 / 0x08) kills the single endless note for good.
VOICES=int(os.environ.get('VOICES_PER_SIDE','1'))
NCH=2*VOICES
PAUSE_VOL=int(os.environ.get('PAUSE_VOL','0x20'),0)  # music level while paused (0x7F = unchanged)
seq+=bytes([0xD3,0x20, 0xD5,PAUSE_VOL, 0xD7])+u16((1<<NCH)-1)
ptrs=[]
for c in range(NCH): ptrs.append(len(seq)+1); seq+=bytes([0x90|c,0,0])
seq+=bytes([0xDB,SEQ_VOL, 0xDD,0x01])
sl=len(seq); seq+=bytes([0xFD,0xFF,0xFF,0xFB])+u16(sl)
for c,pan in enumerate([0x00,0x7F]*VOICES):
    ch=len(seq); seq[ptrs[c]:ptrs[c]+2]=u16(ch)
    seq+=bytes([0xC4, 0xC1,c%2, 0xDF,0x7F, 0xE0,VOL_MOD, 0xDC,0x80, 0xDD,pan])
    lp=len(seq)+1; seq+=bytes([0x90,0,0])
    cl=len(seq); seq+=bytes([0xFD,0xFF,0xFF,0xFB])+u16(cl)
    ly=len(seq); seq[lp:lp+2]=u16(ly)
    seq+=bytes([0x40|0x27,0xFF,0xFF,0x7F, 0xFB])+u16(ly)
seq+=bytes([0xFF])
while len(seq)%16: seq.append(0)
orig=z.read(SEQ_PATH)
files[SEQ_PATH]=orig[:0x40]+struct.pack('<I',len(seq))+bytes(seq)
# 3. soundfont table: append font 33
ft=z.read('ast_audio/audio_soundfont_table'); hdr,b=ft[:0x40],ft[0x40:]
med,addr,cnt=struct.unpack_from('<hII',b)
ent=b[10:10+20*cnt]
crc,size,m,cp,s1,s2,s3=struct.unpack_from('<QIbbhhh',ent,20*24)
new=struct.pack('<QIbbhhh',crc64(FONT_PATH),size,m,cp,s1,(2<<8)|0,s3)
NEW_FONT=cnt
files['ast_audio/audio_soundfont_table']=hdr+struct.pack('<hII',med,addr,cnt+1)+ent+new+b[10+20*cnt:]
# 4. seq->font table: point seq 2 at the new font
sf=z.read('ast_audio/audio_seq_font_table'); hdr,b=sf[:0x40],sf[0x40:]
pre=b[:4]; n=struct.unpack_from('<I',b,4)[0]; data=bytearray(b[8:8+n])
off=len(data); data+=bytes([1,NEW_FONT]); data[2*SEQ_ID:2*SEQ_ID+2]=u16(off)
files['ast_audio/audio_seq_font_table']=hdr+pre+struct.pack('<I',len(data))+bytes(data)+b[8+n:]
out=sys.argv[2]
with zipfile.ZipFile(out,'w',zipfile.ZIP_STORED) as zo:
    for k in sorted(files): zo.writestr(k,files[k])
print('frames',nframes,'secs %.2f'%(nframes/SR),'pcm',nframes*4,'seq',seq.hex(' '))
print('font table entries',cnt+1,'trailing bytes',len(b)-8-n)
