"""Build the Washi theme for T3 Code: washi.json + SVG layers (paper, sumi ink, hanko seal)."""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#2a2622"       # sumi
VERM = "#b3321f"      # hanko vermilion
INDIGO = "#2d5878"    # ai-iro
PAPER = "#f3eee2"
SERIF = '"Iowan Old Style",Palatino,"Palatino Linotype",Georgia,"Hiragino Mincho ProN","Yu Mincho",serif'


def f(x):
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


def data_uri(svg):
    out = svg.replace("%", "%25").replace("#", "%23").replace('"', "'").replace("<", "%3C").replace(">", "%3E")
    return "url(\"data:image/svg+xml," + out + "\")"


# ---------------------------------------------------------------- paper fibres
def fibre_svg(size, freq, seed, rgb, k, bias, octs=3):
    r, g, b = rgb
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{size}' height='{size}'>"
            f"<filter id='a' x='0' y='0' width='100%' height='100%'>"
            f"<feTurbulence type='fractalNoise' baseFrequency='{freq}' numOctaves='{octs}' seed='{seed}' stitchTiles='stitch'/>"
            f"<feColorMatrix values='0 0 0 0 {r} 0 0 0 0 {g} 0 0 0 0 {b} {k} 0 0 0 {bias}'/></filter>"
            f"<rect width='100%' height='100%' filter='url(#a)'/></svg>")


def strands_svg():
    """Short, soft, mostly aligned kozo strands (blurred in-SVG; static)."""
    rnd = random.Random(31)
    out = []
    for _ in range(46):
        x, y = rnd.uniform(0, 700), rnd.uniform(0, 700)
        ang = rnd.uniform(-12, 12) + (90 if rnd.random() < .12 else 0)
        ln = rnd.uniform(80, 200)
        dx, dy = ln * math.cos(math.radians(ang)), ln * math.sin(math.radians(ang))
        bend = rnd.uniform(-14, 14)
        out.append(f"<path d='M{f(x)} {f(y)}q{f(dx / 2 + bend)} {f(dy / 2 - bend)} {f(dx)} {f(dy)}' stroke='#8a7550' stroke-opacity='{rnd.uniform(.08, .14):.2f}' stroke-width='{rnd.uniform(.7, 1.5):.1f}' fill='none' stroke-linecap='round'/>")
    return ("<svg xmlns='http://www.w3.org/2000/svg' width='700' height='700'><defs><filter id='z' x='-5%' y='-5%' width='110%' height='110%'>"
            "<feGaussianBlur stdDeviation='.6'/></filter></defs><g filter='url(#z)'>" + "".join(out) + "</g></svg>")


FIB_H = data_uri(fibre_svg(480, "0.010 0.12", 4, (.5, .42, .28), 4, -3.3, 2))
FIB_V = data_uri(fibre_svg(560, "0.12 0.009", 9, (.55, .46, .32), 4, -3.3, 2))
FIB_S = data_uri(fibre_svg(380, "0.012 0.12", 12, (.45, .37, .25), 4, -3.3, 2))   # sidebar (kozo)
FIB_D = data_uri(fibre_svg(300, "0.6 0.6", 21, (.35, .28, .18), 4, -2.75))   # fine grain, very faint
STRANDS = data_uri(strands_svg())


# ---------------------------------------------------------------- ink bloom (static rasters; grows by transform, satellites wick in over time)
INKC = "#2a2622"
SAT = [(88, 112, 30), (322, 96, 22), (310, 312, 26)]


def _defs():
    return (f"<defs><radialGradient id='g'><stop offset='0' stop-color='{INKC}' stop-opacity='.7'/>"
            f"<stop offset='.4' stop-color='{INKC}' stop-opacity='.42'/><stop offset='.75' stop-color='{INKC}' stop-opacity='.16'/>"
            f"<stop offset='1' stop-color='{INKC}' stop-opacity='0'/></radialGradient>"
            "<filter id='r' x='-30%' y='-30%' width='160%' height='160%'>"
            "<feTurbulence type='fractalNoise' baseFrequency='.014' numOctaves='4' seed='11' result='n'/>"
            "<feDisplacementMap in='SourceGraphic' in2='n' scale='80' xChannelSelector='R' yChannelSelector='G'/></filter>"
            "<filter id='s' x='-30%' y='-30%' width='160%' height='160%'>"
            "<feTurbulence type='fractalNoise' baseFrequency='.03' numOctaves='3' seed='5' result='n'/>"
            "<feDisplacementMap in='SourceGraphic' in2='n' scale='34' xChannelSelector='G' yChannelSelector='R'/></filter></defs>")


def _sat(x, y, r):
    return (f"<circle cx='{x}' cy='{y}' r='{r * 1.9:.0f}' fill='url(#g)' opacity='.8'/><circle cx='{x}' cy='{y}' r='{r}' fill='{INKC}' fill-opacity='.34'/>"
            f"<circle cx='{x}' cy='{y}' r='{r * 1.55:.0f}' fill='none' stroke='{INKC}' stroke-opacity='.4' stroke-width='1.6'/>")


def bloom_svg(which="core"):
    head = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'>" + _defs()
    if which == "core":
        return (head + "<g filter='url(#r)'><circle cx='200' cy='200' r='132' fill='url(#g)'/>"
                f"<circle cx='200' cy='200' r='112' fill='none' stroke='{INKC}' stroke-opacity='.5' stroke-width='3'/>"
                f"<circle cx='200' cy='200' r='88' fill='none' stroke='{INKC}' stroke-opacity='.22' stroke-width='1.5'/></g>"
                f"<g filter='url(#s)'><circle cx='196' cy='198' r='34' fill='{INKC}' fill-opacity='.55'/>"
                f"<circle cx='226' cy='228' r='14' fill='{INKC}' fill-opacity='.4'/></g></svg>")
    if which == "all":
        return head + "<g filter='url(#r)'><circle cx='200' cy='200' r='132' fill='url(#g)'/>" \
            f"<circle cx='200' cy='200' r='112' fill='none' stroke='{INKC}' stroke-opacity='.5' stroke-width='3'/>" \
            f"<circle cx='200' cy='200' r='88' fill='none' stroke='{INKC}' stroke-opacity='.22' stroke-width='1.5'/></g>" \
            f"<g filter='url(#s)'><circle cx='196' cy='198' r='34' fill='{INKC}' fill-opacity='.55'/><circle cx='226' cy='228' r='14' fill='{INKC}' fill-opacity='.4'/>" \
            + "".join(_sat(*t) for t in SAT) + "</g></svg>"
    return head + "<g filter='url(#s)'>" + _sat(*SAT[int(which)]) + "</g></svg>"


# ---------------------------------------------------------------- bamboo (static): tapered culms, pressed-brush leaf clusters
def bamboo_svg():
    rnd = random.Random(7)
    out = []
    stalks = [(50, 500, 40, -20, 13, .62), (112, 470, 124, 60, 7, .46), (156, 440, 146, 170, 5, .3)]
    col = "#2a2622"
    for x0, y0, x1, ytop, w, op in stalks:
        ys, y = [], y0
        while y > ytop + 40:
            y -= rnd.randint(70, 96)
            ys.append(y)
        edges = [y0] + ys + [ytop]

        def xat(yy):
            return x0 + (x1 - x0) * (y0 - yy) / (y0 - ytop)
        # each segment: a slightly tapered quad, wetter (darker) on one side, plus a pale lit side
        for a, b in zip(edges[:-1], edges[1:]):
            wa, wb = w * (1 - .13 * (y0 - a) / (y0 - ytop)), w * (1 - .13 * (y0 - b) / (y0 - ytop)) * .92
            xa, xb = xat(a), xat(b)
            gap = 3
            ya, yb = a - gap * (a != y0), b + gap
            out.append(f"<path d='M{f(xa - wa / 2)} {f(ya)}L{f(xb - wb / 2)} {f(yb)}Q{f(xb)} {f(yb - 2)} {f(xb + wb / 2)} {f(yb)}L{f(xa + wa / 2)} {f(ya)}Z' fill='{col}' fill-opacity='{op * .72:.2f}'/>")
            out.append(f"<path d='M{f(xa - wa * .3)} {f(ya)}L{f(xb - wb * .3)} {f(yb)}' stroke='{col}' stroke-opacity='{min(op * .9, .8):.2f}' stroke-width='{f(max(wa * .28, 1.4))}' fill='none' stroke-linecap='round'/>")
        for yn in ys:
            xn = xat(yn)
            out.append(f"<path d='M{f(xn - w * .7)} {f(yn)}Q{f(xn)} {f(yn - 2.5)} {f(xn + w * .7)} {f(yn)}' stroke='{col}' stroke-opacity='{min(op + .25, .9):.2f}' stroke-width='2' fill='none' stroke-linecap='round'/>")
            # leaf cluster: 3-5 pressed-brush leaves fanning from the node, drooping
            side = rnd.choice((-1, 1))
            for _ in range(rnd.randint(3, 5)):
                ang = (0 if side > 0 else 180) + side * -1 * rnd.randint(-30, 42)
                ln = rnd.randint(30, 58) * (w / 9) ** .8
                lw = ln * rnd.uniform(.14, .2)
                lop = op * rnd.uniform(.7, 1.0)
                out.append(
                    f"<path d='M0 0C{f(ln * .18)} {f(-lw * .6)} {f(ln * .5)} {f(-lw * 1.25)} {f(ln)} {f(lw * .25)}C{f(ln * .55)} {f(lw * .55)} {f(ln * .2)} {f(lw * .35)} 0 0Z' "
                    f"transform='translate({f(xn)} {f(yn)}) rotate({ang})' fill='{col}' fill-opacity='{lop:.2f}'/>")
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 520'>"
            "<defs><linearGradient id='m' x1='0' y1='1' x2='0' y2='0'><stop offset='0' stop-color='#fff' stop-opacity='0'/><stop offset='.25' stop-color='#fff'/><stop offset='.7' stop-color='#fff'/><stop offset='1' stop-color='#fff' stop-opacity='0'/></linearGradient>"
            "<mask id='k'><rect width='200' height='520' fill='url(#m)'/></mask></defs>"
            "<g mask='url(#k)'>" + "".join(out) + "</g></svg>")


# ---------------------------------------------------------------- enso (static + drawn-while-working)
def enso_svg(animated=False):
    """Filled brush enso: heavy wet entry, thinning body, dry-brush exit of split bristle streaks. Eccentric, one stroke."""
    rnd = random.Random(14)
    N = 120
    t0, sweep = math.radians(-70), math.radians(305)

    def centre(u, off=0.0):
        a = t0 + sweep * u
        rx, ry = 70 + off + 3 * math.sin(a * 2 + .6), 63 + off
        # slight spiral inward and tilt
        k = 1 - .06 * u
        x, y = rx * k * math.cos(a), ry * k * math.sin(a)
        c, sn = math.cos(.18), math.sin(.18)
        return 100 + x * c - y * sn, 100 + x * sn + y * c, a

    def width(u):
        return 5 + 15 * math.exp(-((u) / .16) ** 2) + 9 * (1 - u) ** 1.5 - 2.5 * u

    def offs(u, side, w):
        x, y, a = centre(u)
        k = 1 - .06 * u
        nx, ny = math.cos(a), math.sin(a)
        return x + nx * side * w / 2, y + ny * side * w / 2

    main_end = .84
    outer, inner = [], []
    for i in range(N + 1):
        u = main_end * i / N
        w = width(u) * (1 + .08 * math.sin(u * 40))
        outer.append(offs(u, 1, w))
        inner.append(offs(u, -1, w))
    pts = outer + inner[::-1]
    d = "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"
    out = [f"<path d='{d}' fill='{INK}' fill-opacity='.7'/>"]
    # wet entry blob + bloom of ink
    ex, ey, _ = centre(.02)
    out.append(f"<ellipse cx='{f(ex)}' cy='{f(ey)}' rx='13' ry='10' fill='{INK}' fill-opacity='.35' transform='rotate(-30 {f(ex)} {f(ey)})'/>")
    # dry-brush exit: split bristle streaks with paper showing through
    for j in range(5):
        u0 = main_end - .02 + rnd.uniform(0, .03)
        u1 = u0 + rnd.uniform(.08, .15) - j * .004
        side = (j - 2) * 2.2
        ps = []
        for i in range(14):
            u = u0 + (u1 - u0) * i / 13
            x, y, a = centre(u)
            ps.append((x + math.cos(a) * side, y + math.sin(a) * side))
        out.append("<path d='M" + "L".join(f"{f(x)} {f(y)}" for x, y in ps) + f"' fill='none' stroke='{INK}' stroke-opacity='{rnd.uniform(.4, .62):.2f}' stroke-width='{rnd.uniform(1, 1.9):.1f}' stroke-linecap='round'/>")
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><defs><filter id='q' x='-10%' y='-10%' width='120%' height='120%'>"
            "<feTurbulence type='fractalNoise' baseFrequency='.55' numOctaves='2' seed='6' result='n'/>"
            "<feDisplacementMap in='SourceGraphic' in2='n' scale='3' xChannelSelector='R' yChannelSelector='G'/></filter></defs>"
            "<g filter='url(#q)'>" + "".join(out) + "</g></svg>")


# ---------------------------------------------------------------- hanko seal
def seal_svg():
    # 玉 (jade) carved in negative inside a rough-edged vermilion square
    return (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
        "<defs><filter id='w' x='-5%' y='-5%' width='110%' height='110%'>"
        "<feTurbulence type='fractalNoise' baseFrequency='.07' numOctaves='3' seed='3' result='n'/>"
        "<feDisplacementMap in='SourceGraphic' in2='n' scale='3.5' xChannelSelector='R' yChannelSelector='G' result='d'/>"
        "<feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' seed='8' result='t'/>"
        "<feColorMatrix in='t' values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -9 6.2' result='m'/>"
        "<feComposite in='d' in2='m' operator='in'/></filter></defs>"
        f"<g filter='url(#w)'><rect x='6' y='6' width='88' height='88' rx='5' fill='{VERM}'/>"
        "<g fill='none' stroke='#f6efdc' stroke-linecap='square'>"
        "<rect x='12.5' y='12.5' width='75' height='75' rx='2' stroke-width='2.4'/>"
        "<path d='M28 32H72M32 50H68M24 70H76M50 32V70' stroke-width='6.5'/>"
        "<path d='M62 55L68 62' stroke-width='5'/></g></g></svg>")


# ---------------------------------------------------------------- title seal for icon (small ink dot used in rows)
colors = {
    "canvas": PAPER, "chrome": "#ebe4d3", "toolbar": "#ece5d4", "toolbarForeground": "#2b2621",
    "toolbarBorder": "#d3c9b0", "toolbarControl": "#e3dac4", "toolbarControlForeground": "#2b2621",
    "toolbarControlHover": "#d9cfb6", "surface": "#f7f3e8", "surfaceRaised": "#fbf8ef",
    "surfaceOverlay": "#faf6ec", "text": "#28231f", "textMuted": "#5f564a", "border": "#d6ccb5",
    "input": "#c3b79c", "focus": INDIGO, "accent": VERM, "accentForeground": "#fcf7ec",
    "secondary": "#e4dbc6", "secondaryForeground": "#352f28", "muted": "#e8e0cc",
    "mutedForeground": "#5c5347", "placeholder": "#857b6c", "secondaryLabel": "#645b4e",
    "iconMuted": "#6f6558", "error": "#9b1f2b", "errorForeground": "#8a1a25", "errorSurface": "#f2dad2",
    "warning": "#8a5a10", "warningForeground": "#6f4708", "warningSurface": "#f1e2bc",
    "update": INDIGO, "updateForeground": "#244c69", "updateSurface": "#dde5e6",
    "accentSurface": "#efd8ca", "accentSurfaceForeground": "#7a2216", "messageSurface": "#f9f5ea",
    "messageForeground": "#28231f", "messageAction": "#2b2622", "messageActionForeground": "#f6f0e2",
    "messageActionHover": "#463e36", "codeBackground": "#e9e1cd", "codeForeground": "#2c2722",
    "searchMatchBackground": "#efd788", "searchMatchForeground": "#28231f",
    "searchMatchActiveBackground": VERM, "searchMatchActiveForeground": "#fcf7ec",
    "sidebar": "#e9e0cb", "sidebarForeground": "#2b2621", "sidebarMutedForeground": "#554c40",
    "sidebarControlSurface": "#f0e8d5", "sidebarRowHover": "#e0d6bd", "sidebarRowActive": "#d8ccb2",
    "sidebarRowSelected": "#dccfb4", "sidebarBorder": "#cfc3a8", "terminalBackground": "#2a2622",
    "terminalForeground": "#ebe4d3", "terminalCursor": "#e0624b", "terminalSelection": "#4e463d",
    "terminalScrollbar": "#5a5249", "terminalScrollbarHover": "#7d7367",
}

CW = "var(--chat-content-max-width,46rem)"
G = f"(100% - {CW})/2"
BUSY = ('body:has([data-timeline-row-kind="working"])',
        'body:has([data-thread-item] [aria-busy="true"][aria-current]:not([aria-current="false"]))')
SB = "233,224,203"   # sidebar paper rgb


def busy(sel):
    return ",".join(f"{b} {sel}" for b in BUSY)


SCRIM = (f"linear-gradient(90deg,transparent calc(50% - {CW}/2 - 200px),rgba(243,238,226,.78) calc(50% - {CW}/2 - 18px),"
         f"rgba(243,238,226,.78) calc(50% + {CW}/2 + 18px),transparent calc(50% + {CW}/2 + 200px))")
NARROW_SCRIM = ("linear-gradient(90deg,rgba(243,238,226,.7),rgba(243,238,226,.7))")


def gutter_layers(bamboo):
    # right gutter: enso (static); left gutter: bamboo (wide screens only); reading-column scrim on top
    lay = [f"var(--wa-es) right 18px top 52px/min(210px,calc({G} - 36px)) auto no-repeat"]
    if bamboo:
        lay.insert(0, "var(--wa-bam) left 10px bottom 120px/auto min(340px,40%) no-repeat")
    lay.append(SCRIM)
    return ",".join(lay)


def deckle(seed, amp=5, n=7):
    r = random.Random(seed)
    pts = []
    for i in range(n):          # top, left to right
        pts.append(f"{i * 100 / n + r.uniform(0, 3):.0f}% {r.uniform(0, amp):.1f}px")
    pts.append(f"calc(100% - {r.uniform(0, amp):.1f}px) {r.uniform(0, amp):.1f}px")
    for i in range(1, 5):       # right, top to bottom
        pts.append(f"calc(100% - {r.uniform(0, amp):.1f}px) {i * 100 / 5 + r.uniform(-4, 4):.0f}%")
    pts.append(f"calc(100% - {r.uniform(0, amp):.1f}px) calc(100% - {r.uniform(0, amp):.1f}px)")
    for i in range(n - 1, -1, -1):   # bottom, right to left
        pts.append(f"{i * 100 / n + r.uniform(0, 3):.0f}% calc(100% - {r.uniform(0, amp):.1f}px)")
    pts.append(f"{r.uniform(0, amp):.1f}px calc(100% - {r.uniform(0, amp):.1f}px)")
    for i in range(4, 0, -1):   # left, bottom to top
        pts.append(f"{r.uniform(0, amp):.1f}px {i * 100 / 5 + r.uniform(-4, 4):.0f}%")
    return "polygon(" + ",".join(pts) + ")"


BAM_BP = "(min-width:1700px)"
INK_RGBA = "rgba(42,38,34,"

css = (
    ":root{--wa-bam:" + data_uri(bamboo_svg()) + ";--wa-es:" + data_uri(enso_svg(False))
    + ";--wa-bl:" + data_uri(bloom_svg("core")) + ";--wa-b1:" + data_uri(bloom_svg("0")) + ";--wa-b2:" + data_uri(bloom_svg("1")) + ";--wa-b3:" + data_uri(bloom_svg("2")) + ";--wa-ball:" + data_uri(bloom_svg("all")) + ";--wa-seal:" + data_uri(seal_svg()) + ";--wa-enso-sm:" + data_uri(enso_svg(False)) + "}"
    "@property --wa-hw{syntax:'<percentage>';inherits:false;initial-value:0%}"
    "@property --wa-rw{syntax:'<percentage>';inherits:false;initial-value:0%}"
    "@property --wa-s1{syntax:'<percentage>';inherits:false;initial-value:0%}"
    "@property --wa-s2{syntax:'<percentage>';inherits:false;initial-value:0%}"
    "@property --wa-s3{syntax:'<percentage>';inherits:false;initial-value:0%}"
    # ---- paper: sparse fibres + long kozo strands + vignette. Moving art lives on pseudo-elements only.
    # (conversation needs position+isolation so the ink/seal pseudo-elements can sit behind the text but above the paper)
    f"[data-workspace-area=\"conversation\"]{{isolation:isolate;position:relative;background:{FIB_H} 0 0,{FIB_V} 40px 20px,{STRANDS} 0 0,{FIB_D} 0 0,radial-gradient(ellipse at 50% 35%,#f8f4e9 30%,rgba(236,228,208,.7) 100%),{PAPER}!important}}"
    f"[data-workspace-area=\"conversation\"] .messages-timeline-scroll{{background:{gutter_layers(False)}!important}}"
    f"@media {BAM_BP}{{[data-workspace-area=\"conversation\"] .messages-timeline-scroll{{background:{gutter_layers(True)}!important}}}}"
    # ---- ink bloom in the left gutter: a dry stain at rest; spreads over ~9s while a turn runs, then three satellites wick in
    # at 3s, 10s and 20s and the whole stain creeps outward for two minutes (transitions only, nothing resets)
    f"[data-workspace-area=\"conversation\"]::before{{content:\"\";position:absolute;z-index:-1;pointer-events:none;left:calc({G}/2 - min(340px,calc({G} - 20px))/2);top:4%;"
    f"width:min(340px,calc({G} - 20px));aspect-ratio:1;background:var(--wa-b1) center/var(--wa-s1) var(--wa-s1) no-repeat,var(--wa-b2) center/var(--wa-s2) var(--wa-s2) no-repeat,var(--wa-b3) center/var(--wa-s3) var(--wa-s3) no-repeat,var(--wa-bl) center/100% 100% no-repeat;"
    "opacity:.24;transform:scale(.5);scale:1;--wa-s1:0%;--wa-s2:0%;--wa-s3:0%;"
    "transition:transform 3.2s cubic-bezier(.3,.2,.2,1),opacity 2.4s ease-out,scale 3s ease-out,--wa-s1 2.4s ease-out,--wa-s2 2.4s ease-out,--wa-s3 2.4s ease-out}"
    + busy('[data-workspace-area="conversation"]::before') + "{opacity:.9;transform:scale(1);scale:1.16;--wa-s1:100%;--wa-s2:100%;--wa-s3:100%;will-change:transform,opacity;"
    "transition:transform 9s cubic-bezier(.15,.7,.25,1),opacity 1.6s ease-out,scale 150s cubic-bezier(.1,.6,.3,1),--wa-s1 12s ease-out 3s,--wa-s2 14s ease-out 10s,--wa-s3 16s ease-out 20s;animation:wa-drift 52s ease-in-out infinite}"
    "@keyframes wa-drift{0%,100%{rotate:0deg}30%{rotate:4deg}70%{rotate:-4deg}}"
    # ---- hanko seal in the right gutter: lifted while working, stamped when the turn completes
    f"[data-workspace-area=\"conversation\"]::after{{content:\"\";position:absolute;z-index:-1;pointer-events:none;right:calc({G}/2 - 36px - 4px);bottom:150px;width:72px;height:72px;"
    "background:var(--wa-seal) center/100% 100% no-repeat;opacity:.94;transform:rotate(-5deg) scale(1);border-radius:5px;"
    "transition:transform .4s cubic-bezier(.16,1.4,.4,1) .35s,opacity .12s linear .35s;animation:wa-press 1.3s ease-out .72s backwards}"
    "@keyframes wa-press{0%{box-shadow:0 0 0 0 rgba(122,34,22,.25)}100%{box-shadow:0 0 0 14px rgba(122,34,22,0)}}"
    + busy('[data-workspace-area="conversation"]::after') + "{opacity:0;transform:translateY(-22px) rotate(-14deg) scale(1.55);transition:transform .7s ease-in,opacity .6s ease-in;animation:none}"
    # ---- sidebar: kozo paper
    f"[data-slot=\"sidebar-inner\"]{{isolation:isolate;position:relative;font-family:{SERIF};background:linear-gradient(rgba({SB},.55),rgba({SB},.55)),{FIB_S} 0 0,{FIB_D} 30px 10px,rgb({SB})!important}}"
    "[data-slot=\"sidebar-inner\"]::before,[data-slot=\"sidebar-inner\"]::after{display:none}"
    # ---- narrow: no gutters, so a small ink + seal + enso dock sits in the sidebar's top band (beside the window controls),
    # which holds no thread text however long the list gets
    "@media (max-width:1459px){"
    "[data-workspace-area=\"conversation\"]::before,[data-workspace-area=\"conversation\"]::after{display:none}"
    "[data-workspace-area=\"conversation\"] .messages-timeline-scroll{background:transparent!important}"
    f"[data-workspace-area=\"conversation\"]{{background:linear-gradient(rgba(243,238,226,.8),rgba(243,238,226,.8)),{FIB_H} 0 0,{FIB_V} 40px 20px,{STRANDS} 0 0,{FIB_D} 0 0,radial-gradient(ellipse at 50% 35%,#f8f4e9 30%,rgba(236,228,208,.7) 100%),{PAPER}!important}}"
    f"[data-slot=\"sidebar-inner\"]{{background:linear-gradient(rgba({SB},.55),rgba({SB},.55)),{FIB_S} 0 0,{FIB_D} 30px 10px,rgb({SB})!important}}"
    "[data-slot=\"sidebar-inner\"]::after{display:block;content:\"\";position:absolute;z-index:-1;pointer-events:none;right:54px;top:8px;width:40px;height:40px;"
    "background:var(--wa-b1) center/var(--wa-s1) var(--wa-s1) no-repeat,var(--wa-bl) center/100% 100% no-repeat;opacity:.2;transform:scale(.6);--wa-s1:0%;"
    "transition:transform 3s ease-out,opacity 2.4s ease-out,--wa-s1 2.4s ease-out}"
    + busy('[data-slot="sidebar-inner"]::after') + "{opacity:.4;transform:scale(1);--wa-s1:100%;transition:transform 8s cubic-bezier(.15,.7,.25,1),opacity 1.6s ease-out,--wa-s1 10s ease-out 3s}"
    "[data-slot=\"sidebar-inner\"]::before{display:block;content:\"\";position:absolute;z-index:-1;pointer-events:none;right:14px;top:12px;width:28px;height:28px;border-radius:3px;"
    "background:var(--wa-seal) center/100% 100% no-repeat;opacity:.94;transform:rotate(-5deg) scale(1);"
    "transition:transform .4s cubic-bezier(.16,1.4,.4,1) .35s,opacity .12s linear .35s;animation:wa-press 1.3s ease-out .72s backwards}"
    + busy('[data-slot="sidebar-inner"]::before') + "{opacity:0;transform:translateY(-10px) rotate(-14deg) scale(1.5);transition:transform .7s ease-in,opacity .6s ease-in;animation:none}"
    "}"
    # ---- header: serif title; a brush line is drawn under it (registered property, so it can be animated under !important)
    f"[data-chat-header]{{font-family:{SERIF};letter-spacing:.03em;background-color:rgba(236,229,212,.95)!important;"
    f"background-image:linear-gradient(90deg,rgba(42,38,34,0),rgba(42,38,34,.55) 12%,rgba(42,38,34,.4) 70%,rgba(42,38,34,.15)),linear-gradient(rgba(42,38,34,.1),rgba(42,38,34,.1))!important;"
    "background-repeat:no-repeat!important;background-size:var(--wa-hw) 2px,100% 1px!important;background-position:0 100%,0 100%!important;border-bottom:0!important;--wa-hw:0%;transition:--wa-hw 1.2s ease-in}"
    + busy("[data-chat-header]") + "{--wa-hw:100%;transition:--wa-hw 2.4s cubic-bezier(.3,.6,.3,1)}"
    # ---- rows: hover brush stroke; busy = a slow wash passes; selected = a vermilion bar
    "[data-thread-item]{position:relative;border-radius:4px}"
    "[data-thread-item]::after{content:\"\";position:absolute;left:10px;right:10px;bottom:1px;height:2px;pointer-events:none;z-index:2;background:linear-gradient(90deg,rgba(42,38,34,.7),rgba(42,38,34,.1));transform:scaleX(0);transform-origin:left;transition:transform .5s cubic-bezier(.2,.7,.2,1)}"
    "[data-thread-item]:hover::after{transform:scaleX(1)}"
    f"[data-thread-item] [aria-current]:not([aria-current=\"false\"]){{box-shadow:inset 3px 0 {VERM}}}"
    "[data-thread-item] [aria-busy=\"true\"]{background-image:linear-gradient(100deg,transparent,rgba(42,38,34,.1) 50%,transparent)!important;background-size:60% 100%!important;background-repeat:no-repeat!important;background-position:-80% 0;animation:wa-wash 3.2s ease-in-out infinite}"
    "@keyframes wa-wash{to{background-position:180% 0}}"
    # live Working row: a brush line is drawn once (animated registered property), then holds
    "[data-timeline-row-kind=\"working\"]{background-image:linear-gradient(90deg,transparent,rgba(42,38,34,.5) 16%,rgba(42,38,34,.5) 84%,transparent)!important;background-repeat:no-repeat!important;"
    "background-size:var(--wa-rw) 2px!important;background-position:0 100%!important;--wa-rw:0%;animation:wa-brush 2.6s cubic-bezier(.4,0,.3,1) forwards}"
    "@keyframes wa-brush{from{--wa-rw:0%}to{--wa-rw:100%}}"
    f"[data-timeline-row-kind=\"work\"]{{border-left:1px solid rgba(42,38,34,.25);padding-left:10px;font-family:{SERIF}}}"
    # ---- bubbles: pasted paper labels with a deckled edge
    f"[data-user-message-bubble]{{font-family:{SERIF};font-size:1.03em;background:#f9f5ea!important;border:0!important;border-radius:0!important;padding-left:16px!important;"
    "box-shadow:inset 0 0 0 1px rgba(42,38,34,.18),inset 4px 0 0 rgba(179,50,31,.75)!important;"
    f"clip-path:{deckle(5)}}}"
    # ---- composer
    "[data-slot=\"composer-host\"]{background:#f8f4e8!important;border:1px solid rgba(42,38,34,.3)!important;border-top:0!important;border-radius:2px!important;"
    f"background-image:linear-gradient(90deg,rgba(45,88,120,0),{INDIGO} 14%,{INDIGO} 86%,rgba(45,88,120,0)),linear-gradient(90deg,rgba(42,38,34,0),rgba(42,38,34,.7) 8%,rgba(42,38,34,.55) 60%,rgba(42,38,34,.7) 92%,rgba(42,38,34,0))!important;"
    "background-repeat:no-repeat!important;background-size:0 2px,100% 3px!important;background-position:50% 100%,0 0!important;"
    "transition:border-color .2s,background-size .7s cubic-bezier(.2,.7,.2,1)}"
    f"[data-slot=\"composer-host\"]:focus-within{{border-color:{INDIGO}!important;background-size:calc(100% - 16px) 2px,100% 3px!important}}"
    f".composer-tiptap{{font-family:{SERIF};font-size:1.05em}}"
    "[data-slot=\"composer-host\"] :focus-visible,.composer-tiptap:focus-visible{outline:none!important;box-shadow:none!important}"
    # ---- markdown
    f".chat-markdown{{font-family:{SERIF}}}"
    f".chat-markdown :is(h1,h2,h3){{font-family:{SERIF};font-weight:600;letter-spacing:.02em}}"
    ".chat-markdown :is(h1,h2){background:linear-gradient(90deg,rgba(42,38,34,.55),rgba(42,38,34,0)) 0 100%/100% 2px no-repeat;padding-bottom:.28em}"
    ".chat-markdown-codeblock{background:#e9e1cd!important;border:1px solid #d3c8ae!important;border-left:3px solid " + INDIGO + "!important;border-radius:3px!important}"
    ".chat-markdown :not(pre)>code{color:#7a2a1d;background:rgba(42,38,34,.07);padding:.05em .32em;border-radius:3px}"
    f".chat-markdown a{{color:{INDIGO}!important;text-decoration-thickness:1px;text-underline-offset:3px}}"
    ".chat-markdown a:hover{color:" + VERM + "!important}"
    f".chat-markdown blockquote{{border-left:3px solid {VERM};margin-left:0;padding:.1em 0 .1em 1em;color:#4a4136;font-style:italic;background:linear-gradient(90deg,rgba(179,50,31,.06),transparent)}}"
    ".chat-markdown table{border-collapse:collapse}.chat-markdown th{border-bottom:2px solid #2a2622;text-align:left;font-weight:600}"
    ".chat-markdown td{border-bottom:1px solid rgba(42,38,34,.2)}.chat-markdown :is(th,td){padding:.35em .8em .35em 0}"
    ".chat-markdown hr{border:0;height:2px;background:linear-gradient(90deg,transparent,rgba(42,38,34,.55) 20%,rgba(42,38,34,.4) 80%,transparent)}"
    f".chat-markdown li::marker{{color:{VERM}}}"
    "::selection{background:rgba(179,50,31,.2)}"
    # ---- popups
    "[data-slot=\"dialog-popup\"],[data-slot=\"popover-popup\"],[data-slot=\"menu-popup\"]{border-radius:4px!important;border:1px solid #cfc3a8!important;background-image:" + FIB_D + "!important;box-shadow:0 14px 40px -14px rgba(42,38,34,.35)}"
    f"[data-slot=\"dialog-popup\"]{{border-top:3px solid {VERM}!important}}"
    f"[data-slot=\"dialog-popup\"],[data-slot=\"popover-popup\"],[data-slot=\"menu-popup\"],[data-slot=\"tooltip-popup\"],[data-thread-details-card]{{font-family:{SERIF}}}"
    "[data-slot=\"tooltip-popup\"]{border-radius:3px!important;background:#2b2622!important;color:#f6f0e2!important}"
    # ---- controls (hover, active, focus-visible)
    "[data-slot=\"button\"],[data-slot=\"input\"],[data-slot=\"select-trigger\"]{border-radius:4px!important}"
    "[data-slot=\"button\"]:hover{box-shadow:inset 0 0 0 1px rgba(42,38,34,.4)}"
    "[data-slot=\"button\"]:active{transform:translateY(1px);box-shadow:inset 0 2px 4px rgba(42,38,34,.25)}"
    "[data-slot=\"input\"]{background:#faf6ec!important;border-color:#c3b79c!important}"
    f"[data-slot=\"input\"]:focus,[data-slot=\"input\"]:focus-visible,[data-slot=\"select-trigger\"]:focus-visible{{border-color:{INDIGO}!important;box-shadow:0 2px 0 0 {INDIGO}!important;outline:none!important}}"
    "[data-slot=\"select-trigger\"]{background:#faf6ec!important;border-color:#c3b79c!important}[data-slot=\"select-trigger\"]:hover{border-color:#2a2622!important}"
    "[data-slot=\"switch\"]{border:1px solid rgba(42,38,34,.35)!important;background:#ddd3bb!important}"
    "[data-slot=\"switch\"][aria-checked=\"true\"]{background:#2a2622!important;border-color:#2a2622!important}"
    "[data-slot=\"switch\"]>*{background:#f6efdc!important;box-shadow:0 0 0 1px rgba(42,38,34,.3)!important}"
    f":focus-visible{{outline:2px solid {INDIGO};outline-offset:2px}}"
    "svg.lucide{stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}"
    # ---- panels
    f"[data-slot=\"project-monogram\"]{{background:#2a2622!important;color:#f6efdc!important;border-radius:2px!important;font-family:{SERIF};transform:rotate(-3deg)}}"
    "[data-thread-details-card]{background:#f7f3e8!important;border:1px solid #d3c8ae!important;border-radius:4px!important;box-shadow:none!important;border-top:3px solid #2a2622!important}"
    "[data-thread-terminal-drawer]{border-top:3px solid #2a2622!important}"
    f"[data-settings-page-scroll]{{background:{FIB_D} 0 0,{PAPER}!important;font-family:{SERIF}}}"
    # ---- scrollbars
    "::-webkit-scrollbar-track,[data-slot=\"scroll-area-scrollbar\"]{background:transparent!important}"
    "::-webkit-scrollbar-thumb,[data-slot=\"scroll-area-thumb\"]{background:rgba(42,38,34,.22)!important;border-radius:6px!important}"
    "::-webkit-scrollbar-thumb:hover{background:rgba(179,50,31,.45)!important}"
    # ---- reduced motion: freeze to a good still (SVG-internal media queries do not apply, so it is all outer CSS)
    "@media (prefers-reduced-motion:reduce){[data-workspace-area=\"conversation\"]::before,[data-workspace-area=\"conversation\"]::after,[data-slot=\"sidebar-inner\"]::before,[data-slot=\"sidebar-inner\"]::after,"
    "[data-thread-item],[data-thread-item] [aria-busy],[data-timeline-row-kind],[data-slot=\"composer-host\"],[data-chat-header]{transition:none!important;animation:none!important}"
    "[data-workspace-area=\"conversation\"]::before{opacity:.24!important;transform:scale(.5)!important;rotate:0deg!important}"
    + busy('[data-workspace-area="conversation"]::before') + "{opacity:.85!important;transform:scale(1)!important;scale:1.06!important;--wa-s1:100%!important;--wa-s2:100%!important;--wa-s3:100%!important}"
    + busy('[data-workspace-area="conversation"]::after') + "{opacity:.35!important;transform:translateY(-12px) rotate(-10deg) scale(1.15)!important}"
    "[data-slot=\"sidebar-inner\"]::after{opacity:.28!important;transform:scale(.85)!important}"
    + busy('[data-slot="sidebar-inner"]::after') + "{opacity:.4!important;transform:scale(1)!important;--wa-s1:100%!important}"
    + busy('[data-slot="sidebar-inner"]::before') + "{opacity:.35!important;transform:translateY(-4px) rotate(-10deg)!important}"
    "[data-timeline-row-kind=\"working\"]{--wa-rw:100%!important}"
    "body:has([data-timeline-row-kind=\"working\"]) [data-chat-header]{--wa-hw:100%!important}}"
)

theme = {"version": 1, "id": "washi", "name": "Washi", "appearance": "light", "accent": VERM, "canvas": PAPER,
         "colors": colors, "css": css}
out = os.path.join(HERE, "..", "washi.json")
with open(out, "w") as fh:
    json.dump(theme, fh, ensure_ascii=False)
print("css chars:", len(css))
os.makedirs(os.path.join(HERE, "..", "assets", "svg"), exist_ok=True)
for n, s in (("bloom", bloom_svg("all")), ("bamboo", bamboo_svg()), ("enso", enso_svg(False)), ("seal", seal_svg())):
    open(os.path.join(HERE, "..", "assets", "svg", f"{n}.svg"), "w").write(s)
