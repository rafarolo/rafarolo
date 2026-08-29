import io, os, sys, random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_all import THEMES, SKY, SANS, MONO, OUT, NL

BIG = [("17", "YEARS ON THE JVM"), ("798", "PULL REQUESTS"),
       ("906", "CODE REVIEWS"), ("8", "SECTORS SERVED")]

H = 300
STEP = 15
COLS = 42
TRAIL_MIN, TRAIL_MAX = 5, 16
FALL = H + TRAIL_MAX * STEP

# The head is the bright drop, the trail fades behind it. On a light ground a white head
# is invisible, so light runs the same structure with the accent as its brightest tone.
RAIN = {
    "light": dict(head="#0B4152", mid="#2C7F8C", tail="#0E5468", group="0.20"),
    "dark":  dict(head="#EAF7FB", mid="#8FCEDC", tail="#56AEC2", group="0.34"),
}


def banner(t):
    c = THEMES[t]
    rnd = random.Random(11)

    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" width="1000" height="%d" '
         'role="img" aria-label="Rafael Rolo, Specialist and Tech Lead in Capital Markets. '
         '17 years on the JVM, 798 pull requests authored, 906 code reviews for others, '
         'eight sectors served.">' % (H, H)]

    p.append('<defs>')
    p.append('<linearGradient id="s%s" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>' % (t, c["g0"], c["g1"], c["g2"]))
    # The footer's sky, reversed. It runs light down to horizon and closes on a strip along
    # its bottom edge; this runs horizon up to light and opens on a strip along its top, so
    # the two bands bracket the page instead of repeating it.
    k = SKY[t]
    p.append('<linearGradient id="w%s" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
             '</linearGradient>' % (t, k["horizon"], k["top"]))
    # Fades the digits out before they reach the figures, so texture never competes with data.
    p.append('<linearGradient id="f%s" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#FFFFFF" stop-opacity="1"/>'
             '<stop offset="0.70" stop-color="#FFFFFF" stop-opacity="0.65"/>'
             '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>' % t)
    p.append('<mask id="m%s"><rect x="0" y="0" width="1000" height="%d" fill="url(#f%s)"/></mask>'
             % (t, H, t))
    p.append('<clipPath id="r%s"><rect x="0" y="0" width="1000" height="%d" rx="10"/></clipPath>' % (t, H))
    p.append('</defs>')

    p.append('<style>'
             '.fade{opacity:0;animation:f .6s ease forwards}'
             '.rain{animation:fall linear infinite}'
             '@keyframes f{to{opacity:1}}'
             '@keyframes fall{to{transform:translateY(%dpx)}}'
             '@media (prefers-reduced-motion: reduce){'
             '.fade{opacity:1;animation:none}.rain{animation:none}}'
             '</style>' % FALL)

    p.append('<g clip-path="url(#r%s)">' % t)
    p.append('<rect x="0" y="0" width="1000" height="%d" fill="url(#w%s)"/>' % (H, t))

    r = RAIN[t]
    p.append('<g mask="url(#m%s)" font-family="%s" font-size="12" opacity="%s">'
             % (t, MONO, r["group"]))
    for col in range(COLS):
        x = 10 + col * 24
        length = rnd.randint(TRAIL_MIN, TRAIL_MAX)
        dur = round(rnd.uniform(3.6, 11.5), 1)
        delay = round(rnd.uniform(-11.5, 0.0), 1)
        top = -length * STEP
        p.append('<g class="rain" style="animation-duration:%ss;animation-delay:%ss">' % (dur, delay))
        for i in range(length):
            # i counts up towards the head, so the trail thins out behind the drop
            ratio = i / float(length - 1) if length > 1 else 1.0
            if i == length - 1:
                fill, op = r["head"], 1.0
            elif i >= length - 3:
                fill, op = r["mid"], 0.72
            else:
                fill, op = r["tail"], round(ratio ** 1.7, 3)
            p.append('<text x="%d" y="%d" fill="%s" opacity="%s">%s</text>'
                     % (x, top + i * STEP, fill, op, rnd.choice("01")))
        p.append('</g>')
    p.append('</g>')

    p.append('<g font-family="%s">' % SANS)
    p.append('<text class="fade" x="60" y="104" font-size="42" font-weight="700" fill="%s" '
             'letter-spacing="-0.6">Rafael Rôlo</text>' % c["ink"])
    p.append('<text class="fade" style="animation-delay:.12s" x="60" y="136" font-size="13" '
             'font-weight="600" fill="%s" letter-spacing="2.6">SPECIALIST &amp; TECH LEAD · '
             'CAPITAL MARKETS</text>' % c["role"])
    p.append('<line class="fade" style="animation-delay:.2s" x1="60" y1="166" x2="940" y2="166" '
             'stroke="%s" stroke-width="1"/>' % c["line"])

    for i, (val, lab) in enumerate(BIG):
        x, d = 60 + i * 228, 0.3 + i * 0.09
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="232" font-size="46" '
                 'font-weight="700" fill="%s" letter-spacing="-1.2">%s</text>' % (d, x, c["ink"], val))
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="256" font-size="12" '
                 'font-weight="600" fill="%s" letter-spacing="1.6">%s</text>'
                 % (d + .06, x + 1, c["mut"], lab))

    p.append('<text class="fade" style="animation-delay:.75s" x="60" y="286" font-size="9.5" '
             'font-weight="600" fill="%s" letter-spacing="1.2">PRIVATE CORPORATE REPOSITORIES · '
             'MEASURED AUGUST 2026</text>' % c["dim"])
    p.append('</g>')

    p.append('<rect x="0" y="0" width="1000" height="5" fill="url(#s%s)"/>' % t)
    p.append('</g></svg>')
    return NL.join(p) + NL


for t in ("light", "dark"):
    io.open(os.path.join(OUT, "banner-%s.svg" % t), "w", encoding="utf-8",
            newline="\n").write(banner(t))
    print("wrote banner-%s.svg" % t)
