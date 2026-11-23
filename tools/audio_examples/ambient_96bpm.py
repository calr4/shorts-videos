import numpy as np, wave, sys
sr=44100; D=16.0; n=int(sr*D); t=np.arange(n)/sr
def note(m): return 440*2**((m-69)/12)
out=np.zeros((n,2))
bpm=96; beat=60/bpm; bar=beat*4
chords=[[50,57,62,66,69],[47,54,59,62,66],[43,50,55,59,62],[45,52,57,61,64]]  # D, Bm, G, A voicings
# pad
for i in range(int(D/bar)+1):
    ch=chords[i%4]; s0=i*bar
    seg=(t>=s0-0.3)&(t<s0+bar+0.6); tt=t[seg]-s0
    env=np.clip((tt+0.3)/0.5,0,1)*np.clip((bar+0.6-tt)/0.8,0,1)
    for j,m in enumerate(ch):
        f=note(m); 
        for det,pan in ((-0.004,0.3),(0.004,0.7)):
            w=sum(np.sin(2*np.pi*f*(1+det)*h*tt + j)/h**1.7 for h in (1,2,3,4))
            out[seg,0]+=w*env*0.05*(1-pan); out[seg,1]+=w*env*0.05*pan
# arp plucks (8th notes) from 2.5s
k=0; s0=2.5
while s0<D-0.6:
    ch=chords[int(s0//bar)%4]; m=ch[[1,2,4,3,2,4,3,1][k%8]]+12
    seg=(t>=s0)&(t<s0+0.6); tt=t[seg]-s0
    w=(np.sin(2*np.pi*note(m)*tt)+0.3*np.sin(4*np.pi*note(m)*tt))*np.exp(-tt*7)*np.clip(tt/0.004,0,1)
    pan=0.35+0.3*(k%2); g=0.11*min(1,(s0-2.5)/2.5+0.4)
    out[seg,0]+=w*g*(1-pan); out[seg,1]+=w*g*pan
    s0+=beat/2; k+=1
# kick + soft hat from 5.25s (when the scroll starts)
s0=np.ceil(5.25/beat)*beat; b=0
while s0<D-0.8:
    seg=(t>=s0)&(t<s0+0.35); tt=t[seg]-s0
    kk=np.sin(2*np.pi*(48*tt+ (110/18)*(1-np.exp(-tt*18))))*np.exp(-tt*9)
    out[seg,:]+= (kk*0.42)[:,None]
    h0=s0+beat/2; seg=(t>=h0)&(t<h0+0.06); tt=t[seg]-h0
    rng=np.random.default_rng(b); hh=rng.standard_normal(tt.size); hh=np.diff(hh,prepend=0)*np.exp(-tt*70)
    out[seg,:]+=(hh*0.05)[:,None]
    s0+=beat; b+=1
# whoosh at the night switch (2.75s) and a soft chime at the booking (13.4s)
rng=np.random.default_rng(7); nz=rng.standard_normal(n); nz=np.convolve(nz,np.ones(60)/60,'same')
out+= (nz*np.exp(-((t-2.9)/0.45)**2)*0.9)[:,None]
for m,dl in ((81,0),(85,0.09),(88,0.18)):
    seg=t>=13.4+dl; tt=t[seg]-13.4-dl
    out[seg,:]+=(np.sin(2*np.pi*note(m)*tt)*np.exp(-tt*3.2)*0.09)[:,None]
fade=np.clip(t/0.4,0,1)*np.clip((D-t)/1.2,0,1); out*=fade[:,None]
out/=max(1e-9,np.abs(out).max())/0.85
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype('<i2').tobytes()); w.close()
