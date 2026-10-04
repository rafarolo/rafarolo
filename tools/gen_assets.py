import io, os, math

NL = chr(10)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

THEMES = {
    "light": dict(bg="#F7F9FA", ink="#0E151C", mut="#5A6675", dim="#808C99",
                  acc="#0E5468", role="#0E5468", line="#DDE3E8", track="#D7E3EC",
                  g0="#0E5468", g1="#2C7F8C", g2="#B08243", panel="#EFF4F9",
                  pan0="#FFFFFF", pan1="#DCE8F2"),
    "dark":  dict(bg="#0D1117", ink="#E8EEF2", mut="#94A3AE", dim="#6B7783",
                  acc="#56AEC2", role="#7FC6D6", line="#21303C", track="#1B2B37",
                  g0="#56AEC2", g1="#3E93A8", g2="#C9A468", panel="#131E29",
                  pan0="#0D1117", pan1="#152836"),
}

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Mono', Consolas, 'Liberation Mono', monospace"


GLASS = {
    "light": dict(edge="#FFFFFF", edge_op="0.9",
                  sheen="#FFFFFF", sheen_op="0.55", shadow="0.16"),
    "dark":  dict(edge="#7FC6D6", edge_op="0.16",
                  sheen="#BFE6F0", sheen_op="0.07", shadow="0.55"),
}


def glass_defs(t, ident, w=1000, shadow=False):
    """One surface treatment shared by every panel, so the page reads as a set.

    A real frosted pane would sample what is behind it, which an SVG in a README cannot
    see. What it can do is behave like glass: a vertical gradient, a lit top edge where
    the light lands, and a slow reflection crossing the surface.

    The two stops are named colours rather than one panel colour multiplied up and down.
    Dark starts on GitHub's own canvas, #0D1117, so a panel does not sit on the page as a
    grey card laid over the reading surface, and falls to a blue; light does the same from
    white. The tint used to be grey because both stops came out of one grey.

    The drop shadow is opt-in, and nothing that animates every frame wears it: a filter
    on a moving element is re-rendered on every one of those frames."""
    g, c = GLASS[t], THEMES[t]
    defs = (
        '<linearGradient id="pg%s%s" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
        '<linearGradient id="sn%s%s" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="%s" stop-opacity="0"/>'
        '<stop offset="0.5" stop-color="%s" stop-opacity="%s"/>'
        '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>'
        % (ident, t, c["pan0"], c["pan1"],
           ident, t, g["sheen"], g["sheen"], g["sheen_op"], g["sheen"])
    )
    if shadow:
        defs += ('<filter id="ds%s%s" x="-30%%" y="-30%%" width="160%%" height="160%%">'
                 '<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" '
                 'flood-opacity="%s"/></filter>' % (ident, t, g["shadow"]))
    return defs


SWEEP = 22


def glass_style(offset=0):
    """A pass every twenty-two seconds. Long enough that the page is not glinting at you,
    short enough that a reader who scrolls to one panel and stays there sees it happen.

    translateX on one rect is the cheapest thing on the page, so the interval is a
    question of taste rather than of cost."""
    return ('.sheen{animation:sweep %ds ease-in-out %ds infinite}'
            '@keyframes sweep{0%%{transform:translateX(-115%%)}'
            '17%%,100%%{transform:translateX(115%%)}}'
            '@media (prefers-reduced-motion: reduce){.sheen{display:none}}' % (SWEEP, offset))


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
RINGS = [(0.84, 84, "PULL REQUESTS MERGED", "814 merged of 964 opened"),
         (0.88, 88, "TEST COVERAGE", "core service, up from 74.7%"),
         (0.50, 50, "OF EVERY PR I TOUCHED", "963 reviews against 964 of my own")]
RR = 46.0
RC = 2 * math.pi * RR
# One fill, a hold, then a fade to nothing and round again. The reset happens while the
# arc is invisible, so the loop has no visible snap.
#
# Fifteen seconds, of which the fill is the first one and a half. The cycle used to be a
# minute: the panel spent fifty-six of those sixty seconds frozen, which is the state
# almost anyone scrolling past actually saw.
CYCLE = 15.0
FILL_END = 0.10
HOLD_END = 0.90
GONE = 0.96


def delay(i):
    """One number, shared by all three animations on a ring.

    The arc, the head that draws it and the figure in the middle are one event seen three
    ways. They had three different delays -- .25 + i*1.4 for the arc against .25 + i*.3
    for the head -- so on the second and third rings the head set off a second early and
    came to rest against an arc that had not started."""
    return 0.15 + i * 0.30


def rings(t):
    c = THEMES[t]
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 212" width="1000" height="212" '
         'role="img" aria-label="Three proportions. 84 percent of pull requests opened were '
         'merged, 814 of 964. Test coverage 88 percent, up from 74.7. 50 percent of every pull '
         'request touched belonged to someone else: 963 reviews against 964 of my own.">']
    p.append('<defs>' + glass_defs(t, "rg", shadow=True) +
             '<clipPath id="rg%s"><rect x="0" y="0" width="1000" height="212" rx="10"/></clipPath>' % t)
    p.append('</defs>')

    css = ['.lb{opacity:0;animation:fa .4s ease forwards}@keyframes fa{to{opacity:1}}']
    for i, (frac, _, _, _) in enumerate(RINGS):
        cx, d = 190 + i * 310, delay(i)
        off = RC * (1 - frac)
        ang = 360.0 * frac
        css.append('.a%d{stroke-dasharray:%.1f;stroke-dashoffset:%.1f;'
                   'animation:k%d %.1fs linear %.2fs infinite}'
                   % (i, RC, RC, i, CYCLE, d))
        css.append('@keyframes k%d{0%%{stroke-dashoffset:%.1f;opacity:1}'
                   '%.0f%%{stroke-dashoffset:%.1f;opacity:1}'
                   '%.0f%%{stroke-dashoffset:%.1f;opacity:1}'
                   '%.0f%%{stroke-dashoffset:%.1f;opacity:0}'
                   '100%%{stroke-dashoffset:%.1f;opacity:0}}'
                   % (i, RC, FILL_END * 100, off, HOLD_END * 100, off,
                      GONE * 100, off, RC))
        # The head rides the same clock as the arc it draws. transform-box is set to
        # view-box so the origin below is read in the coordinates the circle is drawn in,
        # rather than against the head's own bounding box.
        css.append('.h%d{transform-box:view-box;transform-origin:%dpx 86px;'
                   'animation:g%d %.1fs linear %.2fs infinite}' % (i, cx, i, CYCLE, d))
        css.append('@keyframes g%d{0%%{transform:rotate(0);opacity:1}'
                   '%.0f%%{transform:rotate(%.2fdeg);opacity:1}'
                   '%.0f%%{transform:rotate(%.2fdeg);opacity:1}'
                   '%.0f%%{transform:rotate(%.2fdeg);opacity:0}'
                   '100%%{transform:rotate(0);opacity:0}}'
                   % (i, FILL_END * 100, ang, HOLD_END * 100, ang, GONE * 100, ang))
        # The figure grew by scrolling sixteen stacked copies of itself past a slot,
        # which is a slot machine: the eye follows the travelling digits instead of the
        # arc, and a strip of numbers sliding behind a window reads as something the
        # reader is meant to be able to scroll. One number now, rising into place on the
        # same clock as the arc, and fifteen text elements per ring lighter.
        css.append('.v%d{transform-box:view-box;transform-origin:%dpx 88px;'
                   'animation:n%d %.1fs linear %.2fs infinite}' % (i, cx, i, CYCLE, d))
        css.append('@keyframes n%d{0%%{opacity:0;transform:scale(.76)}'
                   '%.0f%%{opacity:1;transform:scale(1)}'
                   '%.0f%%{opacity:1;transform:scale(1)}'
                   '%.0f%%{opacity:0;transform:scale(1)}'
                   '100%%{opacity:0;transform:scale(.76)}}'
                   % (i, FILL_END * 100, HOLD_END * 100, GONE * 100))
    # This brace was missing. Everything from here to the end of the block -- the three
    # counters and the sheen -- was declared inside the reduced-motion query and applied
    # to nobody else, so on an ordinary screen the numbers sat on frame zero reading 0%.
    css.append('@media (prefers-reduced-motion: reduce){.lb{opacity:1;animation:none}')
    for i, (frac, _, _, _) in enumerate(RINGS):
        css.append('.a%d{stroke-dashoffset:%.1f;animation:none}' % (i, RC * (1 - frac)))
        css.append('.h%d{transform:rotate(%.2fdeg);animation:none}' % (i, 360.0 * frac))
        css.append('.v%d{opacity:1;transform:none;animation:none}' % i)
    css.append('}')
    css.append(glass_style(6))
    p.append('<style>' + "".join(css) + '</style>')

    p.append('<g clip-path="url(#rg%s)">' % t)
    p.append(glass_bg(t, "rg", 1000, 212))
    p.append('<g font-family="%s">' % SANS)
    for i, (frac, big, lab, sub) in enumerate(RINGS):
        cx, cy = 190 + i * 310, 86
        # The shadow sits under the track, which never moves. On the arc it was
        # re-rendered on every frame of the fill, for a softness that eleven pixels of
        # opaque stroke hide anyway.
        p.append('<circle cx="%d" cy="%d" r="%.1f" fill="none" stroke="%s" stroke-width="11" '
                 'filter="url(#dsrg%s)"/>' % (cx, cy, RR, c["track"], t))
        p.append('<circle class="a%d" cx="%d" cy="%d" r="%.1f" fill="none" stroke="%s" '
                 'stroke-width="11" stroke-linecap="round" transform="rotate(-90 %d %d)"/>'
                 % (i, cx, cy, RR, c["acc"], cx, cy))
        p.append('<g class="h%d">' % i)
        p.append('<circle cx="%d" cy="%.1f" r="11" fill="%s" opacity="0.22"/>'
                 % (cx, cy - RR, c["acc"]))
        p.append('<circle cx="%d" cy="%.1f" r="5.5" fill="#FFFFFF" stroke="%s" '
                 'stroke-width="1.5"/>' % (cx, cy - RR, c["acc"]))
        p.append('</g>')
        p.append('<text class="v%d" x="%d" y="%d" font-size="30" font-weight="700" fill="%s" '
                 'text-anchor="middle" letter-spacing="-1">%d%%</text>'
                 % (i, cx, cy + 10, c["ink"], big))
        p.append('<text class="lb" style="animation-delay:%.2fs" x="%d" y="170" font-size="12" '
                 'font-weight="700" fill="%s" text-anchor="middle" letter-spacing="1.5">%s</text>'
                 % (.5 + i * .1, cx, c["mut"], lab))
        p.append('<text class="lb" style="animation-delay:%.2fs" x="%d" y="189" font-size="12" '
                 'fill="%s" text-anchor="middle">%s</text>' % (.56 + i * .1, cx, c["dim"], sub))
    p.append('</g></g></svg>')
    return NL.join(p) + NL


SKY = {
    "light": dict(top="#F7F9FA", horizon="#DCE9ED", far="#BACDD5", mid="#93AEB9",
                  near="#5F7C88", win="#B08243", win2="#0E5468", winop=".55"),
    "dark":  dict(top="#0A1015", horizon="#16303B", far="#1C3540", mid="#142731",
                  near="#0B161C", win="#C9A468", win2="#56AEC2", winop=".95"),
}


for t in ("light", "dark"):
    io.open(os.path.join(OUT, "rings-%s.svg" % t), "w", encoding="utf-8",
            newline="\n").write(rings(t))
    print("wrote rings-%s.svg" % t)
