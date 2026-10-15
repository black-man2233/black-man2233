# Profile art

`assets/*.svg` is generated. Don't hand-edit it; change `build_profile.py` and rebuild:

```sh
python -m venv .venv && .venv/bin/pip install fonttools brotli uharfbuzz
.venv/bin/python scripts/build_profile.py
```

- Projects, toolbox and socials live in the `FLOORS`, `TOOLBOX` and `SOCIALS` tuples at the top of the script.
- Text is baked in as Archivo glyph outlines. GitHub serves README images with no external fonts, so live text would fall back to a system font.
- GitHub strips CSS and JS from READMEs. The only motion is the turntable, a CSS animation inside the SVG, and it stops under `prefers-reduced-motion`.
- Font: Archivo (SIL OFL, `src/OFL.txt`). Icons: Simple Icons 9.21.0 (CC0).
