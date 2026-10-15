# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

GitHub profile README (`README.md` in the `black-man2233/black-man2233` repo), rendered by GitHub's Markdown sanitizer. No custom CSS, no JS, limited HTML (`<div align>`, `<img>`, `<picture>`, `<details>`, tables). Visuals come from images and third-party SVG endpoints. Rendered in GitHub light and dark themes.

## Users

Primarily Kevin himself and his friends. The profile is a personal corner, not a hiring pitch. Recruiters and other devs will still land on it, but they don't drive decisions.

## Product Purpose

A GitHub profile that feels like Kevin's own space and shows what he does at a glance. Success: it's fun to open, it looks like him, and a visitor leaves knowing he's a C#/.NET backend developer who does some frontend.

## Positioning

C#/.NET backend developer, with some frontend work (Vue). That identity should read first. The broader tool list is secondary.

## Capabilities and Constraints

- Must keep the GitHub stats cards (stats, top languages, streak, activity graph).
- Must keep the contribution snake animation. It references `raw.githubusercontent.com/black-man2233/black-man2233/output/*.svg`, but no `output` branch exists on the remote (checked 2026-10-15) and no workflow generates one, so the snake is broken right now. It needs a `.github/workflows/snake.yml` (Platane/snk).
- Third-party widgets (vercel/herokuapp endpoints) can rate-limit or go down. Treat them as untrusted uptime.
- The user asked to "add some cool stuff" (more personality/features). Which features is still open.

## Brand Commitments

- Display name: **Kevin** (not the handle `black-man2233`).

## Evidence on Hand

- Existing `README.md`: tech list (C#, Python, JS/TS, .NET, Vue, Bootstrap, Docker, Godot, Linux), stats widgets, snake.
- **Social links point at platform homepages on purpose** (`instagram.com`, `discord.com`, `linkedin.com`, `twitter.com`, `ko-fi.com`, `paypal.com`, empty `mailto:`). Kevin will fill in his own handles (decided 2026-10-15). Keep these as they are; never invent handles or drop them.
- Not yet confirmed for the profile: specific personal projects, interests or music to feature.

## Product Principles

1. **Personal over performative.** Write for Kevin and his friends, not a recruiter checklist. Real touches from his life beat generic dev-profile decoration.
2. **Identity first.** ".NET backend, a bit of frontend" should come through before any badge wall.
3. **Truthful content only.** No placeholder links, invented stats or fake claims.
4. **Fun, but it has to work.** Add playful extras only if they render reliably in both GitHub themes.
