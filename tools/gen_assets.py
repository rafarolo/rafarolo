import io, os, math, random

NL = chr(10)
SERIF = "Georgia, 'Iowan Old Style', 'Times New Roman', Times, serif"

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

THEMES = {
    "light": dict(bg="#F7F9FA", ink="#0E151C", mut="#5A6675", dim="#808C99",
                  acc="#0E5468", role="#0E5468", line="#DDE3E8", track="#DFE6EA",
                  g0="#0E5468", g1="#2C7F8C", g2="#B08243", panel="#EEF2F4"),
    "dark":  dict(bg="#0D1319", ink="#E8EEF2", mut="#94A3AE", dim="#6B7783",
                  acc="#56AEC2", role="#7FC6D6", line="#23303A", track="#1E2932",
                  g0="#56AEC2", g1="#3E93A8", g2="#C9A468", panel="#141C23"),
}

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Mono', Consolas, 'Liberation Mono', monospace"

BIG = [("17", "YEARS ON THE JVM"), ("798", "PULL REQUESTS"), ("906", "CODE REVIEWS"),
       ("8", "SECTORS SERVED")]
YEARS = [("'23", 158, 201), ("'24", 173, 221), ("'25", 217, 278), ("'26", 251, 206)]
SCALE = 58.0 / 278.0
BASE = 196



def shade(hexcol, f):
    r, g, b = int(hexcol[1:3], 16), int(hexcol[3:5], 16), int(hexcol[5:7], 16)
    c = lambda v: max(0, min(255, int(v * f)))
    return "#%02X%02X%02X" % (c(r), c(g), c(b))


GLASS = {
    "light": dict(top=1.022, bottom=0.972, edge="#FFFFFF", edge_op="0.9",
                  sheen="#FFFFFF", sheen_op="0.55", shadow="0.16"),
    "dark":  dict(top=1.30, bottom=0.86, edge="#FFFFFF", edge_op="0.10",
                  sheen="#BFE6F0", sheen_op="0.07", shadow="0.55"),
}


def glass_defs(t, ident, w=1000):
    """One surface treatment shared by every panel, so the page reads as a set.

    A real frosted pane would sample what is behind it, which an SVG in a README cannot
    see. What it can do is behave like glass: a vertical gradient, a lit top edge where
    the light lands, and a slow reflection crossing the surface."""
    g, c = GLASS[t], THEMES[t]
    base = c["panel"]
    return (
        '<linearGradient id="pg%s%s" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
        '<linearGradient id="sn%s%s" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="%s" stop-opacity="0"/>'
        '<stop offset="0.5" stop-color="%s" stop-opacity="%s"/>'
        '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>'
        '<filter id="ds%s%s" x="-30%%" y="-30%%" width="160%%" height="160%%">'
        '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="%s" flood-opacity="%s"/>'
        '</filter>'
        % (ident, t, shade(base, g["top"]), shade(base, g["bottom"]),
           ident, t, g["sheen"], g["sheen"], g["sheen_op"], g["sheen"],
           ident, t, "#000000" if t == "light" else "#000000", g["shadow"])
    )


def glass_style(dur=11):
    return ('.sheen{animation:sweep %ds ease-in-out infinite}'
            '@keyframes sweep{0%%{transform:translateX(-115%%)}'
            '55%%,100%%{transform:translateX(115%%)}}'
            '@media (prefers-reduced-motion: reduce){.sheen{display:none}}' % dur)


def glass_bg(t, ident, w, h):
    g = GLASS[t]
    return (
        '<rect x="0" y="0" width="%d" height="%d" fill="url(#pg%s%s)"/>'
        '<rect class="sheen" x="%d" y="0" width="%d" height="%d" fill="url(#sn%s%s)"/>'
        '<rect x="0" y="0" width="%d" height="1.2" fill="%s" opacity="%s"/>'
        % (w, h, ident, t, -int(w * 0.45), int(w * 0.45), h, ident, t,
           w, g["edge"], g["edge_op"])
    )


RINGS = [(0.88, "88%", "TEST COVERAGE", "core service, up from 74.7%"),
         (0.53, "53%", "OF EVERY PR I TOUCHED", "906 reviews against 798 of my own"),
         (0.89, "89%", "PULL REQUESTS MERGED", "707 merged of 798 opened")]
RR = 46.0
RC = 2 * math.pi * RR
ROW = 40
FRAMES = 14


def ramp(final, n=FRAMES):
    """Values on an ease-out curve, so the counter slows into its answer instead of
    ticking at a constant rate — matching the arc drawn beside it."""
    return [int(round(final * (1 - (1 - i / float(n - 1)) ** 3))) for i in range(n)]


def rings(t):
    c = THEMES[t]
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 212" width="1000" height="212" '
         'role="img" aria-label="Three proportions. Test coverage 88 percent, up from 74.7. '
         '53 percent of every pull request touched belonged to someone else: 906 reviews against '
         '798 of my own. 89 percent of pull requests opened were merged: 707 of 798.">']
    p.append('<defs>' + glass_defs(t, "rg") +
             '<clipPath id="rg%s"><rect x="0" y="0" width="1000" height="212" rx="10"/></clipPath>' % t)
    for i in range(len(RINGS)):
        cx = 190 + i * 310
        p.append('<clipPath id="win%d%s"><rect x="%d" y="%d" width="120" height="%d"/></clipPath>'
                 % (i, t, cx - 60, 86 - ROW // 2 + 4, ROW))
    p.append('</defs>')
    css = ['<style>.lb{opacity:0;animation:fa .5s ease forwards}@keyframes fa{to{opacity:1}}']
    for i, (frac, _, _, _) in enumerate(RINGS):
        css.append('.a%d{stroke-dasharray:%.1f;stroke-dashoffset:%.1f;'
                   'animation:k%d 1.15s cubic-bezier(.25,.9,.3,1) %.2fs forwards}'
                   % (i, RC, RC, i, .25 + i * .16))
        css.append('@keyframes k%d{to{stroke-dashoffset:%.1f}}' % (i, RC * (1 - frac)))
    css.append('@media (prefers-reduced-motion: reduce){.lb{opacity:1;animation:none}')
    for i in range(len(RINGS)):
        css.append('.n%d{animation:none}' % i)
    for i, (frac, _, _, _) in enumerate(RINGS):
        css.append('.a%d{stroke-dashoffset:%.1f;animation:none}' % (i, RC * (1 - frac)))
    for i, (frac, _, _, _) in enumerate(RINGS):
        css.append('.n%d{transform:translateY(%dpx);animation:c%d 1.15s steps(%d,end) %.2fs forwards}'
                   % (i, -(FRAMES - 1) * ROW, i, FRAMES - 1, .25 + i * .16))
        css.append('@keyframes c%d{from{transform:translateY(0)}to{transform:translateY(%dpx)}}'
                   % (i, -(FRAMES - 1) * ROW))
    css.append(glass_style(13))
    css.append('}</style>')
    p.append("".join(css))
    p.append('<g clip-path="url(#rg%s)">' % t)
    p.append(glass_bg(t, "rg", 1000, 212))
    p.append('<g font-family="%s">' % SANS)
    for i, (frac, big, lab, sub) in enumerate(RINGS):
        cx, cy = 190 + i * 310, 86
        p.append('<circle cx="%d" cy="%d" r="%.1f" fill="none" stroke="%s" stroke-width="11"/>'
                 % (cx, cy, RR, c["track"]))
        p.append('<circle class="a%d" cx="%d" cy="%d" r="%.1f" fill="none" stroke="%s" '
                 'stroke-width="11" stroke-linecap="round" filter="url(#dsrg%s)" '
                 'transform="rotate(-90 %d %d)"/>'
                 % (i, cx, cy, RR, c["acc"], t, cx, cy))
        p.append('<g clip-path="url(#win%d%s)"><g class="n%d">' % (i, t, i))
        for step, value in enumerate(ramp(int(big.rstrip("%")))):
            p.append('<text x="%d" y="%d" font-size="30" font-weight="700" fill="%s" '
                     'text-anchor="middle" letter-spacing="-1">%d%%</text>'
                     % (cx, cy + 10 + step * ROW, c["ink"], value))
        p.append('</g></g>')
        p.append('<text class="lb" style="animation-delay:%.2fs" x="%d" y="170" font-size="12" '
                 'font-weight="700" fill="%s" text-anchor="middle" letter-spacing="1.5">%s</text>'
                 % (.7 + i * .12, cx, c["mut"], lab))
        p.append('<text class="lb" style="animation-delay:%.2fs" x="%d" y="189" font-size="12" '
                 'fill="%s" text-anchor="middle">%s</text>' % (.78 + i * .12, cx, c["dim"], sub))
    p.append('</g></g></svg>')
    return "\n".join(p) + "\n"


SKY = {
    "light": dict(top="#F7F9FA", horizon="#DCE9ED", far="#BACDD5", mid="#93AEB9",
                  near="#5F7C88", win="#B08243", win2="#0E5468", winop=".55"),
    "dark":  dict(top="#0A1015", horizon="#16303B", far="#1C3540", mid="#142731",
                  near="#0B161C", win="#C9A468", win2="#56AEC2", winop=".95"),
}
LAYERS = [("far", 27, 20, 46, 38, 92, False), ("mid", 19, 30, 62, 58, 126, True),
          ("near", 12, 46, 92, 78, 158, True)]
GROUND = 255


def dark(hexcol, f):
    r, g, b = int(hexcol[1:3], 16), int(hexcol[3:5], 16), int(hexcol[5:7], 16)
    return "#%02X%02X%02X" % (int(r * f), int(g * f), int(b * f))


def skyline(t):
    rnd = random.Random(7)
    c, k = THEMES[t], SKY[t]
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 260" width="1000" height="260" '
         'role="img" aria-label="A city skyline at dusk, closing the page.">']
    p.append('<defs>')
    p.append('<linearGradient id="sky%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>' % (t, k["top"], k["horizon"]))
    p.append('<linearGradient id="st%s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s"/>'
             '<stop offset="0.55" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
             % (t, c["g0"], c["g1"], c["g2"]))
    p.append('<clipPath id="sc%s"><rect x="0" y="0" width="1000" height="260" rx="10"/></clipPath>' % t)
    p.append('</defs>')
    p.append('<style>.w{animation:tw 4s ease-in-out infinite}.bl{animation:bl 2.6s step-end infinite}'
             '@keyframes tw{0%%,100%%{opacity:%s}45%%{opacity:.16}}@keyframes bl{50%%{opacity:.15}}'
             '.ft{opacity:0;animation:ftin .9s ease .2s forwards}@keyframes ftin{to{opacity:1}}'
             '@media (prefers-reduced-motion: reduce){.w,.bl{animation:none}.ft{opacity:1;animation:none}}</style>' % k["winop"])
    p.append('<g clip-path="url(#sc%s)">' % t)
    p.append('<rect x="0" y="0" width="1000" height="260" fill="url(#sky%s)"/>' % t)
    if t == "dark":
        for _ in range(34):
            p.append('<circle class="w" style="animation-delay:%.1fs" cx="%d" cy="%d" r="%.1f" '
                     'fill="#8FA6B2" opacity=".5"/>'
                     % (rnd.uniform(0, 4), rnd.randint(10, 990), rnd.randint(8, 104), rnd.uniform(.6, 1.3)))
    for name, count, wmin, wmax, hmin, hmax, lit in LAYERS:
        col, x = k[name], -20
        while x < 1010 and count > 0:
            bw, bh = rnd.randint(wmin, wmax), rnd.randint(hmin, hmax)
            top = GROUND - bh
            p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, top, bw, bh, col))
            if name == "near" and bh > 130 and rnd.random() < .6:
                ax = x + bw // 2
                p.append('<rect x="%d" y="%d" width="2" height="18" fill="%s"/>' % (ax, top - 18, col))
                p.append('<circle class="bl" style="animation-delay:%.1fs" cx="%d" cy="%d" r="2.2" '
                         'fill="%s"/>' % (rnd.uniform(0, 2), ax + 1, top - 20, k["win"]))
            if lit:
                unlit = dark(col, .58 if t == "light" else .55)
                for wx in range(x + 7, x + bw - 6, 12):
                    for wy in range(top + 11, GROUND - 8, 14):
                        r = rnd.random()
                        if r > .52:
                            p.append('<rect x="%d" y="%d" width="4" height="5" fill="%s"/>'
                                     % (wx, wy, unlit))
                            continue
                        fill = k["win2"] if r < .11 else k["win"]
                        if r < .13:
                            p.append('<rect class="w" style="animation-delay:%.1fs" x="%d" y="%d" '
                                     'width="4" height="5" fill="%s"/>' % (rnd.uniform(0, 4), wx, wy, fill))
                        else:
                            p.append('<rect x="%d" y="%d" width="4" height="5" fill="%s" opacity="%s"/>'
                                     % (wx, wy, fill, k["winop"]))
            x += bw + rnd.randint(3, 14)
            count -= 1
    p.append('<text class="ft" x="500" y="44" font-family="%s" font-size="24" font-style="italic" fill="%s" text-anchor="middle">To an artificial mind, all reality is virtual.</text>' % (SERIF, c["ink"]))
    p.append('<rect x="0" y="255" width="1000" height="5" fill="url(#st%s)"/>' % t)
    p.append('</g></svg>')
    return "\n".join(p) + "\n"


for t in ("light", "dark"):
    for name, fn in (("rings", rings), ("skyline", skyline)):
        io.open(os.path.join(OUT, "%s-%s.svg" % (name, t)), "w", encoding="utf-8",
                newline="\n").write(fn(t))
    print("wrote banner/rings/archetype/skyline for", t)
