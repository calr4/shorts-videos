# AI Tool Drop: daily Short playbook

How each day's video for the "AI Tool Drop" YouTube channel is made. This repo is PUBLIC: it holds only videos, the animated page source, and tools. Never commit names, emails, locations, business details, credentials, research notes, the video log, or performance numbers.

## The format
A 9 to 20 second vertical video (1080x1920, 30 fps) about one AI tool, one comparison, or one short list of tools. It is a single-file animated page (`index.html`, no network requests) filmed with `../tools/film.js`. Everything on screen is drawn in code and is a pure function of time `t`: no CSS transitions, no timers.

Format checklist:
- The hook is fully readable within the first second, as big on-screen text.
- High density: a new piece of information every 1 to 3 seconds. Viewers should want to pause or rewatch.
- No voiceover. A beat that starts at 0 seconds.
- Keep text between 6% and 75% of the height and away from the right 12% (the Shorts UI covers the bottom and the right edge).
- End on the tool's name or a clear takeaway, then "Follow for one AI tool a day".

Formats to rotate: single tool ("this AI does X"), task-to-tool list ("5 free AI tools for X"), free vs paid, before and after, myth vs fact, "what changed this week".

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
