import io, os, sys, math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_assets import glass_bg, glass_defs, glass_style, THEMES, SANS, OUT, NL


def esc(v):
    return v.replace("&", "&amp;")

# label, years, share of last 12 months' classified PRs (%), anchor
# Ordered so the two deepest areas sit next to each other: the depth polygon reads as one
# mass instead of two spurs, and the notch where focus drops falls right after its peak.
AXES = [
    ("BACKEND ON THE JVM", 17, 31.6, "middle"),
    ("DATA", 14, 6.8, "start"),
    ("CLOUD & PLATFORM", 7, 14.7, "start"),
    ("SECURITY & IDENTITY", 7, 30.5, "end"),
    ("OBSERVABILITY", 7, 16.3, "end"),
]
MAXY = max(a[1] for a in AXES) * 1.0
MAXS = max(a[2] for a in AXES) * 1.0

CX, CY, R = 296, 232, 138
NOTES = [
    ("Backend on the JVM", "17 years deep, 32% of the last year", "the anchor: deepest, and still the busiest"),
    ("Data", "14 years deep, 7% of the last year", "the longest history, the smallest slice now"),
    ("Security & identity", "7 years deep, 31% of the last year", "the steepest climb of the five"),
]


def pt(i, frac):
    ang = math.radians(-90 + i * (360.0 / len(AXES)))
    return CX + R * frac * math.cos(ang), CY + R * frac * math.sin(ang)


def poly(fracs):
    return " ".join("%.1f,%.1f" % pt(i, f) for i, f in enumerate(fracs))


def radar(t):
    c = THEMES[t]
    h = 470
    depth = [a[1] / MAXY for a in AXES]
    focus = [a[2] / MAXS for a in AXES]

    alt = "Radar comparing depth in years against share of the last twelve months of pull requests. " + \
          "; ".join("%s: %d years, %.0f percent" % (esc(a[0].title()), a[1], a[2]) for a in AXES)
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" width="1000" height="%d" '
         'role="img" aria-label="%s">' % (h, h, alt)]
    p.append('<defs>' + glass_defs(t, "rd") + '<clipPath id="rd%s"><rect x="0" y="0" width="1000" height="%d" rx="10"/>'
             '</clipPath></defs>' % (t, h))
    p.append('<style>'
             '.gr{opacity:0;animation:gi .5s ease .1s forwards}'
             '.pg{transform-box:fill-box;transform-origin:50% 50%;transform:scale(.05);opacity:0;'
             'animation:gw .95s cubic-bezier(.25,.9,.3,1) forwards}'
             '.tx{opacity:0;animation:gi .5s ease forwards}'
             '@keyframes gi{to{opacity:1}}@keyframes gw{to{transform:scale(1);opacity:1}}'
             '@media (prefers-reduced-motion: reduce){.gr,.tx{opacity:1;animation:none}'
             '.pg{transform:scale(1);opacity:1;animation:none}}'
             + glass_style(14) + '</style>')
    p.append('<g clip-path="url(#rd%s)">' % t)
    p.append(glass_bg(t, "rd", 1000, h))
    p.append('<g font-family="%s">' % SANS)

    for ring in (.25, .5, .75, 1.0):
        p.append('<polygon class="gr" points="%s" fill="none" stroke="%s" stroke-width="1" '
                 'opacity="%.2f"/>' % (poly([ring] * len(AXES)), c["line"], 1 if ring == 1 else .8))
    for i in range(len(AXES)):
        x, y = pt(i, 1.0)
        p.append('<line class="gr" x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1" '
                 'opacity="0.7"/>' % (CX, CY, x, y, c["line"]))

    p.append('<polygon class="pg" points="%s" fill="%s" fill-opacity="0.14" stroke="%s" '
             'stroke-width="1.6" stroke-dasharray="5 4" opacity="0.9"/>' % (poly(depth), c["acc"], c["acc"]))
    p.append('<polygon class="pg" style="animation-delay:.22s" points="%s" fill="%s" '
             'fill-opacity="0.34" stroke="%s" stroke-width="2.4"/>' % (poly(focus), c["acc"], c["acc"]))
    for i, f in enumerate(focus):
        x, y = pt(i, f)
        p.append('<circle class="tx" style="animation-delay:%.2fs" cx="%.1f" cy="%.1f" r="4" '
                 'fill="%s"/>' % (.9 + i * .06, x, y, c["acc"]))

    for i, (lab, yrs, share, anchor) in enumerate(AXES):
        x, y = pt(i, 1.0)
        ang = -90 + i * (360.0 / len(AXES))
        ox = 16 if anchor == "start" else (-16 if anchor == "end" else 0)
        oy = -16 if abs(ang + 90) < 1 else (20 if math.sin(math.radians(ang)) > .3 else 6)
        p.append('<text class="tx" style="animation-delay:%.2fs" x="%.1f" y="%.1f" font-size="10.5" '
                 'font-weight="700" fill="%s" text-anchor="%s" letter-spacing="1.2">%s</text>'
                 % (.75 + i * .06, x + ox, y + oy, c["mut"], anchor, esc(lab)))
        p.append('<text class="tx" style="animation-delay:%.2fs" x="%.1f" y="%.1f" font-size="10.5" '
                 'fill="%s" text-anchor="%s">%dy · %.0f%%</text>'
                 % (.8 + i * .06, x + ox, y + oy + 15, c["dim"], anchor, yrs, share))

    lx = 620
    p.append('<text class="tx" style="animation-delay:1.15s" x="%d" y="70" font-size="11" '
             'font-weight="700" fill="%s" letter-spacing="1.6">WHAT THE SHAPE SAYS</text>' % (lx, c["mut"]))
    y = 108
    for i, (title, num, note) in enumerate(NOTES):
        title = esc(title)
        d = 1.2 + i * .1
        p.append('<circle class="tx" style="animation-delay:%.2fs" cx="%d" cy="%d" r="3.5" fill="%s"/>'
                 % (d, lx + 4, y - 5, c["acc"]))
        p.append('<text class="tx" style="animation-delay:%.2fs" x="%d" y="%d" font-size="14" '
                 'font-weight="700" fill="%s">%s</text>' % (d, lx + 18, y, c["ink"], title))
        p.append('<text class="tx" style="animation-delay:%.2fs" x="%d" y="%d" font-size="12" '
                 'fill="%s">%s</text>' % (d + .05, lx + 18, y + 19, c["acc"], num))
        p.append('<text class="tx" style="animation-delay:%.2fs" x="%d" y="%d" font-size="12" '
                 'fill="%s">%s</text>' % (d + .08, lx + 18, y + 37, c["dim"], note))
        y += 76

    p.append('<g class="tx" style="animation-delay:1.5s">')
    p.append('<rect x="%d" y="358" width="26" height="3" fill="%s" opacity="0.55"/>' % (lx, c["acc"]))
    p.append('<text x="%d" y="363" font-size="10.5" fill="%s">depth, years since first use</text>'
             % (lx + 34, c["dim"]))
    p.append('<rect x="%d" y="380" width="26" height="3" fill="%s"/>' % (lx, c["acc"]))
    p.append('<text x="%d" y="385" font-size="10.5" fill="%s">focus, share of the last 12 months</text>'
             % (lx + 34, c["dim"]))
    p.append('<text x="%d" y="412" font-size="9.5" fill="%s">190 of 337 pull requests matched an area '
             'by title</text>' % (lx, c["dim"]))
    p.append('</g>')

    p.append('</g></g></svg>')
    return NL.join(p) + NL


for t in ("light", "dark"):
    io.open(os.path.join(OUT, "radar-%s.svg" % t), "w", encoding="utf-8",
            newline="\n").write(radar(t))
    print("wrote radar-%s.svg" % t)
