import io, os, sys, random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_all import THEMES, SKY, SANS, MONO, OUT, NL

BIG = [("17", "YEARS ON THE JVM"), ("798", "PULL REQUESTS"),
       ("906", "CODE REVIEWS"), ("8", "SECTORS SERVED")]

H = 372
STEP = 15
COLS = 40
TRAIL_MIN, TRAIL_MAX = 15, 24
FALL = H + TRAIL_MAX * STEP

# The head is the bright drop, the trail fades behind it. On a light ground a white head
# is invisible, so light runs the same structure with the accent as its brightest tone.
RAIN = {
    "light": dict(head="#08323F", mid="#146A80", tail="#2C7F8C", group="0.34"),
    "dark":  dict(head="#F2FBFD", mid="#A6DCE8", tail="#56AEC2", group="0.55"),
}


NAME = "RAFAEL"
GLYPHS = "RAFAEL01"
# A handful of columns spell it outright. Any more and the eye reads the texture instead of
# the name set in type above it, which is the one thing the background must not do.
SPELLING_COLUMNS = 5


def banner(t):
    c = THEMES[t]
    rnd = random.Random(11)

    r = RAIN[t]
    columns = []
    keyframe_rules = []
    for col in range(COLS):
        length = rnd.randint(TRAIL_MIN, TRAIL_MAX)
        block = length * STEP
        columns.append((
            10 + col * 25,
            length,
            block,
            round(rnd.uniform(4.0, 13.0), 1),
            round(rnd.uniform(-13.0, 0.0), 1),
            col % (COLS // SPELLING_COLUMNS) == 0,
        ))
        keyframe_rules.append("@keyframes d%d{to{transform:translateY(%dpx)}}" % (col, block))
    keyframes = "".join(keyframe_rules)

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
             '<stop offset="0.30" stop-color="#FFFFFF" stop-opacity="0.92"/>'
             '<stop offset="0.60" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>' % t)
    # userSpaceOnUse, or the mask region is derived from the bounding box of the digits --
    # which sit above the canvas before they fall -- and almost nothing survives it.
    p.append('<mask id="m%s" maskUnits="userSpaceOnUse" x="0" y="0" width="1000" height="%d">'
             '<rect x="0" y="0" width="1000" height="%d" fill="url(#f%s)"/></mask>'
             % (t, H, H, t))
    p.append('<clipPath id="r%s"><rect x="0" y="0" width="1000" height="%d" rx="10"/></clipPath>' % (t, H))
    p.append('</defs>')

    p.append('<style>'
             '.fade{opacity:0;animation:f .6s ease forwards}'
             '.rain{animation:fall linear infinite}'
             '@keyframes f{to{opacity:1}}'
             '%s'
             '@media (prefers-reduced-motion: reduce){'
             '.fade{opacity:1;animation:none}.rain{animation:none}}'
             '</style>' % keyframes)

    p.append('<g clip-path="url(#r%s)">' % t)
    p.append('<rect x="0" y="0" width="1000" height="%d" fill="url(#w%s)"/>' % (H, t))

    p.append('<g mask="url(#m%s)" font-family="%s" font-size="12" fill="%s" opacity="%s">'
             % (t, MONO, r["tail"], r["group"]))
    for col, (x, length, block, dur, delay, spells) in enumerate(columns):
        p.append('<g style="animation:d%d %ss linear %ss infinite">' % (col, dur, delay))
        # The trail is emitted twice, one block above the other, and the column travels
        # exactly one block. The loop is seamless and the column is never off the band --
        # which is what the previous version got wrong: each drop spent most of its cycle
        # above or below the banner, so at any instant most columns were simply absent.
        for copy in range(2):
            for i in range(length):
                ratio = i / float(length - 1)
                y = -block + copy * block + i * STEP
                # A spelling column runs the name upward, so the drop's head lands on the
                # last letter and the name is read in the direction it falls.
                glyph = (NAME[(length - 1 - i) % len(NAME)] if spells
                         else rnd.choice(GLYPHS))
                if i == length - 1:
                    p.append('<text x="%d" y="%d" fill="%s">%s</text>'
                             % (x, y, r["head"], glyph))
                elif i >= length - 3:
                    p.append('<text x="%d" y="%d" fill="%s" opacity=".78">%s</text>'
                             % (x, y, r["mid"], glyph))
                else:
                    op = round(ratio ** 1.6, 2)
                    # Anything fainter than this is not visible once the group opacity and
                    # the mask are applied, so it is weight in the file and nothing else.
                    if op < 0.08:
                        continue
                    p.append('<text x="%d" y="%d" opacity="%s">%s</text>'
                             % (x, y, op, glyph))
        p.append('</g>')
    p.append('</g>')

    p.append('<g font-family="%s">' % SANS)
    p.append('<text class="fade" x="60" y="176" font-size="42" font-weight="700" fill="%s" '
             'letter-spacing="-0.6">Rafael Rôlo</text>' % c["ink"])
    p.append('<text class="fade" style="animation-delay:.12s" x="60" y="208" font-size="13" '
             'font-weight="600" fill="%s" letter-spacing="2.6">SPECIALIST &amp; TECH LEAD · '
             'CAPITAL MARKETS</text>' % c["role"])
    p.append('<line class="fade" style="animation-delay:.2s" x1="60" y1="238" x2="940" y2="238" '
             'stroke="%s" stroke-width="1"/>' % c["line"])

    for i, (val, lab) in enumerate(BIG):
        x, d = 60 + i * 228, 0.3 + i * 0.09
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="304" font-size="46" '
                 'font-weight="700" fill="%s" letter-spacing="-1.2">%s</text>' % (d, x, c["ink"], val))
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="328" font-size="12" '
                 'font-weight="600" fill="%s" letter-spacing="1.6">%s</text>'
                 % (d + .06, x + 1, c["mut"], lab))

    p.append('<text class="fade" style="animation-delay:.75s" x="60" y="358" font-size="9.5" '
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
