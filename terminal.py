"""Generates terminal.svg, the terminal at the top of my GitHub profile README.

How to update the profile:
1. Edit the content block below (the prompt / say / table calls). Colors are my Ghostty palette.
2. python3 terminal.py terminal.svg
3. Open terminal.svg in a browser to check it (lines animate in, tables must not overflow).
4. Keep the <img alt> on the first line of README.md in sync: screen readers and search see only the alt.
5. Commit README.md, terminal.py and terminal.svg together and push. The profile updates right away.

Goes stale by hand: the gzyms version.
"""
import sys
from html import escape

BG, FG, DIM = "#1E1E2E", "#F0F0FF", "#9399B2"
GREEN, BLUE, PURPLE, CYAN, PINK = "#50FA7B", "#8AB4F8", "#B347FF", "#8BE9FD", "#FF6B9D"

FS, LH, PAD, TOP, W = 14, 22, 24, 64, 900
CW = FS * 0.6  # monospace advance
STEP = 0.12    # seconds between lines appearing

lines = []  # each: list of (col_in_chars, text, color, bold)
boxes = []  # (first line, rows, col widths, has header)


def say(*spans):
    col, out = 0, []
    for s in spans:
        t, c, b = (s + (False,))[:3]
        out.append((col, t, c, b))
        col += len(t)
    lines.append(out)


def prompt(cmd):
    say(("~ ", BLUE), ("❯ ", GREEN), (cmd, FG))


def table(rows, header=None):
    """Nushell-style table. Text goes in lines, borders are SVG strokes drawn later."""
    allrows = ([header] if header else []) + rows
    w = [max(len(c[0]) for c in col) + 3 for col in zip(*allrows)]
    lines.append([])
    boxes.append((len(lines), len(allrows), w, bool(header)))
    for r, cells in enumerate(allrows):
        starts = [sum(w[:k]) + 1.5 for k in range(len(w))]
        lines.append([(x, t, c, bool(header) and r == 0) for x, (t, c) in zip(starts, cells)])
    lines.append([])


prompt("whoami")
say(("Greg Zalewski", PURPLE, True), (" · Staff Software Engineer @ Redocly (Austin, TX)", FG))
say(("In IT since 2010: automating, tinkering and solving interesting problems.", DIM))
say()
prompt("ls ~/projects | where active")
table(
    header=[("#", GREEN), ("name", GREEN), ("what", GREEN), ("stack", GREEN)],
    rows=[
        [("0", GREEN), ("gzyms", CYAN), ("a status bar for macOS at ~0% CPU, v0.0.1 is out", FG), ("Swift", PINK)],
        [("1", GREEN), ("dotfiles", CYAN), ("my whole setup: shell, editor, agents, smart home", FG), ("chezmoi · nu", PINK)],
        [("2", GREEN), ("home-lab", CYAN), ("my playground: smart home tools, jarvis-brain assistant", FG), ("Docker · Node", PINK)],
        [("3", GREEN), ("HyprMac", CYAN), ("macOS tiling window manager, latest open source contribution", FG), ("Swift", PINK)],
    ],
)
prompt("brew install zalewskigrzegorz/tap/gzyms")
say(("==>", BLUE, True), (" Installing Cask ", FG), ("gzyms", GREEN, True))
say(("🍺  gzyms was successfully installed!", FG))
say()
prompt("open ~/stack.toml")
table(rows=[
    [("terminal", GREEN), ("nushell · tuios · nvim (LazyVim)", FG)],
    [("work", GREEN), ("TypeScript · React · Node · Postgres · AWS", FG)],
    [("off hours", GREEN), ("gaming, smart home, keeping a dog and a cat out of trouble", FG)],
])
prompt("")

H = TOP + LH * len(lines) + PAD - 6
out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">
<title id="t">Greg Zalewski, Staff Software Engineer at Redocly. Projects: gzyms, dotfiles, HyprMac.</title>
<style>
text{{font:{FS}px "JetBrains Mono","SF Mono",Menlo,Consolas,"DejaVu Sans Mono",monospace;white-space:pre}}
.b{{font-weight:700}}
.l{{animation:in .25s ease-out both}}
.c{{animation:blink 1s steps(1) infinite}}
@keyframes in{{from{{opacity:0;transform:translateY(4px)}}}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.l,.c{{animation:none}}}}
</style>
<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="#585B70" stroke-opacity=".6"/>
<circle cx="22" cy="20" r="6" fill="#FF5F57"/><circle cx="42" cy="20" r="6" fill="#FEBC2E"/><circle cx="62" cy="20" r="6" fill="#28C840"/>
<text x="{W / 2}" y="25" fill="{DIM}" text-anchor="middle" font-size="12">nu — ~</text>''']

for i, spans in enumerate(lines):
    # textLength pins every span to the grid whatever monospace font the viewer has; emoji are left alone
    fit = lambda t: "" if any(ord(ch) > 0xFFFF for ch in t) else f' textLength="{len(t) * CW:.1f}" lengthAdjust="spacingAndGlyphs"'
    parts = [f'<tspan x="{PAD + col * CW:.1f}"{fit(t)} fill="{c}"{" class=\"b\"" if b else ""}>{escape(t)}</tspan>'
             for col, t, c, b in spans if t]
    if i == len(lines) - 1:
        end = max(col + len(t) for col, t, _, _ in spans)
        parts.append(f'<tspan x="{PAD + end * CW:.1f}" class="c" fill="{FG}">█</tspan>')
    if parts:
        out.append(f'<text y="{TOP + i * LH}" class="l" style="animation-delay:{i * STEP:.2f}s">{"".join(parts)}</text>')

for first, n, w, header in boxes:
    mid = lambda k: TOP + k * LH - FS * 0.35  # visual middle of line k
    y0, y1 = mid(first) - LH / 2 - 2, mid(first + n - 1) + LH / 2 + 2
    x0 = PAD
    x1 = x0 + sum(w) * CW
    path = "".join(f"M{x0 + sum(w[:k + 1]) * CW:.1f} {y0:.1f}V{y1:.1f}" for k in range(len(w) - 1))
    if header:
        path += f"M{x0:.1f} {mid(first) + LH / 2:.1f}H{x1:.1f}"
    out.append(f'<g class="l" style="animation-delay:{first * STEP:.2f}s" stroke="{DIM}" stroke-opacity=".55" fill="none">'
               f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" rx="6"/><path d="{path}"/></g>')

out.append("</svg>")
open(sys.argv[1], "w").write("\n".join(out) + "\n")
print(f"{W}x{H}, {len(lines)} lines, {len(boxes)} tables")
