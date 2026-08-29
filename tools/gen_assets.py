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


# Largest to smallest, so the row reads downhill instead of zig-zagging.
RINGS = [(0.89, "89%", "PULL REQUESTS MERGED", "707 merged of 798 opened"),
         (0.88, "88%", "TEST COVERAGE", "core service, up from 74.7%"),
         (0.53, "53%", "OF EVERY PR I TOUCHED", "906 reviews against 798 of my own")]
RR = 46.0
RC = 2 * math.pi * RR
ROW = 40
FRAMES = 22
# One slow fill, a long hold, then a fade to nothing and round again. The reset happens
# while the arc is invisible, so the loop has no visible snap.
CYCLE = 11.0
FILL_END = 0.26
HOLD_END = 0.93
GONE = 0.985


def ramp(final, n=FRAMES):
    """A steady climb from zero. Linear on purpose: the arc and the head that draws it move
    at a constant rate too, and three things easing differently read as three things that
    are not quite together."""
    return [int(round(final * i / float(n - 1))) for i in range(n)]


def rings(t):
    c = THEMES[t]
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 212" width="1000" height="212" '
         'role="img" aria-label="Three proportions. 89 percent of pull requests opened were '
         'merged, 707 of 798. Test coverage 88 percent, up from 74.7. 53 percent of every pull '
         'request touched belonged to someone else: 906 reviews against 798 of my own.">']
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
                   'animation:k%d %.1fs linear %.2fs infinite}'
                   % (i, RC, RC, i, CYCLE, .25 + i * .3))
        css.append('@keyframes k%d{'
                   '0%%{stroke-dashoffset:%.1f;opacity:1;animation-timing-function:linear}'
                   '%.0f%%{stroke-dashoffset:%.1f;opacity:1}'
                   '%.0f%%{stroke-dashoffset:%.1f;opacity:1}'
                   '%.0f%%{stroke-dashoffset:%.1f;opacity:0}'
                   '100%%{stroke-dashoffset:%.1f;opacity:0}}'
                   % (i, RC, FILL_END * 100, RC * (1 - frac), HOLD_END * 100, RC * (1 - frac),
                      GONE * 100, RC * (1 - frac), RC))
    css.append('@media (prefers-reduced-motion: reduce){.lb{opacity:1;animation:none}')
    for i in range(len(RINGS)):
        css.append('.n%d{animation:none;transform:translateY(%dpx)}' % (i, -(FRAMES - 1) * ROW))
    for i, (frac, _, _, _) in enumerate(RINGS):
        css.append('.a%d{stroke-dashoffset:%.1f;animation:none}' % (i, RC * (1 - frac)))
    for i, (frac, _, _, _) in enumerate(RINGS):
        end = -(FRAMES - 1) * ROW
        css.append('.n%d{animation:c%d %.1fs linear %.2fs infinite}' % (i, i, CYCLE, .25 + i * .3))
        css.append('@keyframes c%d{'
                   '0%%{transform:translateY(0);opacity:1;animation-timing-function:steps(%d,end)}'
                   '%.0f%%{transform:translateY(%dpx);opacity:1}'
                   '%.0f%%{transform:translateY(%dpx);opacity:1}'
                   '%.0f%%{transform:translateY(%dpx);opacity:0}'
                   '100%%{transform:translateY(0);opacity:0}}'
                   % (i, FRAMES - 1, FILL_END * 100, end, HOLD_END * 100, end,
                      GONE * 100, end))
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
        # The bright head that draws the arc, on the same curve and delay as the arc
        # itself, coming to rest exactly where the value does.
        # animateTransform takes the centre of rotation as arguments, so there is no
        # transform-origin to resolve and no transform-box to depend on.
        p.append('<g>')
        angle = 360.0 * frac
        p.append('<animateTransform attributeName="transform" type="rotate" '
                 'values="0 %d %d;%.2f %d %d;%.2f %d %d;0 %d %d" '
                 'keyTimes="0;%.3f;%.3f;1" calcMode="spline" '
                 'keySplines="0 0 1 1;0 0 1 1;0 0 1 1" '
                 'begin="%.2fs" dur="%.1fs" repeatCount="indefinite"/>'
                 % (cx, cy, angle, cx, cy, angle, cx, cy, cx, cy,
                    FILL_END, GONE, .25 + i * .3, CYCLE))
        p.append('<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;%.3f;%.3f;1" '
                 'begin="%.2fs" dur="%.1fs" repeatCount="indefinite"/>'
                 % (HOLD_END, GONE, .25 + i * .3, CYCLE))
        p.append('<circle cx="%d" cy="%.1f" r="11" fill="%s" opacity="0.22"/>'
                 % (cx, cy - RR, c["acc"]))
        p.append('<circle cx="%d" cy="%.1f" r="5.5" fill="#FFFFFF" stroke="%s" '
                 'stroke-width="1.5"/>' % (cx, cy - RR, c["acc"]))
        p.append('</g>')
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
    p.append('<style>.w{animation:tw 4s ease-in-out infinite}'
             '.bk{animation-name:bk;animation-timing-function:step-end;animation-iteration-count:infinite}'
             '.bo{animation-name:bo;animation-timing-function:step-end;animation-iteration-count:infinite}'
             '.bl{animation:bl 2.6s step-end infinite}'
             '@keyframes tw{0%%,100%%{opacity:%s}45%%{opacity:.16}}'
             '@keyframes bk{0%%,58%%{opacity:1}59%%,100%%{opacity:.06}}'
             '@keyframes bo{0%%,44%%{opacity:.06}45%%,100%%{opacity:1}}'
             '@keyframes bl{50%%{opacity:.15}}'
             '.ft{opacity:0;animation:ftin .9s ease .2s forwards}@keyframes ftin{to{opacity:1}}'
             '@media (prefers-reduced-motion: reduce){.w,.bk,.bl,.plane{animation:none}.ft{opacity:1;animation:none}}</style>' % k["winop"])
    p.append('<g clip-path="url(#sc%s)">' % t)
    p.append('<rect x="0" y="0" width="1000" height="260" fill="url(#sky%s)"/>' % t)
    if t == "dark":
        for i in range(58):
            period = round(rnd.uniform(1.8, 7.5), 1)
            p.append('<circle class="%s" style="animation-duration:%ss;animation-delay:-%.1fs" '
                     'cx="%d" cy="%d" r="%.1f" fill="#C8DCE6" opacity=".6"/>'
                     % (rnd.choice(("w", "bk", "bo")), period, rnd.uniform(0, period),
                        rnd.randint(10, 990), rnd.randint(8, 104), rnd.uniform(.6, 1.4)))

        sx, sy = 908, 42
        p.append('<g opacity="0.9">'
                 '<animateTransform attributeName="transform" type="scale" '
                 'values="1;1.35;1" keyTimes="0;0.5;1" additive="sum" dur="4.4s" '
                 'repeatCount="indefinite"/>'
                 '<animate attributeName="opacity" values="0.55;1;0.55" dur="4.4s" '
                 'repeatCount="indefinite"/>'
                 '<path d="M%d %d l3.5 9 l9 3.5 l-9 3.5 l-3.5 9 l-3.5 -9 l-9 -3.5 l9 -3.5 z" '
                 'fill="#FFFFFF" transform="translate(%d %d)"/>'
                 '</g>' % (0, -12, sx, sy))

        # A streak every half minute and something slower and brighter every three, both
        # off screen for almost all of their cycle so they stay events rather than motion.
        for name, length, width, cycle, cross, y0, drop in (
            ("shooting", 74, 1.8, 31.0, 0.030, 26, 96),
            ("comet", 132, 3.0, 97.0, 0.055, 14, 132),
        ):
            p.append('<linearGradient id="%s%s" x1="0" y1="0" x2="1" y2="0">'
                     '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
                     '<stop offset="1" stop-color="#FFFFFF" stop-opacity="1"/></linearGradient>'
                     % (name, t))
            p.append('<g opacity="0">'
                     '<line x1="0" y1="0" x2="%d" y2="%d" stroke="url(#%s%s)" stroke-width="%.1f" '
                     'stroke-linecap="round"/>'
                     '<circle cx="%d" cy="%d" r="%.1f" fill="#FFFFFF"/>'
                     '<animate attributeName="opacity" values="0;1;1;0;0" '
                     'keyTimes="0;0.004;%.3f;%.3f;1" dur="%.1fs" repeatCount="indefinite"/>'
                     '<animateTransform attributeName="transform" type="translate" '
                     'values="-%d %d;1060 %d;1060 %d" keyTimes="0;%.3f;1" '
                     'dur="%.1fs" repeatCount="indefinite"/>'
                     '</g>'
                     % (length, int(length * 0.36), name, t, width,
                        length, int(length * 0.36), width * 0.9,
                        cross * 0.92, cross, cycle,
                        length, y0, y0 + drop, y0 + drop, cross, cycle))
    def bridge():
        col = k["mid"]
        deck_y = GROUND - 34
        x0, x1, mast = 548, 918, 742
        top = GROUND - 168
        out = ['<g>']
        out.append('<rect x="%d" y="%d" width="%d" height="5" fill="%s"/>'
                   % (x0, deck_y, x1 - x0, col))
        out.append('<rect x="%d" y="%d" width="6" height="%d" fill="%s"/>'
                   % (mast - 3, top, deck_y - top + 5, col))
        for step in range(1, 8):
            span = step * 24
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.1" '
                       'opacity="0.85"/>' % (mast, top + 10, mast - span, deck_y, col))
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.1" '
                       'opacity="0.85"/>' % (mast, top + 10, mast + span, deck_y, col))
        for pier in (x0 + 40, x1 - 40):
            out.append('<rect x="%d" y="%d" width="7" height="%d" fill="%s"/>'
                       % (pier, deck_y, GROUND - deck_y, col))
        out.append('<circle class="bl" cx="%d" cy="%d" r="2.2" fill="%s"/>' % (mast, top - 4, k["win"]))
        out.append('</g>')
        return "".join(out)

    for name, count, wmin, wmax, hmin, hmax, lit in LAYERS:
        if name == "near":
            p.append(bridge())
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
                        if r < .09:
                            p.append('<rect class="w" style="animation-delay:%.1fs" x="%d" y="%d" '
                                     'width="4" height="5" fill="%s"/>' % (rnd.uniform(0, 4), wx, wy, fill))
                        elif r < .20:
                            # Own period per window: a shared one makes the whole facade
                            # beat in time, which is the opposite of a building at night.
                            period = round(rnd.uniform(2.4, 11.0), 1)
                            p.append('<rect class="%s" style="animation-duration:%ss;'
                                     'animation-delay:-%.1fs" x="%d" y="%d" width="4" height="5" '
                                     'fill="%s"/>'
                                     % (rnd.choice(("bk", "bo")), period,
                                        rnd.uniform(0, period), wx, wy, fill))
                        else:
                            p.append('<rect x="%d" y="%d" width="4" height="5" fill="%s" opacity="%s"/>'
                                     % (wx, wy, fill, k["winop"]))
            x += bw + rnd.randint(3, 14)
            count -= 1
    # Seen from above: fuselage, swept wings and tailplane. At this size a side view
    # loses its wings entirely and reads as a helicopter.
    blue = c["acc"] if t == "light" else "#7FC6D6"
    p.append('<g class="plane">'
             '<path d="M16 -1.2 L7 -13 L11.5 -13 L23 -1.2 Z" fill="#FFFFFF"/>'
             '<path d="M16 1.2 L7 13 L11.5 13 L23 1.2 Z" fill="#FFFFFF"/>'
             '<path d="M4 -1 L0 -6.5 L3 -6.5 L8.5 -1 Z" fill="#FFFFFF"/>'
             '<path d="M4 1 L0 6.5 L3 6.5 L8.5 1 Z" fill="#FFFFFF"/>'
             '<path d="M2 -2.6 L27 -2.6 Q35 0 27 2.6 L2 2.6 Q-1 0 2 -2.6 Z" fill="#FFFFFF"/>'
             '<path d="M6 0 L28 0" stroke="%s" stroke-width="1.4" stroke-linecap="round"/>'
             '<circle cx="8" cy="-13" r="1.5" fill="%s">'
             '<animate attributeName="opacity" values="1;0.1;1" dur="1.4s" '
             'repeatCount="indefinite"/></circle>'
             '<circle cx="8" cy="13" r="1.5" fill="%s">'
             '<animate attributeName="opacity" values="0.1;1;0.1" dur="1.4s" '
             'repeatCount="indefinite"/></circle>'
             '<animateTransform attributeName="transform" type="translate" '
             'values="-70 62;1070 40;1070 40" keyTimes="0;0.16;1" '
             'dur="60s" repeatCount="indefinite"/>'
             '</g>' % (blue, blue, blue))

    p.append('<text class="ft" x="500" y="44" font-family="%s" font-size="24" font-style="italic" fill="%s" text-anchor="middle">To an artificial mind, all reality is virtual.</text>' % (SERIF, c["ink"]))
    p.append('<rect x="0" y="255" width="1000" height="5" fill="url(#st%s)"/>' % t)
    p.append('</g></svg>')
    return "\n".join(p) + "\n"


for t in ("light", "dark"):
    for name, fn in (("rings", rings), ("skyline", skyline)):
        io.open(os.path.join(OUT, "%s-%s.svg" % (name, t)), "w", encoding="utf-8",
                newline="\n").write(fn(t))
    print("wrote banner/rings/archetype/skyline for", t)
