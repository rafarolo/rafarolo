import io, os, sys, random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_assets import THEMES, SKY, SANS, MONO, OUT, NL

BIG = [("17", "YEARS ON THE JVM"), ("964", "PULL REQUESTS"),
       ("963", "CODE REVIEWS"), ("5", "SECTORS SERVED")]

H = 372
STEP = 15
SEQ = "RAFAEL01"
# Trail lengths are multiples of the sequence, because a column travels exactly its own
# height per loop: any other length puts a jump in the middle of the word at the seam.
LENGTHS = (16, 24)
COLS = 40

# The head is the bright drop, the trail fades behind it. On a light ground a white head
# is invisible, so light runs the same structure with the accent as its brightest tone.
RAIN = {
    "light": dict(head="#08323F", mid="#146A80", tail="#2C7F8C", group="0.34"),
    "dark":  dict(head="#F2FBFD", mid="#A6DCE8", tail="#56AEC2", group="0.55"),
}


def trail(r, length, phase):
    """One column's worth of glyphs, drawn at x=0 and y=0..length*STEP.

    A trail is fully determined by its length and the point of the sequence it starts on,
    which is two lengths against eight phases: sixteen shapes for forty columns, each of
    which drew its own copy twice over. The columns differ by where they sit and how fast
    they fall, and both of those live on the group that references this one."""
    out = []
    for i in range(length):
        ratio = i / float(length - 1)
        y = i * STEP
        # Read down a column and the sequence is always R A F A E L 0 1, in order. Each
        # column enters at its own point; starting every one at R would band the field
        # into rows of a single letter.
        glyph = SEQ[(i + phase) % len(SEQ)]
        if i == length - 1:
            out.append('<text y="%d" fill="%s">%s</text>' % (y, r["head"], glyph))
        elif i >= length - 3:
            out.append('<text y="%d" fill="%s" opacity=".78">%s</text>' % (y, r["mid"], glyph))
        else:
            op = round(ratio ** 1.6, 2)
            # Anything fainter than this is not visible once the group opacity and the
            # mask are applied, so it is weight in the file and nothing else.
            if op >= 0.08:
                out.append('<text y="%d" opacity="%s">%s</text>' % (y, op, glyph))
    return "".join(out)


def banner(t):
    c = THEMES[t]
    rnd = random.Random(11)

    r = RAIN[t]
    columns = []
    for col in range(COLS):
        length = rnd.choice(LENGTHS)
        columns.append((
            10 + col * 25,
            length,
            length * STEP,
            # Three to nine seconds. At four to thirteen the slow half of the field read
            # as drizzle on a still image rather than as rain.
            round(rnd.uniform(3.0, 9.0), 1),
            round(rnd.uniform(-9.0, 0.0), 1),
            rnd.randrange(len(SEQ)),
        ))

    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" width="1000" height="%d" '
         'role="img" aria-label="Rafael Rolo, Specialist and Tech Lead in Capital Markets. '
         '17 years on the JVM, 964 pull requests authored, 963 code reviews for others, '
         'five sectors served.">' % (H, H)]

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

    shapes = sorted(set((length, phase) for _, length, _, _, _, phase in columns))
    for length, phase in shapes:
        p.append('<g id="q%d_%d%s">%s</g>' % (length, phase, t, trail(r, length, phase)))
    p.append('</defs>')

    p.append('<style>'
             '.fade{opacity:0;animation:f .5s ease forwards}'
             '@keyframes f{to{opacity:1}}'
             + "".join('@keyframes d%d{to{transform:translateY(%dpx)}}' % (n, n * STEP)
                       for n in LENGTHS) +
             '@media (prefers-reduced-motion: reduce){'
             '.fade{opacity:1;animation:none}.rain{animation:none}}'
             '</style>')

    p.append('<g clip-path="url(#r%s)">' % t)
    p.append('<rect x="0" y="0" width="1000" height="%d" fill="url(#w%s)"/>' % (H, t))

    p.append('<g mask="url(#m%s)" font-family="%s" font-size="12" fill="%s" opacity="%s">'
             % (t, MONO, r["tail"], r["group"]))
    for x, length, block, dur, delay, phase in columns:
        # The trail is referenced twice, one block above the other, and the column travels
        # exactly one block. The loop is seamless and the column is never off the band --
        # which is what an earlier version got wrong: each drop spent most of its cycle
        # above or below the banner, so at any instant most columns were simply absent.
        p.append('<g transform="translate(%d 0)">'
                 '<g class="rain" style="animation:d%d %ss linear %ss infinite">'
                 '<use href="#q%d_%d%s" y="%d"/><use href="#q%d_%d%s"/></g></g>'
                 % (x, length, dur, delay, length, phase, t, -block, length, phase, t))
    p.append('</g>')

    p.append('<g font-family="%s">' % SANS)
    p.append('<text class="fade" x="60" y="176" font-size="42" font-weight="700" fill="%s" '
             'letter-spacing="-0.6">Rafael Rôlo</text>' % c["ink"])
    p.append('<text class="fade" style="animation-delay:.1s" x="60" y="208" font-size="13" '
             'font-weight="600" fill="%s" letter-spacing="2.6">SPECIALIST &amp; TECH LEAD · '
             'CAPITAL MARKETS</text>' % c["role"])
    p.append('<line class="fade" style="animation-delay:.16s" x1="60" y1="238" x2="940" y2="238" '
             'stroke="%s" stroke-width="1"/>' % c["line"])

    for i, (val, lab) in enumerate(BIG):
        x, d = 60 + i * 228, 0.22 + i * 0.07
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="304" font-size="46" '
                 'font-weight="700" fill="%s" letter-spacing="-1.2">%s</text>' % (d, x, c["ink"], val))
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="328" font-size="12" '
                 'font-weight="600" fill="%s" letter-spacing="1.6">%s</text>'
                 % (d + .05, x + 1, c["mut"], lab))

    p.append('<text class="fade" style="animation-delay:.55s" x="60" y="358" font-size="9.5" '
             'font-weight="600" fill="%s" letter-spacing="1.2">PRIVATE CORPORATE REPOSITORIES · '
             'MEASURED SEPTEMBER 2026</text>' % c["dim"])
    p.append('</g>')

    p.append('<rect x="0" y="0" width="1000" height="5" fill="url(#s%s)"/>' % t)
    p.append('</g></svg>')
    return NL.join(p) + NL


for t in ("light", "dark"):
    io.open(os.path.join(OUT, "banner-%s.svg" % t), "w", encoding="utf-8",
            newline="\n").write(banner(t))
    print("wrote banner-%s.svg" % t)
