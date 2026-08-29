import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_all import glass_bg, glass_defs, glass_style, THEMES, SANS, OUT, NL

# year, authored, reviewed, complete year
YEARS = [(2023, 158, 201, True), (2024, 173, 221, True),
         (2025, 217, 278, True), (2026, 251, 206, False)]

DAYS_ELAPSED, DAYS_IN_YEAR = 241, 365

LEFT, RIGHT, BASE, MAXH = 92, 830, 252, 150
BW, GAP = 46, 8
RATE = DAYS_IN_YEAR / float(DAYS_ELAPSED)


def projected(value):
    return int(round(value * RATE))


_peak = max(max(projected(a), projected(r)) if not k else max(a, r) for _, a, r, k in YEARS)
SCALE = MAXH / float(_peak)
SLOT = (RIGHT - LEFT) / float(len(YEARS))


def centre(i):
    return LEFT + SLOT * i + SLOT / 2


def prs(t):
    c = THEMES[t]
    h = 378
    totals = [a + r for _, a, r, _ in YEARS]
    projected_total = projected(YEARS[-1][1]) + projected(YEARS[-1][2])

    alt = ("Pull requests per year, authored and reviewed for others. " +
           "; ".join("%d: %d authored, %d reviewed%s" % (y, a, r, "" if k else ", to 29 August")
                     for y, a, r, k in YEARS))
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" width="1000" height="%d" '
         'role="img" aria-label="%s">' % (h, h, alt)]
    p.append('<defs>' + glass_defs(t, "pr") + '<clipPath id="pr%s"><rect x="0" y="0" width="1000" height="%d" rx="10"/>'
             '</clipPath>'
             '<marker id="ah%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
             'markerHeight="6" orient="auto-start-reverse">'
             '<path d="M0 0L10 5L0 10z" fill="%s"/></marker></defs>' % (t, h, t, c["acc"]))
    p.append('<style>'
             '.b{transform-box:fill-box;transform-origin:50%% 100%%;transform:scaleY(0);'
             'animation:gw .8s cubic-bezier(.2,.85,.25,1) forwards}'
             '.t{opacity:0;animation:fi .45s ease forwards}'
             '@keyframes gw{to{transform:scaleY(1)}}@keyframes fi{to{opacity:1}}'
             '@media (prefers-reduced-motion: reduce){.b{transform:scaleY(1);animation:none}'
             '.t{opacity:1;animation:none}}'
             + glass_style(12) + '</style>')
    p.append('<g clip-path="url(#pr%s)">' % t)
    p.append(glass_bg(t, "pr", 1000, h))
    p.append('<g font-family="%s">' % SANS)

    p.append('<text class="t" x="%d" y="46" font-size="12" font-weight="700" fill="%s" '
             'letter-spacing="1.8">PULL REQUESTS PER YEAR</text>' % (LEFT - 44, c["mut"]))
    p.append('<g class="t" style="animation-delay:.1s">')
    p.append('<circle cx="%d" cy="42" r="5" fill="%s" opacity="0.38"/>' % (RIGHT - 372, c["acc"]))
    p.append('<text x="%d" y="46" font-size="12" fill="%s">authored</text>' % (RIGHT - 360, c["dim"]))
    p.append('<circle cx="%d" cy="42" r="5" fill="%s"/>' % (RIGHT - 272, c["acc"]))
    p.append('<text x="%d" y="46" font-size="12" fill="%s">reviewed for others</text>'
             % (RIGHT - 260, c["dim"]))
    p.append('<rect x="%d" y="36" width="16" height="11" rx="2" fill="none" stroke="%s" '
             'stroke-width="1.6" stroke-dasharray="4 3"/>' % (RIGHT - 96, c["acc"]))
    p.append('<text x="%d" y="46" font-size="12" fill="%s">projection</text>'
             % (RIGHT - 74, c["dim"]))
    p.append('</g>')

    p.append('<line class="t" style="animation-delay:.15s" x1="%d" y1="%d" x2="%d" y2="%d" '
             'stroke="%s" stroke-width="1"/>' % (LEFT - 44, BASE + 1, RIGHT + 44, BASE + 1, c["line"]))

    for i, (year, authored, reviewed, complete) in enumerate(YEARS):
        cx = centre(i)
        d = .3 + i * .12
        for j, (value, solid) in enumerate(((authored, False), (reviewed, True))):
            bh = value * SCALE
            x = cx - BW - GAP / 2 + j * (BW + GAP)
            top = BASE - bh
            if not complete:
                ph = projected(value) * SCALE
                begin = d + .5 + j * .06
                spline = 'calcMode="spline" keySplines="0.25 0.9 0.3 1" fill="freeze"'
                # height and y are animated directly: scaling a stroked rectangle thins its
                # horizontal edges and stretches the dash pattern while it grows.
                p.append('<rect x="%.1f" y="%.1f" width="%d" height="0" rx="3" fill="none" '
                         'stroke="%s" stroke-width="1.6" stroke-dasharray="4 4" opacity="0.85">'
                         '<animate attributeName="height" from="0" to="%.1f" begin="%.2fs" '
                         'dur="1.1s" %s/>'
                         '<animate attributeName="y" from="%d" to="%.1f" begin="%.2fs" '
                         'dur="1.1s" %s/>'
                         '<animate attributeName="stroke-dashoffset" from="0" to="16" '
                         'begin="%.2fs" dur="1.6s" repeatCount="indefinite"/>'
                         '</rect>'
                         % (x, BASE, BW, c["acc"], ph, begin, spline,
                            BASE, BASE - ph, begin, spline, begin + 1.1))
                p.append('<text class="t" style="animation-delay:%.2fs" x="%.1f" y="%d" '
                         'font-size="14" font-weight="700" fill="%s" text-anchor="middle" '
                         'opacity="0.9">%d'
                         '<animate attributeName="y" from="%d" to="%.1f" begin="%.2fs" '
                         'dur="1.1s" %s/></text>'
                         % (begin + .05, x + BW / 2.0, BASE - 9, c["acc"], projected(value),
                            BASE - 9, BASE - ph - 9, begin + .05, spline))
            p.append('<rect class="b" style="animation-delay:%.2fs" x="%.1f" y="%.1f" width="%d" '
                     'height="%.1f" rx="3" fill="%s"%s/>'
                     % (d + j * .06, x, top, BW, bh, c["acc"],
                        "" if solid else ' opacity="0.38"'))
            p.append('<text class="t" style="animation-delay:%.2fs" x="%.1f" y="%.1f" font-size="17" '
                     'font-weight="700" fill="%s" text-anchor="middle">%d</text>'
                     % (d + .3 + j * .06, x + BW / 2.0, top - 11, c["ink"], value))

        label = str(year) if complete else "%d *" % year
        p.append('<text class="t" style="animation-delay:%.2fs" x="%.1f" y="%d" font-size="17" '
                 'font-weight="700" fill="%s" text-anchor="middle">%s</text>'
                 % (d + .35, cx, BASE + 32, c["mut"], label))

    last = YEARS[-1]
    solid_top = BASE - max(last[1], last[2]) * SCALE
    dashed_top = BASE - max(projected(last[1]), projected(last[2])) * SCALE
    ax = RIGHT + 34
    lift = int(round((RATE - 1) * 100))
    p.append('<g class="t" style="animation-delay:1.25s">')
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" '
             'marker-end="url(#ah%s)"/>' % (ax, solid_top, ax, dashed_top + 12, c["acc"], t))
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1" '
             'stroke-dasharray="3 3" opacity="0.5"/>'
             % (ax - 26, solid_top, ax + 6, solid_top, c["dim"]))
    p.append('<text x="%.1f" y="%.1f" font-size="16" font-weight="700" fill="%s">+%d%%</text>'
             % (ax + 14, dashed_top + 20, c["acc"], lift))
    p.append('<text x="%.1f" y="%.1f" font-size="11" fill="%s">if the pace</text>'
             % (ax + 14, dashed_top + 38, c["dim"]))
    p.append('<text x="%.1f" y="%.1f" font-size="11" fill="%s">holds</text>'
             % (ax + 14, dashed_top + 52, c["dim"]))
    p.append('</g>')

    for i in range(len(YEARS) - 1):
        x = (centre(i) + centre(i + 1)) / 2.0
        prev, nxt = YEARS[i], YEARS[i + 1]
        if nxt[3]:
            growth = (prev[1] + prev[2]), (nxt[1] + nxt[2])
            text = "+%d%%" % round((growth[1] - growth[0]) * 100.0 / growth[0])
            fill, weight = c["acc"], "700"
        else:
            text = "8 of 12 months"
            fill, weight = c["dim"], "600"
        p.append('<text class="t" style="animation-delay:%.2fs" x="%.1f" y="%d" font-size="13" '
                 'font-weight="%s" fill="%s" text-anchor="middle">%s</text>'
                 % (1.0 + i * .1, x, BASE + 60, weight, fill, text))

    p.append('<g class="t" style="animation-delay:1.4s">')
    p.append('<rect x="%d" y="%d" width="20" height="11" rx="2" fill="none" stroke="%s" '
             'stroke-width="1.6" stroke-dasharray="4 4"/>' % (LEFT - 44, BASE + 82, c["acc"]))
    p.append('<text x="%d" y="%d" font-size="12" fill="%s">* 2026 counts to 29 August. The dashed '
             'outline is where each bar lands if the pace holds — %d pull requests touched against '
             '%d in 2025.</text>'
             % (LEFT - 16, BASE + 92, c["dim"], projected_total, totals[2]))
    p.append('</g>')

    p.append('</g></g></svg>')
    return NL.join(p) + NL


for t in ("light", "dark"):
    io.open(os.path.join(OUT, "prs-%s.svg" % t), "w", encoding="utf-8",
            newline="\n").write(prs(t))
    print("wrote prs-%s.svg" % t)
