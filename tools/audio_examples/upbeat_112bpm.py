import numpy as np, wave, sys
sr=44100; D=17.0; n=int(sr*D); t=np.arange(n)/sr
f=lambda m: 440*2**((m-69)/12)
L=np.zeros(n); Rr=np.zeros(n)
bpm=112; beat=60/bpm; bar=4*beat
def add(sig, s0, pan=.5, g=1.0):
    i=int(s0*sr); j=min(n,i+sig.size)
    if i>=n or j<=i: return
    L[i:j]+=sig[:j-i]*g*(1-pan)*1.4; Rr[i:j]+=sig[:j-i]*g*pan*1.4
roots=[45,41,48,43]   # Am F C G
chord=[[57,60,64,67],[53,57,60,65],[55,60,64,67],[55,59,62,67]]
drop=1.9  # full beat enters as the bottle forms
# sidechain envelope
sc=np.ones(n)
nb=int(D/beat)+1
for b in range(nb):
    s0=b*beat
    if s0<drop-0.01: continue
    i=int(s0*sr); ln=int(beat*sr); tt=np.arange(min(ln,n-i))/sr
    sc[i:i+tt.size]=0.35+0.65*np.clip(tt/(beat*0.55),0,1)**1.5
# kick
tk=np.arange(int(.28*sr))/sr
kick=np.sin(2*np.pi*(46*tk+(120/22)*(1-np.exp(-tk*22))))*np.exp(-tk*10)+0.25*np.exp(-tk*400)*np.sin(2*np.pi*1800*tk)
# clap/snare
rng=np.random.default_rng(3); tc=np.arange(int(.18*sr))/sr
clap=rng.standard_normal(tc.size); clap=np.diff(clap,prepend=0)*np.exp(-tc*28)*(1+0.8*np.exp(-((tc-.012)/.004)**2))
th=np.arange(int(.05*sr))/sr; hat=np.diff(np.diff(rng.standard_normal(th.size),prepend=0),prepend=0)*np.exp(-th*90)
for b in range(nb):
    s0=b*beat
    if s0>=drop-0.01:
        add(kick,s0,.5,.62)
        if b%2==1: add(clap,s0,.5,.13)
        add(hat,s0+beat/2,.6,.035); add(hat,s0+beat/4,.38,.014); add(hat,s0+3*beat/4,.42,.014)
    else:
        add(hat,s0+beat/2,.6,.02)
# bass + pad + pluck
for bi in range(int(D/bar)+1):
    s0=bi*bar; r=roots[bi%4]; ch=chord[bi%4]
    # pad (sidechained)
    ln=int((bar+.3)*sr); tt=np.arange(ln)/sr; env=np.clip(tt/.25,0,1)*np.clip((bar+.3-tt)/.3,0,1)
    for j,m in enumerate(ch):
        for det,pan in ((-.005,.25),(.005,.75)):
            w=sum(np.sin(2*np.pi*f(m)*(1+det)*h*tt+j*1.3)/h**1.5 for h in (1,2,3,4,5))
            add(w*env,s0,pan,.035)
    if s0+bar>drop:
        # offbeat bass
        for e in range(8):
            b0=s0+e*beat/2
            if b0<drop-.01 or e%2==0: continue
            tb=np.arange(int(.22*sr))/sr
            w=(np.sin(2*np.pi*f(r-12)*tb)+.5*np.sin(2*np.pi*f(r)*tb)+.2*np.sin(2*np.pi*f(r)*2*tb))*np.exp(-tb*7)*np.clip(tb/.006,0,1)
            add(w,b0,.5,.3)
        # 16th pluck arp
        pat=[0,2,3,1,2,3,0,2,3,1,2,3,2,3,1,3]
        for e in range(16):
            b0=s0+e*beat/4
            if b0<drop-.01: continue
            m=ch[pat[e]]+12; tp=np.arange(int(.3*sr))/sr
            w=(np.sin(2*np.pi*f(m)*tp)+.4*np.sin(4*np.pi*f(m)*tp)+.15*np.sin(6*np.pi*f(m)*tp))*np.exp(-tp*11)*np.clip(tp/.003,0,1)
            add(w,b0,.3+.4*(e%2),.075)
L*=sc**0.0+0; Rr*=1
# riser into the drop + impact
rz=np.random.default_rng(9).standard_normal(n); rz=np.diff(rz,prepend=0)
ris=np.where(t<drop,(t/drop)**2.5,0)*rz*0.05
tone=np.where(t<drop,np.sin(2*np.pi*(180*t+ (600/ (2*drop))*t*t))*(t/drop)**2*0.05,0)
L+=ris+tone; Rr+=ris+tone
ti=np.arange(int(1.2*sr))/sr; imp=np.sin(2*np.pi*(38*ti+(60/8)*(1-np.exp(-ti*8))))*np.exp(-ti*3.2)
add(imp,drop,.5,.5)
# chime on "added to bag"
for m,dl in ((81,0),(84,.08),(88,.16),(93,.24)):
    tcn=np.arange(int(1.4*sr))/sr; add(np.sin(2*np.pi*f(m)*tcn)*np.exp(-tcn*3.5),14.24+dl,.5,.07)
out=np.stack([L,Rr],1); fade=np.clip(t/.05,0,1)*np.clip((D-t)/1.0,0,1); out*=fade[:,None]
out=np.tanh(out*1.6)/np.tanh(1.6); out/=np.abs(out).max()/0.9
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype('<i2').tobytes()); w.close()
print('rms',float(np.sqrt((out**2).mean())))
