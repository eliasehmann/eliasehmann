#!/usr/bin/env python3
"""Writes profile.svg: a macOS Terminal window (dark, zsh, 80x24) that types
the command once, prints the output, and then stays there.
Edit the text below and run ./render.py."""
import os
from html import escape

USER, DIR, BRANCH = "eliasehmann", "eliasehmann", "main"
# The oh-my-zsh default prompt (robbyrussell theme) inside a git repository.
PROMPT = f"➜  {DIR} git:({BRANCH}) "
PROMPT_SVG = (f'<tspan class="green">➜</tspan>  <tspan class="cyan">{DIR}</tspan> '
              f'<tspan class="blue">git:(</tspan><tspan class="red">{BRANCH}</tspan>'
              f'<tspan class="blue">)</tspan> ')
COMMAND = "kubectl describe human eliasehmann"
OUTPUT = """\
Name:         eliasehmann
Namespace:    not-default
Labels:       gitops=flux
              lang=go
              platform=kubernetes
API Version:  github.com/v1
Kind:         Human
Spec:
  Prod:  a dual-boot laptop, IPv6 only
Status:
  Phase:     Building
  Restarts:  too many (WSL)
Events:
  Type     Reason       Age  From      Message
  ----     ------       ---  ----      -------""".splitlines()
EVENTS = [  # these arrive one at a time
    "  Normal   Building     3h   me        own stuff",
    "  Warning  BugFound     2h   upstream  in a tool I depend on",
    "  Normal   PullRequest  1h   me        fix sent upstream",
    "  Normal   Building     5m   me        own stuff again",
]

COLS = 80
ROWS = 1 + len(OUTPUT) + len(EVENTS) + 1  # exactly what is shown, no empty rows
W, BAR, PAD, LINE, FONT = 640, 28, 6, 17, 13          # the window itself
MX, MTOP, MBOT = 26, 10, 28                           # room for the shadow
H = BAR + 2 * PAD + ROWS * LINE
START, PER_CHAR, AFTER_ENTER, PER_EVENT = 0.9, 0.06, 0.5, 0.85
AT = float(os.environ.get("AT", 0))  # for testing: render as if AT seconds in (use with OUT)
OUT = os.environ.get("OUT", "profile.svg")


def y(row):
    return BAR + PAD + (row + 1) * LINE - 4


def line(row, text, delay):
    text = escape(text).replace(
        "Warning", '<tspan class="warn">Warning</tspan>')
    return (f'<text x="{PAD}" y="{y(row)}" class="in" '
            f'style="animation-delay:{delay - AT:.2f}s">{text}</text>')


def cursor(typed, begin, duration):
    """A cursor after `typed` characters, visible only for `duration`."""
    ghost = escape(PROMPT + COMMAND[:typed])
    return (f'<text x="{PAD}" y="{y(0)}" class="cur" '
            f'style="animation-duration:{duration:.2f}s;animation-delay:{begin - AT:.2f}s">'
            f'<tspan class="ghost">{ghost}</tspan><tspan class="block">█</tspan></text>')


n = len(COMMAND)
typed = "".join(
    f'<tspan class="in" style="animation-delay:{START + i * PER_CHAR - AT:.2f}s">'
    f'{escape(c)}</tspan>' for i, c in enumerate(COMMAND))
enter = START + n * PER_CHAR + AFTER_ENTER

body = [f'<text x="{PAD}" y="{y(0)}">{PROMPT_SVG}{typed}</text>',
        cursor(0, 0, START)]
body += [cursor(k, START + (k - 1) * PER_CHAR, PER_CHAR) for k in range(1, n)]
body.append(cursor(n, START + (n - 1) * PER_CHAR, PER_CHAR + AFTER_ENTER))

t = enter
body += [line(1 + i, s, t) for i, s in enumerate(OUTPUT)]
for i, s in enumerate(EVENTS):
    t += PER_EVENT
    body.append(line(1 + len(OUTPUT) + i, s, t))
t += 0.3
body.append(
    f'<text x="{PAD}" y="{y(1 + len(OUTPUT) + len(EVENTS))}" class="in" '
    f'style="animation-delay:{t - AT:.2f}s">{PROMPT_SVG}<tspan class="block">█</tspan></text>')

title = f"{USER} — -zsh — {COLS}×{ROWS}"
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W + 2 * MX} {H + MTOP + MBOT}" width="{W + 2 * MX}" height="{H + MTOP + MBOT}" role="img" aria-label="Terminal: kubectl describe human eliasehmann">
<style>
text {{ font: {FONT}px "SF Mono", SFMono-Regular, ui-monospace, Menlo, Monaco, Consolas, "Liberation Mono", "DejaVu Sans Mono", monospace; fill: #f2f2f2; white-space: pre; }}
.title {{ font: 700 13px -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", "Segoe UI", sans-serif; fill: #b4b4b4; }}
.warn {{ fill: #e5e500; }}
.green {{ fill: #2fd651; }} .cyan {{ fill: #2ee6e6; }} .blue {{ fill: #4a8cff; }} .red {{ fill: #ff5f57; }}
.block {{ fill: #9a9a9a; }}
.ghost {{ fill: transparent; }}
.in {{ opacity: 0; animation: on 0.01s linear forwards; }}
.cur {{ opacity: 0; animation: on linear; }}
@keyframes on {{ from, to {{ opacity: 1; }} }}
@media (prefers-reduced-motion: reduce) {{ .in {{ opacity: 1; animation: none; }} .cur {{ animation: none; }} }}
</style>
<defs>
<clipPath id="win"><rect width="{W}" height="{H}" rx="10"/></clipPath>
<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="8" stdDeviation="9" flood-color="#000" flood-opacity="0.45"/></filter>
</defs>
<g transform="translate({MX} {MTOP})">
<rect width="{W}" height="{H}" rx="10" fill="#1e1e1e" filter="url(#shadow)"/>
<g clip-path="url(#win)">
<rect width="{W}" height="{H}" fill="#1e1e1e"/>
<rect width="{W}" height="{BAR}" fill="#3a3a3c"/>
<rect y="{BAR}" width="{W}" height="1" fill="#000"/>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="9.5" fill="none" stroke="#fff" stroke-opacity="0.16"/>
<circle cx="20" cy="14" r="6" fill="#ff5f57"/><circle cx="40" cy="14" r="6" fill="#febc2e"/><circle cx="60" cy="14" r="6" fill="#28c840"/>
<path transform="translate({W / 2 - 101} 7)" d="M1 2.5A1.5 1.5 0 0 1 2.5 1h3.2l1.6 1.8h6.2A1.5 1.5 0 0 1 15 4.3v6.2a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 1 10.5z" fill="#3b9cf5"/>
<text x="{W / 2 + 10}" y="18.5" text-anchor="middle" class="title">{escape(title)}</text>
<g xml:space="preserve">
{chr(10).join(body)}
</g>
</g>
</svg>
"""
if OUT != "profile.svg":  # a test render
    open(OUT, "w").write(svg)
    raise SystemExit(f"{OUT} written")

# GitHub caches a README image for 5 minutes per file name, so the name
# carries a hash of the content: a new render shows up right away.
import glob
import hashlib
import re

name = f"profile-{hashlib.sha1(svg.encode()).hexdigest()[:7]}.svg"
for old in glob.glob("profile*.svg"):
    os.remove(old)
open(name, "w").write(svg)
readme = open("README.md").read()
open("README.md", "w").write(
    re.sub(r'src="profile[^"]*"', f'src="{name}"', readme))
print(f"{name} written: {W + 2 * MX}x{H + MTOP + MBOT}, settles after {t:.1f} s")
