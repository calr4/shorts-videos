// Films a site folder as a 1080x1920, 30 fps vertical video.
//   node tools/film.js <siteDir> stills [t1,t2,...]   -> <siteDir>/../_stills/*.jpg
//   node tools/film.js <siteDir> video <out.mp4>      -> silent H.264 file
// The site must define, when opened with ?film=1:
//   window.__film  = { duration: seconds, keys: [[time, fractionOfMaxScroll], ...] }
//   window.__frame = function (t, scrollY) { ...set scroll, fire timed taps, render everything for time t... }
// Everything on screen must be a pure function of (t, scrollY): no CSS transitions, no real-time clocks.
const path = require('path'), fs = require('fs'), { spawn } = require('child_process');
let chromium;
try { ({ chromium } = require('playwright')); } catch (e) { ({ chromium } = require('/opt/npm-tools/node_modules/playwright')); }
const FPS = 30;
const smooth = (x) => { x = Math.max(0, Math.min(1, x)); return x * x * x * (x * (x * 6 - 15) + 10); };
(async () => {
  const site = path.resolve(process.argv[2]), mode = process.argv[3] || 'stills';
  const exe = ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find((p) => fs.existsSync(p));
  const browser = await chromium.launch({ executablePath: exe, args: ['--no-sandbox', '--font-render-hinting=none'] });
  const page = await browser.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(site, 'index.html') + '?film=1');
  await page.evaluate(() => document.fonts.ready);
  const film = await page.evaluate(() => ({ ...window.__film, end: document.documentElement.scrollHeight - innerHeight }));
  const keys = film.keys.map(([t, f]) => [t, f * film.end]), N = Math.round(film.duration * FPS);
  const yAt = (t) => { for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) { const [t0, y0] = keys[i - 1], [t1, y1] = keys[i]; return y0 + (y1 - y0) * smooth((t - t0) / (t1 - t0)); } return keys[keys.length - 1][1]; };
  const step = (t) => page.evaluate(([t, y]) => window.__frame(t, y), [t, yAt(t)]);
  if (mode === 'stills') {
    const dir = path.join(site, '..', '_stills'); fs.mkdirSync(dir, { recursive: true });
    const want = (process.argv[4] || '').split(',').filter(Boolean).map(Number);
    for (let f = 0; f < N; f++) {            // walk every frame so timed taps fire in order
      const t = f / FPS; await step(t);
      if (want.some((w) => Math.abs(w - t) < 0.5 / FPS)) await page.screenshot({ path: path.join(dir, `t${t.toFixed(1)}.jpg`), type: 'jpeg', quality: 88 });
    }
    console.log('stills in', dir);
  } else {
    const fin = path.resolve(process.argv[4]), tmp = fin.replace(/\.mp4$/, '.tmp.mp4');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-vf', 'format=yuv420p', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium', '-maxrate', '9M', '-bufsize', '18M', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
    const done = new Promise((res) => ff.on('exit', res));
    for (let f = 0; f < N; f++) {
      await step(f / FPS);
      const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    if ((await done) === 0) { fs.renameSync(tmp, fin); console.log('ok', fin); } else { console.log('ffmpeg failed'); process.exitCode = 1; }
  }
  await browser.close();
})();
