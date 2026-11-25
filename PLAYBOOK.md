# Daily Short playbook

How each day's video for the "Build Your Site" YouTube channel is made. This repo is PUBLIC: it holds only the videos, the demo-site source, and the tools. Research notes, the video log and performance numbers are kept elsewhere, never here. Never commit names, emails, locations, client or business details, credentials, or anything else about the channel owner.

## The format
A 15 to 20 second vertical video (1080x1920, 30 fps) that films a real, working website built that day for an invented brand. The site is a single `index.html` with no network requests; all visuals are drawn in code (canvas, CSS, SVG).

The owner's two standing rules (given 2026-11-25 after watching the videos; they outrank the brief, the experiment and everything else in this file):
1. A stranger must understand the video in the first second.
2. It must look like a website, not an animation or a game.

Format checklist:
- **It reads as a web page being used.** A slim browser bar stays at the top for the whole video (back arrow, a lock, an address pill with an invented address such as `thimbleandowl.example`). Under it is a normal page: a menu bar with a logo and links, a headline with a button, then ordinary sections (products or menu with prices, reviews, opening hours or contact, a footer).
- **The page visibly scrolls.** For at least two thirds of the video the content moves up the screen as one long page, at a pace a person would scroll, with a scrollbar thumb moving down the right edge. Do not replace scrolling with scene changes, page flips, or a camera flying through a 3D scene.
- **Effects live inside the page.** Things may animate, tilt, light up or assemble as they scroll into view, and one section may be a showpiece (3D product, a small game, particles). The showpiece takes at most a third of the video and the page must scroll into it and out of it, so it is clearly part of a page.
- **The first second explains everything in plain words.** The first caption says what this is and who it is for, for example "AI built this website for a bookshop." No series numbers, no in-jokes, nothing that needs an earlier video. The page behind it already shows the browser bar, the menu and the headline.
- **Captions say what the viewer is looking at.** One idea each, seven words or fewer, a new one every 2 to 3 seconds: "This is the real page", "Scroll down to the menu", "The buttons work", "Built by AI. No code typed by hand."
- **Proof that it is interactive:** a visible tap (finger dot) on a real control such as a menu link, a button or a form, and the page responds.
- **End on the whole page:** zoom out for the last 1.5 seconds so the full length of the page is visible top to bottom, with "Follow for a new AI-built site every day".
- No voiceover. An upbeat beat that starts at 0s.

Cold-viewer check (required before publishing): look at the frames at 0.5 s and 3 s and answer three questions as a stranger who has never seen the channel. Is this a website? Did AI make it? What business is it for? If any answer is not obvious, revise.

## Build steps
1. Copy the newest folder in `sites/` as a starting point only for the plumbing (`__film`, `__frame`, captions, tap indicator). The concept, brand, palette, type, layout, and visual technique must be new.
2. Everything on screen must be a pure function of `(t, scrollY)`. No CSS transitions or timers. In normal browsing (no `?film=1`) the same render function runs from `requestAnimationFrame`, so the site is real.
3. The browser bar sits in the top 7% of the height. Keep captions between 9% and 17% of the height as a pill over the page, and all important content above 78% of the height (the Shorts UI covers the bottom and the right edge). Draw the scrollbar thumb on the left of the right-hand 12% so the Shorts buttons do not cover it.
4. `node tools/film.js sites/<folder> stills 0.5,2.5,5,8,11,14` and look at the frames. Fix what is weak: a frame that does not look like a web page, a first frame a stranger would not understand, a dim or empty first frame, text overlapping visuals, tiny type, low contrast, a scene that reads as noise. Repeat until every frame would stop a scroll (expect 1 to 3 rounds).
5. `node tools/film.js sites/<folder> video /tmp/scene.mp4`, write a new music bed (see `tools/audio_examples/`, change tempo, key, and pattern each day), then
   `ffmpeg -i /tmp/scene.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart videos/<date>-<slug>.mp4`.
   Keep the file under 40 MB.
6. Pull 4 frames from the finished file and look at them once more before publishing.

## Variety rules
Each video must be clearly different from the last seven in at least three of: industry, visual technique, colour world, hook wording, structure, music. Never reuse a brand name.

## Honesty rules
- Only say what is true: an AI (Claude) built the site from a prompt, no hand-written code. Do not name any other website builder as the tool, and do not make income or price claims beyond the "looks like $X" style hook.
- Invented brands only. No real companies, people, logos, characters, or copyrighted music.

## Music rule (no exceptions)
Every music bed is generated from scratch in code during the run (synthesised tones and drums, as in `tools/audio_examples/`). Never use an existing song, a sample, a library loop, a cover, a melody copied from or closely following a known song, a platform's trending sound, or music from a generator service. If original music cannot be made, publish the video silent. Do not add music inside TikTok or Instagram.
