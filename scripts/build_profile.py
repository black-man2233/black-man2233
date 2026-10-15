import io
import re
from dataclasses import dataclass
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "assets"
FONT = ROOT / "src" / "archivo-wdth.woff2"
ICONS = ROOT / "src" / "icons"

CREAM = "#F6ECDD"
CREAM_2 = "#C9B9A3"
CREAM_3 = "#A08F7A"
LAMP = "#FFB46B"
ACCENT = "#F97316"
ACCENT_TEXT = "#FDBA74"
WALL = "#3A2416"
WALL_DARK = "#2A190F"
WOOD = "#7A4A28"
WOOD_LIGHT = "#9C6538"
WOOD_DARK = "#4E2E18"
CARPET = "#1A2744"
CARPET_DEEP = "#121C33"


@dataclass(frozen=True)
class Project:
    name: str
    language: str
    year: int


@dataclass(frozen=True)
class Floor:
    title: str
    note: str
    dot: str
    projects: tuple[Project, ...]


FLOORS = (
    Floor("Backend", "C# / .NET", "#A78BFA", (
        Project("HomeServer.NET", "C#", 2026),
        Project("mydash", "C#", 2026),
        Project("TODOAPI", "C#", 2025),
        Project("TelegramMods", "C#", 2025),
        Project("CopyMyShit", "C#", 2025),
    )),
    Floor("Frontend", "a little", "#4FC08D", (
        Project("homeserverdash", "Vue", 2026),
        Project("Studieplusplus", "JavaScript", 2026),
        Project("biak-next", "Vue", 2026),
    )),
    Floor("Games", "Godot", "#60A5FA", (
        Project("Kimpocalypse", "GDScript", 2024),
    )),
)

TOOLBOX = ("Docker", "Linux", "SQLite", "GraphQL", "Python", "Git", "GitHub Actions", "JetBrains")

SOCIALS = (
    ("instagram", "Instagram"),
    ("discord", "Discord"),
    ("x", "X"),
    ("linkedin", "LinkedIn"),
    ("gmail", "Email"),
    ("kofi", "Ko-fi"),
    ("paypal", "PayPal"),
)
DOCK_DIVIDERS_BEFORE = ("gmail", "kofi")


class Typesetter:
    def __init__(self, font_path: Path) -> None:
        font = TTFont(font_path)
        font.flavor = None
        buffer = io.BytesIO()
        font.save(buffer)
        self._face = hb.Face(buffer.getvalue())
        self._upem = self._face.upem
        self._glyphs: dict[str, str] = {}

    def _font(self, wght: int, wdth: int) -> hb.Font:
        font = hb.Font(self._face)
        font.set_variations({"wght": wght, "wdth": wdth})
        return font

    def _shape(self, text: str, wght: int, wdth: int, features: dict[str, bool]) -> tuple[hb.Font, list, list]:
        font = self._font(wght, wdth)
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, features)
        return font, buf.glyph_infos, buf.glyph_positions

    def width(self, text: str, size: float, wght: int, wdth: int = 100, tracking: float = 0.0, tnum: bool = False) -> float:
        features = {"tnum": True} if tnum else {}
        _, infos, positions = self._shape(text, wght, wdth, features)
        advance = sum(position.x_advance for position in positions)
        tracked = tracking * self._upem * max(len(infos) - 1, 0)
        return (advance + tracked) * size / self._upem

    def text(self, text: str, x: float, y: float, size: float, wght: int, fill: str, wdth: int = 100,
             tracking: float = 0.0, anchor: str = "start", tnum: bool = False, opacity: float | None = None,
             extra: str = "") -> str:
        features = {"tnum": True} if tnum else {}
        font, infos, positions = self._shape(text, wght, wdth, features)
        width = self.width(text, size, wght, wdth, tracking, tnum)
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        scale = size / self._upem
        pen_x = 0.0
        uses = []
        for info, position in zip(infos, positions):
            glyph_id = self._glyph(font, info.codepoint, wght, wdth)
            if glyph_id is not None:
                uses.append(f'<use xlink:href="#{glyph_id}" x="{pen_x + position.x_offset:.0f}"/>')
            pen_x += position.x_advance + tracking * self._upem
        opacity_attr = f' opacity="{opacity}"' if opacity is not None else ""
        return (f'<g transform="translate({x:.2f} {y:.2f}) scale({scale:.5f} {-scale:.5f})" '
                f'fill="{fill}"{opacity_attr}{extra}>{"".join(uses)}</g>')

    def _glyph(self, font: hb.Font, gid: int, wght: int, wdth: int) -> str | None:
        key = f"g{wght}-{wdth}-{gid}"
        if key not in self._glyphs:
            pen = SVGPathPen(None, ntos=lambda value: f"{value:.0f}")
            font.draw_glyph_with_pen(gid, pen)
            self._glyphs[key] = pen.getCommands()
        if not self._glyphs[key]:
            return None
        return key

    def take_defs(self) -> str:
        paths = [f'<path id="{key}" d="{d}"/>' for key, d in self._glyphs.items() if d]
        self._glyphs = {}
        return "".join(paths)


def svg_document(width: int, height: int, title: str, body: str, defs: str, style: str = "") -> str:
    style_block = f"<style>{style}</style>" if style else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img">'
            f"<title>{title}</title>{style_block}<defs>{defs}</defs>{body}</svg>")


SPIN_STYLE = (".platter{transform-box:fill-box;transform-origin:center;animation:spin 1.8s linear infinite}"
              "@keyframes spin{to{transform:rotate(360deg)}}"
              "@media (prefers-reduced-motion:reduce){.platter{animation:none}}")


def shared_defs() -> str:
    return (
        f'<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WALL_DARK}"/>'
        f'<stop offset="0.55" stop-color="{WALL}"/><stop offset="1" stop-color="#452B1A"/></linearGradient>'
        f'<linearGradient id="carpet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CARPET}"/>'
        f'<stop offset="1" stop-color="{CARPET_DEEP}"/></linearGradient>'
        '<pattern id="weave" width="6" height="6" patternUnits="userSpaceOnUse">'
        '<path d="M0 0h6M0 3h6" stroke="#FFFFFF" stroke-opacity="0.018" stroke-width="1"/>'
        '<path d="M0 0v6" stroke="#000000" stroke-opacity="0.05" stroke-width="1"/></pattern>'
        f'<radialGradient id="tv-glow"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0.24"/>'
        f'<stop offset="1" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="lamp-glow"><stop offset="0" stop-color="{LAMP}" stop-opacity="0.5"/>'
        f'<stop offset="0.55" stop-color="#FFA05A" stop-opacity="0.26"/><stop offset="1" stop-color="#FFA05A" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="screen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A1F2E"/>'
        '<stop offset="1" stop-color="#0C0F18"/></linearGradient>'
        f'<radialGradient id="screen-wash" cx="0.5" cy="0" r="0.9"><stop offset="0" stop-color="{ACCENT}" stop-opacity="0.32"/>'
        f'<stop offset="0.7" stop-color="{ACCENT}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="wood-top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WOOD_LIGHT}"/>'
        f'<stop offset="1" stop-color="{WOOD}"/></linearGradient>'
        f'<linearGradient id="wood-body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WOOD}"/>'
        f'<stop offset="1" stop-color="{WOOD_DARK}"/></linearGradient>'
        '<linearGradient id="spk-wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5A341B"/>'
        '<stop offset="0.5" stop-color="#7A4A28"/><stop offset="1" stop-color="#5A341B"/></linearGradient>'
        '<radialGradient id="spk-cone" cx="0.45" cy="0.4" r="0.6"><stop offset="0" stop-color="#3A3330"/>'
        '<stop offset="0.7" stop-color="#1A1614"/><stop offset="1" stop-color="#0D0B0A"/></radialGradient>'
        '<linearGradient id="lamp-shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7D7A8"/>'
        '<stop offset="1" stop-color="#E9A65C"/></linearGradient>'
        '<linearGradient id="pole" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2A1A0E"/>'
        '<stop offset="0.5" stop-color="#6B4A2C"/><stop offset="1" stop-color="#2A1A0E"/></linearGradient>'
        '<linearGradient id="tt-plinth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A5530"/>'
        '<stop offset="1" stop-color="#5E371C"/></linearGradient>'
        '<radialGradient id="tt-vinyl"><stop offset="0" stop-color="#1B1817"/><stop offset="1" stop-color="#0A0909"/></radialGradient>'
        '<linearGradient id="larry" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2A65A"/>'
        '<stop offset="0.48" stop-color="#E9774A"/><stop offset="0.485" stop-color="#3A6B7E"/>'
        '<stop offset="1" stop-color="#1F4357"/></linearGradient>'
        '<linearGradient id="ye" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B3262E"/>'
        '<stop offset="1" stop-color="#6E1219"/></linearGradient>'
        '<linearGradient id="sofa-back" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A3F6E"/>'
        '<stop offset="1" stop-color="#1D2E52"/></linearGradient>'
        '<linearGradient id="sofa-seat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2C4373"/>'
        '<stop offset="1" stop-color="#18264A"/></linearGradient>'
        '<linearGradient id="board-wash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB46B" stop-opacity="0.07"/>'
        '<stop offset="0.35" stop-color="#FFB46B" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="board-rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF0DC" stop-opacity="0.42"/>'
        '<stop offset="0.4" stop-color="#FFF0DC" stop-opacity="0.08"/><stop offset="1" stop-color="#FFF0DC" stop-opacity="0.16"/></linearGradient>'
        '<filter id="soft-shadow" x="-20%" y="-20%" width="140%" height="160%">'
        '<feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#000000" flood-opacity="0.45"/></filter>'
        '<filter id="small-shadow" x="-30%" y="-30%" width="160%" height="180%">'
        '<feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#000000" flood-opacity="0.45"/></filter>'
        '<filter id="halo" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="9"/></filter>'
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>'
    )


def wall(width: float, height: float) -> str:
    planks = []
    for x in range(0, int(width) + 1, 64):
        planks.append(f'<rect x="{x}" y="0" width="2" height="{height}" fill="#000000" fill-opacity="0.28"/>')
    for x in range(0, int(width) + 1, 9):
        planks.append(f'<rect x="{x}" y="0" width="1" height="{height}" fill="#FFFFFF" fill-opacity="0.022"/>')
    return f'<rect width="{width}" height="{height}" fill="url(#wall)"/>{"".join(planks)}'


def baseboard(width: float, y: float) -> str:
    return (f'<rect x="0" y="{y}" width="{width}" height="12" fill="#4A2A15"/>'
            f'<rect x="0" y="{y}" width="{width}" height="2" fill="#6E4223"/>'
            f'<rect x="0" y="{y + 12}" width="{width}" height="8" fill="#000000" fill-opacity="0.25"/>')


def carpet(width: float, y: float, height: float) -> str:
    return (f'<rect x="0" y="{y}" width="{width}" height="{height}" fill="url(#carpet)"/>'
            f'<rect x="0" y="{y}" width="{width}" height="{height}" fill="url(#weave)"/>')


def lamp(cx: float, top: float, floor: float) -> str:
    return (f'<ellipse cx="{cx}" cy="{top + 40}" rx="300" ry="300" fill="url(#lamp-glow)"/>'
            f'<rect x="{cx - 2}" y="{top + 64}" width="4" height="{floor - top - 70}" fill="url(#pole)"/>'
            f'<ellipse cx="{cx}" cy="{floor - 4}" rx="30" ry="5" fill="#2A1A0E"/>'
            f'<path d="M{cx - 26} {top} H{cx + 26} L{cx + 46} {top + 66} H{cx - 46} Z" fill="url(#lamp-shade)"/>'
            f'<ellipse cx="{cx}" cy="{top + 50}" rx="60" ry="40" fill="{LAMP}" opacity="0.35" filter="url(#glow)"/>')


def speaker(x: float, y: float, w: float, h: float) -> str:
    s = w / 110
    return (f'<g transform="translate({x} {y}) scale({s:.4f} {h / 250:.4f})" filter="url(#soft-shadow)">'
            '<rect x="2" y="2" width="106" height="246" rx="8" fill="url(#spk-wood)"/>'
            '<rect x="10" y="10" width="90" height="230" rx="5" fill="#241812"/>'
            '<circle cx="55" cy="58" r="17" fill="#120E0C"/><circle cx="55" cy="58" r="12" fill="url(#spk-cone)"/>'
            '<circle cx="55" cy="58" r="4" fill="#5C524C"/><circle cx="55" cy="160" r="38" fill="#120E0C"/>'
            '<circle cx="55" cy="160" r="32" fill="url(#spk-cone)"/>'
            '<circle cx="55" cy="160" r="20" fill="none" stroke="#2C2522" stroke-width="2"/>'
            '<circle cx="55" cy="160" r="9" fill="#3F3631"/><circle cx="55" cy="222" r="4" fill="#0B0908"/></g>')


def controller(model: str, x: float, y: float, scale: float, angle: float) -> str:
    if model == "ps5":
        art = ('<path d="M22 14c8-6 22-8 38-8s30 2 38 8c10 7 18 30 20 44 2 12-6 18-13 16-8-2-13-14-20-18H35c-7 4-12 16-20 18-7 2-15-4-13-16C4 44 12 21 22 14Z" fill="#F4F2EE"/>'
               '<path d="M38 12h44c4 0 7 3 7 7v20c0 3-3 5-6 5H37c-3 0-6-2-6-5V19c0-4 3-7 7-7Z" fill="#141416"/>'
               '<path d="M39 14h42" stroke="#5AA8FF" stroke-width="2" stroke-linecap="round" opacity="0.9"/>'
               '<circle cx="42" cy="50" r="7" fill="#141416"/><circle cx="78" cy="50" r="7" fill="#141416"/>'
               '<path d="M20 30h10M25 25v10" stroke="#9A9A9E" stroke-width="3" stroke-linecap="round"/>'
               '<circle cx="96" cy="24" r="2.6" fill="#9A9A9E"/><circle cx="102" cy="30" r="2.6" fill="#9A9A9E"/>'
               '<circle cx="90" cy="30" r="2.6" fill="#9A9A9E"/><circle cx="96" cy="36" r="2.6" fill="#9A9A9E"/>')
    else:
        art = ('<path d="M24 16c6-5 18-7 36-7s30 2 36 7c9 7 17 28 19 42 2 12-6 18-13 16-8-2-12-14-19-18H37c-7 4-11 16-19 18-7 2-15-4-13-16 2-14 10-35 19-42Z" fill="#1C1D22"/>'
               '<rect x="40" y="13" width="40" height="22" rx="5" fill="#2A2C33"/>'
               '<path d="M42 11h36" stroke="#3B82F6" stroke-width="3" stroke-linecap="round"/>'
               '<circle cx="44" cy="48" r="7" fill="#0E0F12" stroke="#2F3138" stroke-width="2"/>'
               '<circle cx="76" cy="48" r="7" fill="#0E0F12" stroke="#2F3138" stroke-width="2"/>'
               '<path d="M21 30h10M26 25v10" stroke="#4A4D57" stroke-width="3" stroke-linecap="round"/>'
               '<circle cx="95" cy="24" r="2.8" fill="#4CC38A"/><circle cx="101" cy="30" r="2.8" fill="#F0597A"/>'
               '<circle cx="89" cy="30" r="2.8" fill="#E7A0D6"/><circle cx="95" cy="36" r="2.8" fill="#6BA5F2"/>')
    return (f'<g transform="translate({x} {y}) rotate({angle} 60 38) scale({scale})" filter="url(#small-shadow)">'
            f"{art}</g>")


def tv(ts: Typesetter, x: float, y: float, w: float, h: float, title_size: float, line_size: float,
       title_ratio: float = 0.5) -> str:
    bezel = 9
    cx = x + w / 2
    inner_x = x + bezel
    inner_y = y + bezel
    inner_w = w - bezel * 2
    inner_h = h - bezel * 2
    title_y = y + h * title_ratio
    title = "KEVIN"
    label = "BACKEND"
    stack = "C# / .NET"
    label_size = line_size * 0.82
    gap = line_size * 0.7
    dot_r = line_size * 0.26
    label_w = ts.width(label, label_size, 700, 125, 0.16)
    stack_w = ts.width(stack, line_size, 500)
    line_w = dot_r * 2 + gap * 0.6 + label_w + gap + stack_w
    line_x = cx - line_w / 2
    line_y = title_y + line_size * 2.3
    sub_y = line_y + line_size * 1.75
    glare = (f'<path d="M{inner_x} {inner_y} H{inner_x + inner_w * 0.42} L{inner_x + inner_w * 0.16} {inner_y + inner_h} H{inner_x} Z" '
             'fill="#FFFFFF" fill-opacity="0.06"/>')
    return (
        f'<ellipse cx="{cx}" cy="{y + h * 0.45}" rx="{w * 0.92}" ry="{h * 0.98}" fill="url(#tv-glow)"/>'
        f'<rect x="{cx - w * 0.13}" y="{y + h - 2}" width="{w * 0.26}" height="11" rx="4" fill="#121110"/>'
        f'<g filter="url(#soft-shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#0E0D0D"/></g>'
        f'<rect x="{inner_x}" y="{inner_y}" width="{inner_w}" height="{inner_h}" rx="3" fill="url(#screen)"/>'
        f'<rect x="{inner_x}" y="{inner_y}" width="{inner_w}" height="{inner_h}" rx="3" fill="url(#screen-wash)"/>'
        f"{glare}"
        + ts.text(title, cx, title_y, title_size, 600, ACCENT, 112, 0.08, "middle", opacity=0.55, extra=' filter="url(#halo)"')
        + ts.text(title, cx, title_y, title_size, 600, CREAM, 112, 0.08, "middle")
        + f'<circle cx="{line_x + dot_r}" cy="{line_y - label_size * 0.36}" r="{dot_r}" fill="{ACCENT}"/>'
        + ts.text(label, line_x + dot_r * 2 + gap * 0.6, line_y, label_size, 700, ACCENT_TEXT, 125, 0.16)
        + ts.text(stack, line_x + dot_r * 2 + gap * 0.6 + label_w + gap, line_y, line_size, 500, CREAM)
        + ts.text("a little frontend on the side", cx, sub_y, line_size * 0.82, 450, CREAM_2, anchor="middle")
    )


def stand(x: float, y: float, w: float, floor: float, body_h: float) -> str:
    top_h = 14
    inset = 8
    pad = 8
    gap = 7
    body_x = x + inset
    body_w = w - inset * 2
    body_y = y + top_h
    drawer_w = (body_w - pad * 2 - gap * 2) / 3
    drawer_h = body_h - pad * 2
    parts = [f'<g filter="url(#soft-shadow)"><rect x="{body_x}" y="{body_y}" width="{body_w}" height="{body_h}" fill="url(#wood-body)"/></g>']
    for line_x in range(int(body_x), int(body_x + body_w), 17):
        parts.append(f'<rect x="{line_x}" y="{body_y}" width="2" height="{body_h}" fill="#000000" fill-opacity="0.07"/>')
    for index in range(3):
        dx = body_x + pad + index * (drawer_w + gap)
        dy = body_y + pad
        if index == 1:
            ps5_w = min(drawer_w * 0.8, 120)
            ps5_x = dx + (drawer_w - ps5_w) / 2
            ps5_y = dy + drawer_h - 30
            parts.append(f'<rect x="{dx}" y="{dy}" width="{drawer_w}" height="{drawer_h}" rx="3" fill="#160E09"/>'
                         f'<rect x="{ps5_x}" y="{ps5_y}" width="{ps5_w}" height="24" rx="11" fill="#F4F2EE"/>'
                         f'<rect x="{ps5_x}" y="{ps5_y + 10}" width="{ps5_w}" height="5" fill="#141416"/>'
                         f'<ellipse cx="{ps5_x + ps5_w / 2}" cy="{ps5_y + 12}" rx="{ps5_w * 0.6}" ry="18" fill="#5AA8FF" opacity="0.12" filter="url(#glow)"/>')
        else:
            parts.append(f'<rect x="{dx}" y="{dy}" width="{drawer_w}" height="{drawer_h}" rx="3" fill="#FFDCB4" fill-opacity="0.06" '
                         'stroke="#000000" stroke-opacity="0.25"/>'
                         f'<rect x="{dx + drawer_w / 2 - 20}" y="{dy + drawer_h / 2 - 2.5}" width="40" height="5" rx="2.5" fill="#C8A57A"/>')
    legs_y = body_y + body_h
    parts.append(f'<rect x="{x + 28}" y="{legs_y}" width="11" height="{floor - legs_y}" fill="{WOOD_DARK}"/>'
                 f'<rect x="{x + w - 39}" y="{legs_y}" width="11" height="{floor - legs_y}" fill="{WOOD_DARK}"/>')
    grain = "".join(f'<rect x="{grain_x}" y="{y + 1}" width="2" height="{top_h - 2}" fill="#000000" fill-opacity="0.09"/>'
                    for grain_x in range(int(x) + 6, int(x + w) - 6, 14))
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{top_h}" rx="4" fill="url(#wood-top)"/>{grain}'
                 f'<rect x="{x + 3}" y="{y + 1}" width="{w - 6}" height="1" fill="#FFDCB4" fill-opacity="0.25"/>')
    return "".join(parts)


def turntable(x: float, y: float, scale: float) -> str:
    return (f'<g transform="translate({x} {y}) scale({scale})" filter="url(#small-shadow)">'
            '<rect x="4" y="16" width="212" height="122" rx="10" fill="url(#tt-plinth)"/>'
            '<rect x="4" y="128" width="212" height="12" rx="4" fill="#3E2412"/>'
            '<circle cx="88" cy="76" r="56" fill="#2B2724"/>'
            '<g class="platter"><circle cx="88" cy="76" r="52" fill="url(#tt-vinyl)"/>'
            '<circle cx="88" cy="76" r="46" fill="none" stroke="#2C2826" stroke-width="0.8"/>'
            '<circle cx="88" cy="76" r="40" fill="none" stroke="#2C2826" stroke-width="0.8"/>'
            '<circle cx="88" cy="76" r="33" fill="none" stroke="#2C2826" stroke-width="0.8"/>'
            '<circle cx="88" cy="76" r="27" fill="none" stroke="#2C2826" stroke-width="0.8"/>'
            '<circle cx="88" cy="76" r="17" fill="#E9A23B"/>'
            '<path d="M76 72h24" stroke="#5B2E0E" stroke-width="2.4" stroke-linecap="round"/>'
            '<path d="M80 80h16" stroke="#5B2E0E" stroke-width="1.6" stroke-linecap="round" opacity="0.7"/>'
            '<circle cx="88" cy="76" r="2.4" fill="#E9E2D6"/></g>'
            '<path d="M88 26a50 50 0 0 1 46 30" fill="none" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="5" stroke-linecap="round"/>'
            '<circle cx="182" cy="40" r="11" fill="#2C2826"/><circle cx="182" cy="40" r="5" fill="#B9B2A6"/>'
            '<path d="M182 40 L168 104 L140 112" fill="none" stroke="#CFC8BC" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
            '<rect x="128" y="106" width="16" height="10" rx="2" fill="#1A1716" transform="rotate(-14 136 111)"/>'
            '<circle cx="196" cy="118" r="5" fill="#2C2826"/><circle cx="178" cy="118" r="3" fill="#E9A23B"/></g>')


def sleeve(ts: Typesetter, x: float, bottom: float, size: float, angle: float, artist: tuple[str, str], larry: bool) -> str:
    y = bottom - size
    text_size = size * 0.1
    pad = size * 0.09
    ink = "#FFF4E0" if larry else "#1A1615"
    if larry:
        art = (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="3" fill="url(#larry)"/>'
               f'<circle cx="{x + size * 0.5}" cy="{y + size * 0.36}" r="{size * 0.17}" fill="#FFE1A1"/>')
    else:
        art = (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="3" fill="#E8E2D8"/>'
               f'<rect x="{x + size * 0.15}" y="{y + size * 0.15}" width="{size * 0.7}" height="{size * 0.46}" rx="2" fill="url(#ye)"/>')
    lines = (ts.text(artist[0], x + pad, bottom - pad - text_size * 1.15, text_size, 800, ink, 125, 0.12)
             + ts.text(artist[1], x + pad, bottom - pad, text_size, 800, ink, 125, 0.12))
    return f'<g transform="rotate({angle} {x} {bottom})" filter="url(#small-shadow)">{art}{lines}</g>'


def vinyl_corner(ts: Typesetter, x: float, floor: float, scale: float) -> str:
    table_w = 240 * scale
    top_y = floor - 170 * scale
    shelf_y = top_y + 16 * scale
    shelf_h = 84 * scale
    spines = []
    spine_colors = (("#C8462E", 64), ("#E9DCC6", 60), ("#1E1B1A", 64), ("#D9A13B", 62), ("#3C5A8C", 58))
    for index, (color, height) in enumerate(spine_colors):
        sx = x + (10 + 12 + index * 10) * scale
        spines.append(f'<rect x="{sx}" y="{shelf_y + shelf_h - height * scale}" width="{7 * scale}" height="{height * scale}" rx="1" fill="{color}"/>')
    sleeve_size = 118 * scale
    return (
        f'<rect x="{x + 18 * scale}" y="{shelf_y + shelf_h + 12 * scale}" width="{12 * scale}" height="{floor - shelf_y - shelf_h - 12 * scale}" fill="{WOOD_DARK}"/>'
        f'<rect x="{x + table_w - 30 * scale}" y="{shelf_y + shelf_h + 12 * scale}" width="{12 * scale}" height="{floor - shelf_y - shelf_h - 12 * scale}" fill="{WOOD_DARK}"/>'
        f'<rect x="{x + 10 * scale}" y="{shelf_y}" width="{table_w - 20 * scale}" height="{shelf_h}" fill="#2A180D"/>'
        + "".join(spines)
        + f'<rect x="{x + 10 * scale}" y="{shelf_y + shelf_h}" width="{table_w - 20 * scale}" height="{12 * scale}" fill="{WOOD}"/>'
        f'<g filter="url(#small-shadow)"><rect x="{x}" y="{top_y}" width="{table_w}" height="{16 * scale}" rx="4" fill="url(#wood-top)"/></g>'
        + turntable(x + 10 * scale, top_y - 150 * scale + 2, scale)
        + sleeve(ts, x + 22 * scale, floor, sleeve_size, -9, ("LARRY", "JUNE"), True)
        + sleeve(ts, x + 106 * scale, floor, sleeve_size, 4, ("KANYE", "WEST"), False)
    )


@dataclass(frozen=True)
class BoardStyle:
    head: float
    name: float
    meta: float
    suite: float
    row: float
    head_gap: float
    floor_gap: float


def floor_height(floor: Floor, style: BoardStyle) -> float:
    return style.head_gap + len(floor.projects) * style.row


def board_floor(ts: Typesetter, floor: Floor, x: float, y: float, w: float, style: BoardStyle) -> str:
    parts = []
    dot_r = style.head * 0.27
    head_y = y + style.head
    title = floor.title.upper()
    parts.append(f'<circle cx="{x + dot_r}" cy="{head_y - style.head * 0.37}" r="{dot_r}" fill="{floor.dot}"/>')
    title_x = x + dot_r * 2 + style.head * 0.9
    parts.append(ts.text(title, title_x, head_y, style.head, 700, CREAM, 125, 0.16))
    title_w = ts.width(title, style.head, 700, 125, 0.16)
    parts.append(ts.text(floor.note, title_x + title_w + style.head * 0.8, head_y, style.head, 450, CREAM_3, tracking=0.02))
    parts.append(ts.text(str(len(floor.projects)), x + w, head_y, style.head * 0.95, 500, CREAM_3, anchor="end", tnum=True))
    rule_y = head_y + style.head * 1.05
    parts.append(f'<rect x="{x}" y="{rule_y}" width="{w}" height="1" fill="{CREAM}" fill-opacity="0.12"/>'
                 f'<rect x="{x}" y="{rule_y + 1}" width="{w}" height="1" fill="#FFFFFF" fill-opacity="0.03"/>')
    row_top = y + style.head_gap
    for index, project in enumerate(floor.projects):
        baseline = row_top + index * style.row + style.row * 0.5 + style.name * 0.36
        parts.append(ts.text(project.name, x, baseline, style.name, 500, CREAM))
        name_w = ts.width(project.name, style.name, 500)
        meta_x = x + name_w + style.name * 0.5
        parts.append(ts.text(project.language, meta_x, baseline, style.meta, 500, CREAM_3, tracking=0.02))
        meta_w = ts.width(project.language, style.meta, 500, tracking=0.02)
        year = str(project.year)
        year_w = ts.width(year, style.suite, 450, 112, -0.02, tnum=True)
        leader_start = meta_x + meta_w + style.name * 0.6
        leader_end = x + w - year_w - style.name * 0.6
        if leader_end > leader_start:
            parts.append(f'<path d="M{leader_start:.1f} {baseline - 1:.1f}H{leader_end:.1f}" stroke="{CREAM}" stroke-opacity="0.24" '
                         'stroke-width="1.4" stroke-linecap="round" stroke-dasharray="0.1 5"/>')
        parts.append(ts.text(year, x + w, baseline, style.suite, 450, CREAM, 112, -0.02, "end", tnum=True))
    return "".join(parts)


def plaque(ts: Typesetter, x: float, y: float, w: float, style: BoardStyle, wrap: bool) -> tuple[str, float]:
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="1" fill="{CREAM}" fill-opacity="0.12"/>']
    label = "TOOLBOX"
    label_y = y + style.head * 2.6
    parts.append(ts.text(label, x, label_y, style.head, 700, CREAM_2, 125, 0.16))
    items_x = x + ts.width(label, style.head, 700, 125, 0.16) + style.head * 1.6
    separator = "  ·  "
    line_size = style.meta * 1.12
    if not wrap:
        parts.append(ts.text(separator.join(TOOLBOX), items_x, label_y, line_size, 450, CREAM_2))
        return "".join(parts), label_y
    lines: list[str] = []
    current = ""
    for item in TOOLBOX:
        candidate = item if not current else current + separator + item
        if ts.width(candidate, line_size, 450) > w - (items_x - x) and current:
            lines.append(current)
            current = item
        else:
            current = candidate
    lines.append(current)
    for index, line in enumerate(lines):
        parts.append(ts.text(line, items_x, label_y + index * line_size * 1.6, line_size, 450, CREAM_2))
    return "".join(parts), label_y + (len(lines) - 1) * line_size * 1.6


def board_frame(x: float, y: float, w: float, h: float, radius: float) -> str:
    shadow_mask = (f'<mask id="board-outside" maskUnits="userSpaceOnUse"><rect x="{x - 80}" y="{y - 80}" width="{w + 160}" height="{h + 160}" fill="#FFFFFF"/>'
                   f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="#000000"/></mask>')
    return (f'{shadow_mask}<g mask="url(#board-outside)"><g filter="url(#soft-shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="#141B2E"/></g></g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="#141B2E" fill-opacity="0.62"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="url(#board-wash)"/>'
            f'<rect x="{x + 0.75}" y="{y + 0.75}" width="{w - 1.5}" height="{h - 1.5}" rx="{radius}" fill="none" stroke="url(#board-rim)" stroke-width="1.5"/>')


def window(width: float, height: float, radius: float) -> str:
    return f'<clipPath id="window"><rect width="{width}" height="{height}" rx="{radius}"/></clipPath>'


def build_room(ts: Typesetter) -> str:
    width = 1000
    floor_y = 440
    style = BoardStyle(head=14, name=21, meta=14, suite=33, row=56, head_gap=42, floor_gap=40)
    board_x, board_y, board_w = 36, floor_y + 52, width - 72
    pad_x, pad_top = 40, 34
    col_gap = 56
    col_w = (board_w - pad_x * 2 - col_gap) / 2
    left_x = board_x + pad_x
    right_x = left_x + col_w + col_gap
    columns = ((FLOORS[0],), (FLOORS[1], FLOORS[2]))
    board_parts = []
    column_bottoms = []
    for column, col_x in zip(columns, (left_x, right_x)):
        cursor = board_y + pad_top
        for index, floor in enumerate(column):
            if index:
                cursor += style.floor_gap
            board_parts.append(board_floor(ts, floor, col_x, cursor, col_w, style))
            cursor += floor_height(floor, style)
        column_bottoms.append(cursor)
    columns_bottom = max(column_bottoms)
    divider_x = left_x + col_w + col_gap / 2
    board_parts.append(f'<rect x="{divider_x}" y="{board_y + pad_top - 4}" width="1" height="{columns_bottom - board_y - pad_top + 8}" fill="{CREAM}" fill-opacity="0.1"/>')
    plaque_svg, plaque_bottom = plaque(ts, left_x, columns_bottom + 26, board_w - pad_x * 2, style, wrap=False)
    board_parts.append(plaque_svg)
    board_h = plaque_bottom + 30 - board_y
    height = int(board_y + board_h + 44)
    scene = (
        wall(width, floor_y)
        + lamp(86, 78, floor_y)
        + tv(ts, 290, 70, 420, 238, 66, 17)
        + speaker(198, 140, 76, 172)
        + speaker(726, 140, 76, 172)
        + stand(186, 312, 628, floor_y, 66)
        + controller("ps4", 292, 272, 0.62, -8)
        + controller("ps5", 634, 272, 0.62, 7)
        + vinyl_corner(ts, 830, floor_y, 0.66)
        + baseboard(width, floor_y)
        + carpet(width, floor_y + 12, height - floor_y - 12)
        + f'<rect x="0" y="{floor_y + 12}" width="{width}" height="8" fill="#000000" fill-opacity="0.22"/>'
        + board_frame(board_x, board_y, board_w, board_h, 30)
        + "".join(board_parts)
    )
    defs = shared_defs() + window(width, height, 24) + ts.take_defs()
    body = f'<g clip-path="url(#window)">{scene}</g>'
    return svg_document(width, height, "Kevin's living room", body, defs, SPIN_STYLE)


def build_room_compact(ts: Typesetter) -> str:
    width = 600
    floor_y = 360
    style = BoardStyle(head=17, name=25, meta=17, suite=38, row=64, head_gap=50, floor_gap=44)
    board_x, board_w = 20, width - 40
    board_y = floor_y + 40
    pad_x, pad_top = 30, 34
    col_x = board_x + pad_x
    col_w = board_w - pad_x * 2
    parts = []
    cursor = board_y + pad_top
    for index, floor in enumerate(FLOORS):
        if index:
            cursor += style.floor_gap
        parts.append(board_floor(ts, floor, col_x, cursor, col_w, style))
        cursor += floor_height(floor, style)
    plaque_svg, plaque_bottom = plaque(ts, col_x, cursor + 30, col_w, style, wrap=True)
    parts.append(plaque_svg)
    board_h = plaque_bottom + 34 - board_y
    height = int(board_y + board_h + 30)
    scene = (
        wall(width, floor_y)
        + tv(ts, 30, 52, 370, 214, 64, 23, 0.4)
        + stand(18, 272, 394, floor_y, 52)
        + controller("ps4", 70, 252, 0.5, -8)
        + controller("ps5", 300, 252, 0.5, 7)
        + vinyl_corner(ts, 424, floor_y, 0.68)
        + baseboard(width, floor_y)
        + carpet(width, floor_y + 12, height - floor_y - 12)
        + board_frame(board_x, board_y, board_w, board_h, 24)
        + "".join(parts)
    )
    defs = shared_defs() + window(width, height, 20) + ts.take_defs()
    body = f'<g clip-path="url(#window)">{scene}</g>'
    return svg_document(width, height, "Kevin's living room", body, defs, SPIN_STYLE)


def sofa(x: float, y: float, scale: float) -> str:
    return (f'<g transform="translate({x} {y}) scale({scale})" filter="url(#soft-shadow)">'
            '<rect x="70" y="20" width="620" height="120" rx="34" fill="url(#sofa-back)"/>'
            '<rect x="88" y="34" width="286" height="100" rx="26" fill="#25395F"/>'
            '<rect x="386" y="34" width="286" height="100" rx="26" fill="#25395F"/>'
            '<rect x="60" y="120" width="640" height="78" rx="24" fill="url(#sofa-seat)"/>'
            '<path d="M380 128v66" stroke="#142140" stroke-width="3"/>'
            '<rect x="10" y="78" width="96" height="140" rx="34" fill="#22365E"/>'
            '<rect x="654" y="78" width="96" height="140" rx="34" fill="#22365E"/>'
            '<rect x="120" y="58" width="96" height="74" rx="20" fill="#C8783E" transform="rotate(-8 168 95)"/>'
            '<rect x="560" y="60" width="90" height="70" rx="20" fill="#E3C9A0" transform="rotate(7 605 95)"/>'
            '<rect x="70" y="214" width="20" height="30" rx="4" fill="#3A2010"/>'
            '<rect x="670" y="214" width="20" height="30" rx="4" fill="#3A2010"/></g>')


def coffee_table(cx: float, top: float, w: float) -> str:
    x = cx - w / 2
    return (f'<rect x="{x + 26}" y="{top + 16}" width="11" height="44" fill="{WOOD_DARK}"/>'
            f'<rect x="{x + w - 37}" y="{top + 16}" width="11" height="44" fill="{WOOD_DARK}"/>'
            f'<g filter="url(#soft-shadow)"><rect x="{x}" y="{top}" width="{w}" height="18" rx="9" fill="url(#wood-top)"/></g>'
            f'<rect x="{x + 60}" y="{top - 33}" width="28" height="33" rx="4" fill="#E8DCC8"/>'
            f'<path d="M{x + 88} {top - 26} h5 a7 7 0 0 1 0 14 h-5" fill="none" stroke="#E8DCC8" stroke-width="4"/>'
            f'<rect x="{x + w - 140}" y="{top - 14}" width="70" height="13" rx="6.5" fill="#1A1918" transform="rotate(-6 {x + w - 105} {top - 7})"/>')


def build_lounge(ts: Typesetter, width: int, compact: bool) -> str:
    motto = "SHIP THINGS. BREAK THINGS. FIX THINGS. REPEAT."
    fact = "I debug with Console.WriteLine and I am not ashamed."
    cx = width / 2
    motto_size = 22 if compact else 15
    fact_size = 22 if compact else 16
    if compact:
        words = motto.split(". ")
        motto_lines = [". ".join(words[:2]) + ".", ". ".join(words[2:])]
    else:
        motto_lines = [motto]
    motto_y = 62
    texts = []
    for index, line in enumerate(motto_lines):
        texts.append(ts.text(line, cx, motto_y + index * motto_size * 1.7, motto_size, 700, CREAM, 125, 0.16, "middle"))
    table_top = motto_y + (len(motto_lines) - 1) * motto_size * 1.7 + 96
    sofa_scale = (width - 80) / 760 if compact else 0.8
    sofa_w = 760 * sofa_scale
    sofa_y = table_top + 90
    sofa_h = 250 * sofa_scale
    fact_y = sofa_y + sofa_h + 54
    height = int(fact_y + 40)
    scene = (
        carpet(width, 0, height)
        + "".join(texts)
        + coffee_table(cx, table_top, 300)
        + sofa(cx - sofa_w / 2, sofa_y, sofa_scale)
        + ts.text(fact, cx, fact_y, fact_size, 450, CREAM_2, anchor="middle")
    )
    defs = shared_defs() + window(width, height, 20 if compact else 24) + ts.take_defs()
    return svg_document(width, height, "Kevin's sofa", f'<g clip-path="url(#window)">{scene}</g>', defs)


DOCK_H = 56
PILL_TOP = 6
PILL_H = 44


def dock_fill(width: float) -> str:
    return (f'<rect x="0" y="{PILL_TOP}" width="{width}" height="{PILL_H}" fill="url(#dock)"/>'
            f'<rect x="0" y="{PILL_TOP}" width="{width}" height="1" fill="#FFF0DC" fill-opacity="0.38"/>'
            f'<rect x="0" y="{PILL_TOP + PILL_H - 1}" width="{width}" height="1" fill="#FFF0DC" fill-opacity="0.12"/>'
            f'<rect x="0" y="{PILL_TOP + PILL_H}" width="{width}" height="3" fill="#000000" fill-opacity="0.16"/>')


DOCK_DEFS = ('<linearGradient id="dock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#26324F"/>'
             '<stop offset="1" stop-color="#18213A"/></linearGradient>')


def icon_path(name: str) -> str:
    source = (ICONS / f"{name}.svg").read_text()
    match = re.search(r'<path d="([^"]+)"', source)
    if match is None:
        raise ValueError(f"No path in icon {name}")
    return match.group(1)


def build_dock_segment(name: str, label: str) -> str:
    width = 52
    divider = ""
    if name in DOCK_DIVIDERS_BEFORE:
        divider = f'<rect x="0" y="{PILL_TOP + 13}" width="1" height="{PILL_H - 26}" fill="{CREAM}" fill-opacity="0.16"/>'
    icon_size = 20
    scale = icon_size / 24
    ix = (width - icon_size) / 2
    iy = PILL_TOP + (PILL_H - icon_size) / 2
    icon = f'<path transform="translate({ix} {iy}) scale({scale:.4f})" d="{icon_path(name)}" fill="{CREAM}" fill-opacity="0.9"/>'
    return svg_document(width, DOCK_H, label, dock_fill(width) + divider + icon, DOCK_DEFS)


def build_dock_cap(side: str) -> str:
    width = 24
    r = PILL_H / 2
    if side == "left":
        shape = f'M{width} {PILL_TOP} H{r} A{r} {r} 0 0 0 {r} {PILL_TOP + PILL_H} H{width} Z'
        rim = f'M{width} {PILL_TOP + 0.5} H{r} A{r - 0.5} {r - 0.5} 0 0 0 2 {PILL_TOP + r}'
    else:
        shape = f'M0 {PILL_TOP} H{width - r} A{r} {r} 0 0 1 {width - r} {PILL_TOP + PILL_H} H0 Z'
        rim = f'M0 {PILL_TOP + 0.5} H{width - r} A{r - 0.5} {r - 0.5} 0 0 1 {width - 2} {PILL_TOP + r}'
    clip = f'<clipPath id="cap"><path d="{shape}"/></clipPath>'
    body = (f'<path d="M0 {PILL_TOP + PILL_H} h{width} v3 h-{width} Z" fill="#000000" fill-opacity="0.16" clip-path="url(#shadow-cap)"/>'
            f'<g clip-path="url(#cap)">{dock_fill(width)}</g>'
            f'<path d="{rim}" fill="none" stroke="#FFF0DC" stroke-opacity="0.38" stroke-width="1"/>')
    shadow_clip = f'<clipPath id="shadow-cap"><path d="{shape}" transform="translate(0 3)"/></clipPath>'
    return svg_document(width, DOCK_H, "", body, DOCK_DEFS + clip + shadow_clip)


def write(name: str, content: str) -> None:
    path = OUT / name
    path.write_text(content)
    print(f"{path.relative_to(OUT.parent)}  {len(content) // 1024} KB")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    ts = Typesetter(FONT)
    write("room.svg", build_room(ts))
    write("room-compact.svg", build_room_compact(ts))
    write("lounge.svg", build_lounge(ts, 1000, compact=False))
    write("lounge-compact.svg", build_lounge(ts, 600, compact=True))
    write("dock-left.svg", build_dock_cap("left"))
    write("dock-right.svg", build_dock_cap("right"))
    for name, label in SOCIALS:
        write(f"dock-{name}.svg", build_dock_segment(name, label))


if __name__ == "__main__":
    main()
