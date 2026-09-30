# alexdong.vercel.app — design notes

A personal site for Alex Dong, CS student at Columbia. One HTML file, no framework. The look is borrowed from
[aino.agency](https://aino.agency): everything sits on a monospace character grid, and the images are made of text.

## The idea

- **Text is the medium.** The intro, the logo, the portrait and every project image are characters redrawn each
  frame in the page's own font. Nothing is a picture of ASCII art; it is ASCII art.
- **Aino's grid, our content.** The intro sequence, the glyph ramp (`NO0A869452I3?!<>=+/:-·`), the 8 × 16 px
  cell and the "resolve out of noise" reveal were reverse-engineered from aino's site. Everything on top of that
  is Alex's: his projects, his own ASCII drawings, a real clip of him waving.
- **The ASCII figure is the star.** Every layout decision on the landing page was made so the waving figure
  draws the eye first and the name second.
- **Quiet, not loud.** Two fonts, one accent colour, light mode only, no counters or decorative numbering, no
  dark mode. Emphasis comes from size and space, not from ornament.
- **One file.** `index.html` carries the CSS, the engine and the baked sprite of the figure, so it works from
  `file://` and deploys as a single static asset. Pages are hash routes inside it.

## Grid and spacing

- The page is laid out on the mono font's cell: `--ch` (one character advance, measured at load) × `--line`
  (16 px). Every margin, gutter and padding is a multiple of those two units, like a terminal.
- Content is a four-column grid with a two-character gutter; the landing page uses a 1.15 / 0.85 split (text /
  figure) and mobile stacks to one column.
- The landing page must never scroll: the figure stretches to fill exactly the space between the nav and the
  footer.

## Colour

Aino's palette, adopted as-is: a near-black ground and off-white ink, for the text and the ASCII alike.

| role   | value              | use                                                                |
| ------ | ------------------ | ------------------------------------------------------------------ |
| ground | `rgb(24,24,24)`    | background, dark grey rather than pure black                       |
| ink    | `rgb(245,245,240)` | text, the ASCII figure, the art tiles, the intro                   |
| accent | `#6FA8FF`          | sky blue: one word per page ("Columbia"), the active nav item, awards, hover |
| muted  | ink at 45–60 %     | small labels only: "HI, I'M", captions under tiles, technology pills, field labels |

Running text is full ink, not grey: the About prose, the photo captions and the project descriptions all read at
100 %. Only small labels step down. The ASCII figure and the art tiles are drawn at full white with a hairline
text stroke, because 6–9 px glyphs otherwise anti-alias to grey on a dark ground.

The accent was burnt orange (`#D4501E`, lifted to `#F26B3A` for the dark ground) until seven candidates were
compared on the real pages; sky blue won over lime, yellow, Columbia blue, mint and a monochrome white. A faint
film-grain overlay (7 %, screen blend) sits over everything. One scheme only: there is no light/dark toggle.
(The site began on a warm off-white paper, `#F2F0EA` with `#161616` ink, and was switched to aino's dark scheme
at Alex's request.)

## Type

Two families, standardised late in the process after trying a serif:

- **Familjen Grotesk 700** for headlines and big text only: the About headline, project titles, the Contact
  headline, the mobile menu. Tight letter-spacing (−0.03 em). This is the "aino headline" voice.
- **Geist Mono** for everything else: nav, labels, body copy, project descriptions, captions, pills, buttons.
  Uppercase for labels and navigation; sentence case for running text.

Sizes that were argued over and settled:

- Body copy: mono 15.6 px on 24 px lines, full ink (12 px was "tiny"; 80 % ink read as grey on the dark ground).
- Project descriptions: 13.2 px on 20 px lines (asked for smaller twice).
- Landing "HI, I'M": 13.2 px uppercase, 60 % ink. Tagline "A CS STUDENT AT COLUMBIA": 16.8 px uppercase,
  0.08 em tracking.
- Newsreader (an italic serif) was tried for the About headline and the landing tagline and removed; the site
  now uses only the two families above.

## The intro

Runs on first load of the session (`Esc` skips; `prefers-reduced-motion` and `#nointro` skip it entirely;
the ◆ mark in the nav replays it).

1. A `=` loading bar draws across the top line and morphs into the nav text, exactly where the real nav sits.
2. A mouse-reactive field of glyphs breathes in the middle of the screen with "CLICK" following the pointer.
3. Click: every glyph falls, explodes, and reassembles into a big ASCII **ALEX** with a slow wave through it.
4. Click again (or wait): the big ALEX collapses into the small ALEX inside the landing headline, and the page
   reveals around it.

## Landing page

Left column, the lockup (chosen from 34 mockups, see "How we got here"):

```
HI, I'M                      mono, small, muted
ALEX                         ASCII stamp, ~4.6× the cap height, 27 rows of cells
A CS STUDENT AT COLUMBIA     mono, Columbia in the accent
[ABOUT ME →] [ALL PROJECTS →]
```

- The whole block is nudged in from the margin by two characters so it does not hang on the same edge as the
  nav's "ALEX DONG".
- The ALEX stamp is live: the same glyph ramp as the intro, with a wave running through it. It is sized from
  the headline's cap height and capped to the column width so it shrinks on phones. It is 20 rows of 6 px
  characters, each no taller than its row, at weight 600 with no stroke: dense enough to read as ALEX from
  across the room, open enough that you can see it is made of `0`, `N`, `A`, `/` and `<` up close. (Finer,
  bolder, stroked settings were tried and read as a solid block with hatching.)

Right column, the figure:

- A real clip of Alex waving, cut out of its room (outlets, cable, jugs, baseboard, floor removed) and baked
  into a 77-frame sprite of character cells at 14.5 fps, embedded in the page. It plays over an even field of
  `·` dots, the way aino's portraits do, and resolves out of noise when the page reveals.
- The loop is idle → raise → wave → lower → rest, cut so the seam is invisible; he is centred on his torso, and
  the figure fills the viewport height.
- A drawn cartoon was the first version and was rejected as "robotic": the realism has to come from footage.

## Navigation and chrome

- Nav: name left, `ABOUT · WORK · CONTACT` centred, `◆ ALEXDONG` right (replays the intro). The role line
  ("CS Student + Engineer") was removed. On phones: name and a Menu button that opens a full-screen list.
- Footer: name left, local time right. Nothing else.
- Page heads are just "◆ About me" / "◆ Work" / "◆ Contact": no section numbers, no item counts.

## Work

- Each project is a row: a 4:3 ASCII art tile on the left, then title / description / award, with a quiet
  footer line pinned to the tile's bottom edge: technology pills on the left, links on the right.
- The art is Alex's own ASCII drawings, animated: a rotating panopticon for Opticon, the Mooodboard "m", the
  Kalshi K and Polymarket P with flow arrows, and the fixed-wing plane releasing the delivery drone. They only
  animate while on screen.
- Hierarchy the page is built around: art + name + description first, technologies + links second.

## About

- Headline "I love building, music, and *random quests*." in the grotesk, one paragraph of mono prose ending in
  a link to Contact, four capitalised bullets (Piano, Filming things, Weightlifting, Tennis & basketball).
- A masonry photo grid at the bottom (three columns, two on tablets, one on phones), photos and short clips with
  one short mono caption each. No ASCII portrait or skills sidebar here; that was cut.

## Contact

- "Reach out *to me!*" as a full-width headline (accent on "to me!"), then the form on the left (Name /
  Email / Message, hairline fields, solid Send) and the links on the right (email, GitHub, LinkedIn, Resume)
  as arrow rows.
- The form posts to FormSubmit, so there is no backend; messages land in Alex's Gmail.

## Motion and interaction rules

- **Hover glitch**, aino-style: only the two or three characters under the pointer scramble through the glyph
  ramp, never the whole word, and the word never changes width. Project titles are the exception: the whole
  title glitches once on enter and once on leave.
- Section content fades up and labels scramble in when a page is shown. Reveals are staggered, not scattered.
- Animations run only for things in view and stop for `prefers-reduced-motion`.
- Buttons: boxed mono caps with an arrow that slides on hover; the primary one is solid ink, and turns accent on
  hover.

## Responsive

- Under 768 px: single column, figure below the headline, no landing nudge, tagline eases to 15 px, hamburger
  menu. The ALEX stamp caps itself to the column width.
- The figure's cell size is derived from the available height, so the figure is the same person at every size,
  just with more or fewer dots around him.

## How we got here (decisions and rejections)

- Started as a long single-scroll page with hero, projects, skills, about and contact. Split into separate
  hash-routed pages for a minimal landing.
- The theme toggle was removed early and the site stayed on warm off-white paper for weeks; then Alex asked for
  aino's own scheme (near-black ground, off-white text and ASCII) and the whole site was flipped to it. Still
  one scheme, no toggle.
- "Skills" page merged into About, then the skills sidebar and ASCII portrait removed entirely.
- The ALEX headline went through: same size as the text → 1.5× → 2× → 5× on one line with "I'm" → then a round
  of 34 mockups. Kept from that round: a small "HI, I'M" over the name (from the "monument" layout), ALEX big but
  not column-filling, the tagline well under ALEX's height and about its width, the boxed buttons, the block
  nudged slightly right. Rejected: the hairline rule under ALEX, the "New York · 2026" line, the serif italic
  (Newsreader, Cormorant Garamond, Fraunces, Bodoni Moda were all tried), links on the eyebrow line, mirrored
  columns, and the 8-character nudge (too far).
- Project rows went 3-column → 2-column → 3-column → the current 2-column with a pinned footer line; chips were
  removed for a mono list and then brought back as pills so they read differently from links.
- The figure: cartoon → footage renderer → pre-baked sprite. Ground tufts under his feet were removed ("just
  regular dots"); a cross-fade that showed two arms for a frame was cut so it only blends frames where the arm
  is already down.
- Counters ("004 entries", "01 human") and section numbers were removed.

## Tooling

- `tools/ascii-wave/`: `bake.py` turns `IMG_4547.mov` into the sprite (segmentation, loop cut, tone curve),
  `wire.py` embeds it into `index.html`. Neither the tools folder nor the raw clip is deployed.
- `tools/mockups/build.py`: generates `mockups.html`, the landing page in every layout that was considered,
  built from the live `index.html` so each mockup is exactly what the site would render. Not deployed.
- Deploy: push to `main` (Vercel GitHub integration) or `vercel --prod` from this folder.
