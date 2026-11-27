# Daily Short playbook

How each day's video for the "Build Your Site" YouTube channel is made. This repo is PUBLIC: it holds only the videos, the demo-site source, and the tools. Research notes, the video log and performance numbers are kept elsewhere, never here. Never commit names, emails, locations, client or business details, credentials, or anything else about the channel owner.

## The format
A 17 to 20 second vertical video (1080x1920, 30 fps) that shows HOW to make a striking website with AI: the result first, then the prompt, then the prompt going into Claude, then the finished site. The site is real and is built that day, from that prompt, for an invented brand. It is a single `index.html` with no network requests; all visuals are drawn in code (canvas, CSS, SVG).

Why this format (owner's instruction, 2026-11-27: study the channels that are winning and use what works): a 2,000-subscriber channel in this exact niche gets 20,000 to 150,000 views per 18-second Short with this structure and the title "How to Make 3D Websites with Claude". Our own plain scrolling-page videos got about 35 views each; our flashy ones got 100 to 1,170. Borrow the structure only. Never copy another creator's footage, wording, site designs, prompts or brand names.

The four beats (keep this order and these timings, within half a second):
1. **Result first, 0 to 4 s.** The most striking part of the finished site, inside the browser frame (slim browser bar with an invented address), already moving in the first frame: a 3D object, particles, a scroll-driven animation. Caption from frame one: "How to make a 3D website like this with AI" (vary the wording daily; always "How to make ... like this").
2. **The prompt, 4 to 7.5 s.** Caption "1. Copy this prompt". A clean card shows the real prompt text (the first lines readable, the rest scrolling past), with a Copy button that the finger dot taps and that changes to "Copied".
3. **Into Claude, 7.5 to 11 s.** Caption "2. Paste it into Claude". A plain chat box drawn by you (the word "Claude" as text, no logo, no imitation of the real app's screen) with the prompt pasted in; the finger taps Send; a short "Building your site..." line.
4. **Done, 11 to end.** Caption "Done. One prompt." then the finished site again in the browser frame, scrolled from top to bottom so it is plainly a real page with real sections and one tap on a working control. Last 2 seconds: "Full prompt in the description. Follow for a new one daily."

Rules that still apply from the owner's earlier feedback:
- A stranger must understand it in the first second: the caption says what this is in plain words, and the browser frame makes it obvious the thing on screen is a website.
- Captions are one idea each, seven words or fewer.
- No voiceover. An upbeat beat that starts at 0 s.

Honesty rules for this format (no exceptions):
- Write the prompt FIRST, as a complete prompt a viewer could paste into Claude. Then build the site by following that prompt and nothing else, so "this prompt made this site" is true. If you change the site afterwards, change the prompt to match.
- The full prompt, word for word as shown, goes in the YouTube description (under 4,000 characters) so "Full prompt in the description" is true. Put a shortened pointer in the Instagram and TikTok captions ("Full prompt on our YouTube").
- Do not say "comment for the prompt" or promise a message or a link: nothing sends them.
- Say "results vary" once in the description: the same prompt gives a similar site, not an identical one.

Cold-viewer check (required before publishing): look at the frames at 0.5 s and 3 s as a stranger. Is this a website? Is it obvious the video will show how to make it with AI? Would you stop scrolling for it? If any answer is no, revise.

## Build steps
1. Take the plumbing (`__film`, `__frame`, browser bar, captions, scrollbar, tap indicator) from `sites/2026-11-25-mooncrust/` or a newer folder, and look at `sites/2026-11-23-solene/` and `sites/2026-11-24-glowtilt/` for how striking 3D and particle scenes were drawn. The prompt card and the chat box are overlays you add for beats 2 and 3. The concept, brand, palette, type, layout and visual technique must be new each day. The concept, brand, palette, type, layout, and visual technique must be new.
2. Everything on screen must be a pure function of `(t, scrollY)`. No CSS transitions or timers. In normal browsing (no `?film=1`) the same render function runs from `requestAnimationFrame`, so the site is real.
3. The browser bar sits in the top 7% of the height. Keep captions between 9% and 17% of the height as a pill over the page, and all important content above 78% of the height (the Shorts UI covers the bottom and the right edge). Draw a scrollbar thumb on the right edge in the upper two thirds of the frame, where the Shorts buttons do not cover it.
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
