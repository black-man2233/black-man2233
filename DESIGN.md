---
name: Kevin's living room (GitHub profile)
description: A GitHub profile README that is a window into Kevin's living room, with his projects listed on a smoked-glass directory board on the carpet.
colors:
  autumn: "#F97316"
  autumn-text: "#FDBA74"
  lamp-amber: "#FFB46B"
  wall: "#3A2416"
  wall-dark: "#2A190F"
  wood: "#7A4A28"
  wood-light: "#9C6538"
  wood-dark: "#4E2E18"
  carpet: "#1A2744"
  carpet-deep: "#121C33"
  board-glass: "rgba(20, 27, 46, 0.62)"
  dock-top: "#26324F"
  dock-bottom: "#18213A"
  screen: "#1A1F2E"
  screen-deep: "#0C0F18"
  cream: "#F6ECDD"
  cream-2: "#C9B9A3"
  cream-3: "#A08F7A"
  rim: "#FFF0DC"
  rule: "rgba(246, 236, 221, 0.12)"
  leader: "rgba(246, 236, 221, 0.24)"
typography:
  display:
    fontFamily: "Archivo (set as outlines)"
    fontSize: "66px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.08em"
    fontVariation: "'wdth' 112"
  suite:
    fontFamily: "Archivo (set as outlines)"
    fontSize: "33px"
    fontWeight: 450
    lineHeight: 1
    letterSpacing: "-0.02em"
    fontFeature: "'tnum'"
    fontVariation: "'wdth' 112"
  title:
    fontFamily: "Archivo (set as outlines)"
    fontSize: "21px"
    fontWeight: 500
    fontVariation: "'wdth' 100"
  body:
    fontFamily: "Archivo (set as outlines)"
    fontSize: "16px"
    fontWeight: 450
    fontVariation: "'wdth' 100"
  label:
    fontFamily: "Archivo (set as outlines)"
    fontSize: "14px"
    fontWeight: 700
    letterSpacing: "0.16em"
    fontVariation: "'wdth' 125"
  meta:
    fontFamily: "Archivo (set as outlines)"
    fontSize: "14px"
    fontWeight: 500
    letterSpacing: "0.02em"
    fontVariation: "'wdth' 100"
rounded:
  screen: "12px"
  window-compact: "20px"
  window: "24px"
  board-compact: "24px"
  board: "30px"
  pill: "22px"
spacing:
  inset-compact: "20px"
  board-pad-compact: "30px"
  board-pad-top: "34px"
  inset: "36px"
  board-pad: "40px"
  floor-gap: "40px"
  row: "56px"
  column-gap: "56px"
components:
  room-window:
    backgroundColor: "{colors.wall}"
    rounded: "{rounded.window}"
    width: "1000px"
  room-window-compact:
    backgroundColor: "{colors.wall}"
    rounded: "{rounded.window-compact}"
    width: "600px"
  directory-board:
    backgroundColor: "{colors.board-glass}"
    textColor: "{colors.cream}"
    rounded: "{rounded.board}"
    padding: "34px 40px 30px"
  directory-board-compact:
    backgroundColor: "{colors.board-glass}"
    textColor: "{colors.cream}"
    rounded: "{rounded.board-compact}"
    padding: "34px 30px"
  directory-row:
    textColor: "{colors.cream}"
    typography: "{typography.title}"
    height: "{spacing.row}"
  floor-head:
    textColor: "{colors.cream}"
    typography: "{typography.label}"
  tv-title:
    backgroundColor: "{colors.screen}"
    textColor: "{colors.cream}"
    typography: "{typography.display}"
    rounded: "{rounded.screen}"
  dock-segment:
    backgroundColor: "{colors.dock-top}"
    textColor: "{colors.cream}"
    width: "52px"
    height: "44px"
  dock-cap:
    backgroundColor: "{colors.dock-top}"
    rounded: "{rounded.pill}"
    width: "24px"
    height: "44px"
  stats-card:
    backgroundColor: "{colors.carpet}"
    textColor: "{colors.cream-2}"
    rounded: "{rounded.window}"
---

# Design System: Kevin's living room (GitHub profile)

## Overview

**Creative North Star: "The Window Into the Living Room"**

The profile is not a page of widgets; it is a set of framed windows onto one warm room. The top window shows the wood-panelled wall with the lamp, the TV that reads KEVIN, speakers, the console stand and the vinyl corner; the carpet below holds a smoked-navy glass directory board listing his real projects by floor (Backend, Frontend, Games). The stats cards sit on the same carpet colour, the dock of socials floats as a glass pill, and the lounge window closes the page at the sofa. The world is inherited from homeserverdash and adapted to a medium with no CSS and no JS.

GitHub's Markdown sanitizer is the defining constraint. Everything the world needs is baked into committed SVG files that `scripts/build_profile.py` generates, with every letter converted to Archivo outlines, so no font loading, no stylesheet and no theme switching can change what renders. Markdown contributes only layout glue: a centred `div`, `<picture>` for the mobile variant, and `<img>` tags.

Density is calm and directory-like: ruled hairlines, dotted leaders, big tabular years, expanded caps for signage. One thing moves.

**Key Characteristics:**
- One warm theme: wood wall, navy carpet, cream lettering, lamp amber, an autumn-orange backlight.
- Every visual is a generated SVG; text is Archivo outlines, never live text.
- Each image is an opaque, rounded, self-contained window that reads the same on GitHub light and dark.
- Content is a directory (hairlines, dotted leaders, tabular numerals), not a card grid or badge wall.
- The spinning record is the only motion.
- Desktop (1000 wide) and compact (600 wide, one column) variants of each scene, switched by `<picture media="(max-width: 640px)">`.

## Colors

Warm wood above, cool navy below, cream on both, with orange used as light rather than as paint.

### Primary
- **Autumn Backlight** (autumn): the TV halo behind KEVIN, the screen wash, and the stats rank and streak rings. It glows; it never fills a surface.
- **Autumn Text** (autumn-text): the one tinted word on the TV, the expanded-caps BACKEND label; also the streak card's current-streak label.

### Secondary
- **Lamp Amber** (lamp-amber): the floor lamp's light pool, the faint warm wash at the top of the board, and the icon colour in the stats card. Ambient light only.

### Tertiary

### Neutral
- **Panelled Wall** (wall, wall-dark): vertical wall gradient, dark at the ceiling, with 64px plank seams and faint 9px grain.
- **Oak Wood** (wood, wood-light, wood-dark): stand top, shelf, table legs, baseboard family.
- **Navy Carpet** (carpet, carpet-deep): the floor gradient with a near-invisible 6px weave; also the background of every third-party stats card.
- **Smoked Board Glass** (board-glass): the directory board, carpet showing through, with a cream rim stroke and a soft drop shadow outside its edge only.
- **Dock Navy** (dock-top, dock-bottom): the dock pill's vertical gradient, with rim highlights in rim cream.
- **Screen Black** (screen, screen-deep): TV panel.
- **Cream Lettering** (cream, cream-2, cream-3): primary text and names, secondary text (subtitles, toolbox, fact line, stats body), tertiary metadata (languages, counts, floor notes).
- **Rule and Leader** (rule, leader): 1px etched rules under floor heads and above the toolbox; dotted leaders between a project and its year.

### Named Rules
**The Light Not Paint Rule.** Autumn and amber appear as glows, halos, rings and one label word. No surface is filled orange.

**The Same Room Rule.** Third-party cards are themed onto the carpet through their URL params (carpet background, cream title and text, amber icons, autumn rings, 24px radius, no border). A widget that cannot take these colours does not ship.

## Typography

**Display Font:** Archivo variable (`scripts/src/archivo-wdth.woff2`, OFL), converted to SVG paths by the generator's HarfBuzz typesetter.
**Body Font:** the same Archivo, normal width.

**Character:** One family, two widths. Expanded caps (wdth 125, 0.16em tracking) is signage; normal width is people and project names. Sizes below are SVG user units in the 1000-wide desktop scenes; GitHub scales them to the column (about 0.83x on desktop).

### Hierarchy
- **Display** (600, 66, wdth 112, 0.08em): KEVIN on the TV only, cream over an autumn blurred halo copy at 0.55 opacity.
- **Suite** (450, 33, wdth 112, -0.02em, tabular): project years, right-aligned at the end of each leader.
- **Title** (500, 21): project names in the directory.
- **Body** (450, 14 to 16): the TV subtitle and the lounge fact line, cream-2, centred.
- **Label** (700, 14 to 15, wdth 125, 0.16em, uppercase): floor heads, TOOLBOX, the TV's BACKEND label, the lounge motto.
- **Meta** (500, 14, 0.02em): language after a name, floor notes, floor counts (tabular), toolbox items (450).

Compact scenes raise every size (label 17, title 25, meta 17, suite 38, body and motto 22) so text survives a phone-width column.

### Named Rules
**The Outlines Only Rule.** Text in the art is set as Archivo glyph outlines (`<use>` references into shared path defs), never `<text>`. GitHub serves SVGs through `<img>`, where web fonts do not load.

**The Two Widths Rule.** Expanded caps label things; normal width names things. Never set a project name in expanded caps, never set signage in normal width.

## Layout

The README is a single centred column. Order: room window, stats block (stats at width 371 and top-languages at 439 side by side, sized so both render ~146px tall; streak full width at 814 below; on phones top-languages and streak swap to narrower `card_width` variants via `<picture>`), snake, dock, lounge window. Sections are separated by two `<br />`.

The room is 1000 wide: wall to y 440, a 12px baseboard, then carpet. The board is inset 36 on each side, 52 below the floor line, padded 40 horizontally and 34 at the top, with two columns 56 apart split by a 1px cream rule at 0.1 opacity. Backend fills the left column; Frontend and Games stack on the right, 40 apart. Rows are 56 tall; the toolbox plaque spans the full width below both columns.

The compact variant is 600 wide, inset 20, padded 30, one column of floors with the toolbox wrapped, rows 64. The lamp and speakers are dropped; the TV, stand, pads and vinyl corner stay. Every full-width scene has a compact twin chosen by `<picture><source media="(max-width: 640px)">`; the top-languages card does the same.

### Named Rules
**The Twin Scene Rule.** A scene ships as a 1000-wide and a 600-wide SVG from the same generator functions. The compact one is recomposed, not scaled down.

## Elevation & Depth

Depth is drawn into the illustration: soft drop shadows under objects, light pools, and tonal gradients. Nothing in Markdown carries a shadow.

### Shadow Vocabulary
- **Soft** (`feDropShadow dy 14, blur 12, black 0.45`): TV, speakers, stand, sofa, coffee table, the board (masked so it falls outside the glass only).
- **Small** (`feDropShadow dy 6, blur 4, black 0.45`): pads, turntable, record sleeves, shelf top.
- **Dock lip** (3px black at 0.16 under the pill): the dock's only lift.

### Named Rules
**The Shadow Stays Outside Rule.** Glass surfaces cast their shadow through a mask so the carpet seen through the board is never darkened.

## Shapes

Every image is a rounded window: clipped to 24 (desktop) or 20 (compact), and the stats cards match with `border_radius=24`. The board is softer than its window (30 desktop, 24 compact). The dock is a full pill (44 tall, 22 radius ends). Furniture uses small radii (3 to 12); the TV bezel is 12. Rules are 1px; leaders are round dots (dasharray 0.1 5, width 1.4).

## Components

### Room Window
Self-contained, opaque, rounded scene. The wall, carpet and board are painted edge to edge inside the clip, so the GitHub page colour never shows through and both themes see the same room.

### Directory Board
Smoked glass at 0.62 over the carpet, a top-down amber wash fading by 35%, a diagonal cream rim (0.42 to 0.08 to 0.16). Each floor: dot, expanded-caps title, normal-width note in cream-3, tabular count right-aligned, then a double hairline (cream 0.12 over white 0.03). Each row: name, language, dotted leader, year. Closes with the TOOLBOX plaque, items joined by spaced middle dots.

### TV
Black bezel (rx 12), screen gradient with an autumn wash from the top and a pale diagonal glare. KEVIN in display; below it BACKEND in autumn-text label caps followed by "C# / .NET" in cream; then the subtitle in cream-2. A broad autumn glow sits on the wall behind the set.

### Dock
A liquid-glass pill of socials built from separate images: `dock-left.svg` (24 wide cap), one 52-wide segment per platform with a 20px cream icon at 0.9, and `dock-right.svg`. Hairline dividers sit before Email and before Ko-fi, grouping social, contact and support. Each segment is its own link with `title` and `alt`; the caps are `alt=""` and live inside the first and last anchors.

### Stats Cards
github-readme-stats and streak-stats themed through URL params onto the carpet (see The Same Room Rule), `hide_border=true`, `border_radius=24`. Top languages hides only HTML and CSS; the data is shown as it is.

### Turntable
The vinyl corner's platter (`.platter`) rotates once every 1.8s, linear, infinite, and stops under `prefers-reduced-motion: reduce`. Larry June and Kanye West sleeves lean against the shelf.

### Named Rules
**The Seamless Dock Rule.** All dock `<a>` and `<img>` tags sit on one line with no whitespace between them. Any space or newline renders as a gap and splits the pill.

**The One Motion Rule.** The turntable is the only animated element in the profile, and it stops under reduced motion. The snake is a separate, external artifact.

## Do's and Don'ts

### Do:
- **Do** change the art by editing `scripts/build_profile.py` and regenerating; the generator is the source of truth.
- **Do** build every new scene as an opaque rounded window (24 desktop, 20 compact) so it reads identically on GitHub light and dark.
- **Do** ship a 600-wide compact twin for every full-width scene and switch it with `<picture media="(max-width: 640px)">`.
- **Do** set all art text as Archivo outlines through the Typesetter, expanded caps for signage and normal width for names.
- **Do** theme any third-party card onto the carpet with cream text and autumn or amber accents via its URL params.
- **Do** keep the social links pointing at the platform homepages (and the empty `mailto:`) until Kevin fills in his handles.
- **Do** write a full alt text on each scene image that carries every word the art shows.

### Don't:
- **Don't** hand-edit anything in `assets/`; the next generator run overwrites it.
- **Don't** use `<text>` or reference a web font in the SVGs.
- **Don't** add a light/dark variant or a second theme for the art.
- **Don't** put whitespace or line breaks between dock segments.
- **Don't** add a second animation; the turntable is the only motion and must keep its reduced-motion stop.
- **Don't** invent social handles or drop the dock links.
- **Don't** fill a surface with autumn orange or lamp amber.
- **Don't** put coloured dots or glowing markers before titles. Kevin rejected them (2026-10-15); floor heads are plain expanded caps.
- **Don't** return to the README kit: capsule wave banners, typing SVGs, badge walls, quote cards, tokyonight-themed cards.
