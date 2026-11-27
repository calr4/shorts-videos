# AI Tool Drop: daily Short playbook

How each day's video for the "AI Tool Drop" YouTube channel is made. This repo is PUBLIC: it holds only videos, the animated page source, and tools. Never commit names, emails, locations, business details, credentials, research notes, the video log, or performance numbers.

## The format
A 14 to 18 second vertical video (1080x1920, 30 fps) in the series **"Free AI website you should know (Part N)"**. It is a single-file animated page (`index.html`, no network requests) filmed with `../tools/film.js`. Everything on screen is drawn in code and is a pure function of time `t`: no CSS transitions, no timers.

Why this format (owner's instruction, 2026-11-27: study the channels that are winning and use what works): a faceless channel has reached Part 207 of a "Powerful website you should know" series with 14-second Shorts that get around 90,000 views; a silent "type this, get that" Short reached 377,000. Both show the result first, then where to go, then what to do, then the result again. Borrow the structure only. Never copy another creator's footage, wording, tool picks in the same order, or series name.

The five beats (keep this order):
1. **Result first, 0 to 2.3 s.** Headline "Free AI website you should know" with a "PART N" tag, and the tool's result already happening on screen (the before turning into the after).
2. **Where, 2.3 to 5 s.** "1. Go to <address>" with the address typed into a plain browser bar.
3. **Do, 5 to 8.6 s.** "2. <the one thing you do>", shown being done with the finger dot.
4. **What the AI does, 8.6 to 12.6 s.** "3. <what it does>", then the result again, bigger.
5. **Proof and follow, 12.6 s to end.** Three or four short facts taken from the maker's page (free, nothing to download, which devices, who made it), then "Follow for Part N+1" and the tool's name large.

Rules:
- Pick tools that are free to use, run in a browser, and give a result you can SEE in two seconds (drawing, images, sound, a visible transformation). Skip tools whose result is a wall of text.
- The Part number goes up by one each day; the Video log has the last number. Part 1 was AutoDraw (2026-11-27), in `aitooldrop/sites/2026-11-27-autodraw/`, which is the reference for the layout and timing.
- A stranger must know in the first second what the tool does: the result is on screen in the first frame.
- One idea per screen, in short everyday words. Keep text between 6% and 75% of the height and away from the right 12%.
- The interface is your own drawing, labelled "Illustration. Not the real screen." Never imitate a real product's screen, logo or mascot.
- No voiceover unless the owner turns one on. A beat that starts at 0 seconds.
- Never use fake urgency ("deleting this in 2 hours"), invented stories, or "comment for the link": nothing sends a link.
- Cold-viewer check (required before publishing): look at the frames at 0.5 s and 3 s as a stranger. Which tool is this? What does it do for me? Would I stop scrolling? If any answer is no, revise.

## Accuracy rules (the channel's reputation depends on these)
- Every claim about a tool (what it does, its name, whether it is free, limits, price) must be checked the same day on the tool maker's own website or help pages, by opening the page. A search snippet or a blog is not enough.
- If the maker does not publish a number, do not state it. Say "limits apply" instead.
- Tool names and plans change often. Use the current name, and add "(formerly ...)" when the old name is better known.
- Put "Details checked <Month Year> and may change" in the description.

## Fairness rules
- This channel is produced by Claude, an AI assistant made by Anthropic. Do not give the channel's own verdict ranking Claude or Anthropic products against competing assistants, in either direction. Comparisons between assistants state checkable facts only (price, limits, features), each sourced.
- Say "Not sponsored" in the description unless the owner has added an affiliate link for that tool. If there is one, disclose it in the description and on screen.
- No income promises, no "get rich" framing, no fake urgency.

## Look and brand rules
- Do not draw any company's logo, mascot, or app icon, and do not imitate a real product's screen. Show ideas with abstract shapes, icons you draw yourself, and text. Tool names appear as plain text.
- Each video must be clearly different from the last seven in at least three of: tool category, format, colour world, hook wording, layout, music.

## Build steps
1. Copy the newest folder in `aitooldrop/sites/` only for the plumbing (`__film`, `__frame`, scene timing). The concept, layout, and palette must be new.
2. `node tools/film.js aitooldrop/sites/<folder> stills 0.5,3,6,9,12` and look at the frames. Fix overlaps, cut-off text, weak first frames, and anything hard to read at a glance. Expect 1 to 3 rounds.
3. `node tools/film.js aitooldrop/sites/<folder> video /tmp/scene.mp4`, write a new music bed (see `tools/audio_examples/`, change tempo, key, and pattern each day), then
   `ffmpeg -i /tmp/scene.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart aitooldrop/videos/<date>-<slug>.mp4`.
   Keep the file under 40 MB.
4. Pull 4 frames from the finished file and look at them once more before publishing.

## Music rule (no exceptions)
Every music bed is generated from scratch in code during the run (synthesised tones and drums, as in `tools/audio_examples/`). Never use an existing song, a sample, a library loop, a cover, a melody copied from or closely following a known song, a platform's trending sound, or music from a generator service. If original music cannot be made, publish the video silent. Do not add music inside TikTok or Instagram.
