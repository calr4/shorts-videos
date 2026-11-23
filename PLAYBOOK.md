# Daily Short playbook

How each day's video for the "Build Your Site" YouTube channel is made. This repo is PUBLIC: it holds only the videos, the demo-site source, and the tools. Research notes, the video log and performance numbers are kept elsewhere, never here. Never commit names, emails, locations, client or business details, credentials, or anything else about the channel owner.

## The format
A 15 to 20 second vertical video (1080x1920, 30 fps) that films a real, working website built that day for an invented brand. The site is a single `index.html` with no network requests; all visuals are drawn in code (canvas, CSS, SVG).

Format checklist:
- A striking moving visual in the first second (particles, 3D motion), before any site UI appears.
- A plain-language value hook on screen at 0s, then "Not a video. A website." around 2s.
- A premium product or brand, and a new scene on every scroll step (scrollytelling).
- Proof that it is interactive: a visible tap that changes something.
- A short caption every 2 to 3 seconds, no voiceover, an upbeat beat that starts at 0s.

## Build steps
1. Copy the newest folder in `sites/` as a starting point only for the plumbing (`__film`, `__frame`, captions, tap indicator). The concept, brand, palette, type, layout, and visual technique must be new.
2. Everything on screen must be a pure function of `(t, scrollY)`. No CSS transitions or timers. In normal browsing (no `?film=1`) the same render function runs from `requestAnimationFrame`, so the site is real.
3. Keep captions between 9% and 17% of the height, and all important content above 78% of the height (the Shorts UI covers the bottom and the right edge).
4. `node tools/film.js sites/<folder> stills 0.5,2.5,5,8,11,14` and look at the frames. Fix what is weak: a dim or empty first frame, text overlapping visuals, tiny type, low contrast, a scene that reads as noise. Repeat until every frame would stop a scroll (expect 1 to 3 rounds).
5. `node tools/film.js sites/<folder> video /tmp/scene.mp4`, write a new music bed (see `tools/audio_examples/`, change tempo, key, and pattern each day), then
   `ffmpeg -i /tmp/scene.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart videos/<date>-<slug>.mp4`.
   Keep the file under 40 MB.
6. Pull 4 frames from the finished file and look at them once more before publishing.

## Variety rules
Each video must be clearly different from the last seven in at least three of: industry, visual technique, colour world, hook wording, structure, music. Never reuse a brand name.

## Honesty rules
- Only say what is true: an AI (Claude) built the site from a prompt, no hand-written code. Do not name any other website builder as the tool, and do not make income or price claims beyond the "looks like $X" style hook.
- Invented brands only. No real companies, people, logos, characters, or copyrighted music.
