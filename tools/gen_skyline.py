import io, os, sys, random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_all import THEMES, SANS, SERIF, OUT, NL

H = 330
GROUND = 325

# Every band is reserved so nothing flies through anything else.
TEXT_Y = 44          # closing line, roughly 26..52
MOON = (888, 40, 17)  # far right, clear of the centred text
COMET_BAND = (60, 88)  # under the phrase, over the aircraft
PLANE_FROM, PLANE_TO = 108, 148  # descending; fin reaches 16 up, wing 12 down
PLANE_PITCH = 5  # degrees nose down: the path alone is too shallow to read as an approach
ROOFLINE = GROUND - 158

SKY = {
    "light": dict(top="#F7F9FA", horizon="#DCE9ED", far="#AFC4CD", mid="#7F98A3",
                  near="#48626D", win="#B08243", win2="#0E5468", winop=".55",
                  warm=("#B08243", "#C2954E", "#8A6A34"), cool=("#0E5468", "#2C7F8C")),
    "dark":  dict(top="#0A1015", horizon="#16303B", far="#101F27", mid="#0A151B",
                  near="#050C10", win="#C9A468", win2="#56AEC2", winop=".95",
                  warm=("#C9A468", "#F0D79A", "#A8823F"), cool=("#56AEC2", "#8FCEDC")),
}

# Only the front layer is lit. Behind it the buildings are silhouettes, which is what they
# look like at this distance anyway -- and a window on a shape that blends into the sky
# reads as a light with nothing under it.
LAYERS = [("far", 27, 20, 46, 38, 92, False), ("mid", 19, 30, 62, 58, 126, False),
          ("near", 17, 46, 92, 78, 158, True)]

BLINKS = ("bk", "bo", "b3", "b4")


def darken(hexcol, f):
    r, g, b = int(hexcol[1:3], 16), int(hexcol[3:5], 16), int(hexcol[5:7], 16)
    return "#%02X%02X%02X" % (int(r * f), int(g * f), int(b * f))


def plane(t, k, ident, delay, flip):
    """Two aircraft on one cycle, each flying half of it in opposite directions, so the
    sky is not the same shot on a loop."""
    blue = THEMES[t]["acc"] if t == "light" else "#7FC6D6"
    # A side profile against the horizon: the wing reads as a swept shape below the
    # fuselage and the fin rises at the tail. Seen from above the wings sit either side of
    # the body and the whole thing flattens into a cross.
    body = (
            # The far wing first, behind the fuselage: a short stub on the other side, dimmer
            # for the distance. Without it the aircraft has one wing and reads as a paper dart.
            '<path d="M25 -2.4 L17 -9 L22 -9 L31 -2.8 Z" fill="#FFFFFF" opacity="0.55"/>'
            '<path d="M23 2.4 L12 12 L18.5 12 L31 3.2 Z" fill="#FFFFFF" opacity="0.92"/>'
            '<ellipse cx="19" cy="7" rx="4" ry="2.2" fill="#FFFFFF" opacity="0.92"/>'
            '<path d="M3 -3.6 L0 -16 L5.5 -16 L12 -3.6 Z" fill="#FFFFFF"/>'
            '<path d="M3 2.2 L-4 8 L2 8 L9.5 3.2 Z" fill="#FFFFFF" opacity="0.92"/>'
            '<path d="M4 -4 L30 -4 Q40 -3.2 42 0 Q40 3.2 30 4 L4 4 Q0 3 0 0 Q0 -3 4 -4 Z" '
            'fill="#FFFFFF"/>'
            '<path d="M8 -1 L34 -1" stroke="%s" stroke-width="1.5" stroke-linecap="round"/>'
            '<circle cx="2" cy="-16" r="1.5" fill="%s">'
            '<animate attributeName="opacity" values="1;0.1;1" dur="1.4s" repeatCount="indefinite"/>'
            '</circle>'
            '<circle cx="14" cy="12" r="1.4" fill="%s">'
            '<animate attributeName="opacity" values="0.1;1;0.1" dur="1.4s" repeatCount="indefinite"/>'
            '</circle>' % (blue, blue, blue))
    # Pitched nose down. Inside the mirrored group a positive rotation renders as a
    # negative one, which is nose down for an aircraft pointing the other way -- so the
    # same value serves both legs.
    pitched = '<g transform="rotate(%d)">%s</g>' % (PLANE_PITCH, body)
    inner = '<g transform="scale(-1 1)">%s</g>' % pitched if flip else pitched
    x0, x1 = (1070, -70) if flip else (-70, 1070)
    y0, y1 = PLANE_FROM, PLANE_TO  # both legs descend; one aircraft climbing away
                                   # and one coming in reads as two unrelated events
    return ('<g opacity="0">'
            '<animate attributeName="opacity" values="0;1;1;0;0" '
            'keyTimes="0;0.005;0.155;0.16;1" begin="%.1fs" dur="120s" repeatCount="indefinite"/>'
            '<animateTransform attributeName="transform" type="translate" '
            'values="%d %d;%d %d;%d %d" keyTimes="0;0.16;1" begin="%.1fs" dur="120s" '
            'repeatCount="indefinite"/>%s</g>'
            % (delay, x0, y0, x1, y1, x1, y1, delay, inner))


def streak(t, name, length, width, cycle, runs):
    """SMIL cannot roll a die, so the variety is written in: several crossings at different
    heights and angles inside one long cycle, parked off screen between them."""
    dy = int(length * 0.55)
    n = len(runs)
    slot, travel = 1.0 / n, 0.035
    pos, times, fade, ftimes = [], [], [], []
    for j, (x0, y0, x1, y1) in enumerate(runs):
        base = j * slot
        pos += ["%d %d" % (x0, y0), "%d %d" % (x1, y1), "%d %d" % (x1, y1)]
        times += ["%.4f" % base, "%.4f" % (base + travel), "%.4f" % (base + slot - 0.001)]
        fade += ["0", "1", "1", "0"]
        ftimes += ["%.4f" % base, "%.4f" % (base + travel * 0.16),
                   "%.4f" % (base + travel * 0.82), "%.4f" % (base + travel)]
    pos.append(pos[-1]); times.append("1")
    fade.append("0"); ftimes.append("1")
    return ('<g opacity="0">'
            '<line x1="0" y1="0" x2="%d" y2="%d" stroke="url(#%s%s)" stroke-width="%.1f" '
            'stroke-linecap="round"/>'
            '<circle cx="%d" cy="%d" r="%.1f" fill="#FFFFFF"/>'
            '<animate attributeName="opacity" values="%s" keyTimes="%s" dur="%.1fs" '
            'repeatCount="indefinite"/>'
            '<animateTransform attributeName="transform" type="translate" values="%s" '
            'keyTimes="%s" dur="%.1fs" repeatCount="indefinite"/>'
            '</g>' % (length, dy, name, t, width, length, dy, width * 0.85,
                      ";".join(fade), ";".join(ftimes), cycle,
                      ";".join(pos), ";".join(times), cycle))


def skyline(t):
    rnd = random.Random(7)
    c, k = THEMES[t], SKY[t]
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" width="1000" '
         'height="%d" role="img" aria-label="To an artificial mind, all reality is virtual. '
         'A city skyline at dusk under a moon, with an aircraft crossing.">' % (H, H)]

    p.append('<defs>')
    p.append('<linearGradient id="sky%s" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
             '</linearGradient>' % (t, k["top"], k["horizon"]))
    p.append('<linearGradient id="st%s" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (t, c["g0"], c["g1"], c["g2"]))
    for name in ("shooting", "comet"):
        p.append('<linearGradient id="%s%s" x1="0" y1="0" x2="1" y2="1">'
                 '<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
                 '<stop offset="0.6" stop-color="#DCEEF6" stop-opacity="0.45"/>'
                 '<stop offset="1" stop-color="#FFFFFF" stop-opacity="1"/></linearGradient>'
                 % (name, t))
    p.append('<clipPath id="sc%s"><rect x="0" y="0" width="1000" height="%d" rx="10"/>'
             '</clipPath>' % (t, H))
    p.append('</defs>')

    p.append('<style>'
             '.st{animation-name:tw;animation-timing-function:ease-in-out;'
             'animation-iteration-count:infinite;animation-direction:alternate}'
             '.st2{animation-name:tw2;animation-timing-function:ease-in-out;'
             'animation-iteration-count:infinite;animation-direction:alternate}'
             + "".join('.%s{animation-name:%s;animation-timing-function:ease-in-out;'
                       'animation-iteration-count:infinite}' % (b, b) for b in BLINKS) +
             '.bl{animation:bl 2.6s step-end infinite}'
             '.ft{opacity:0;animation:ftin .9s ease .2s forwards}'
             '@keyframes tw{0%,100%{opacity:.85}50%{opacity:.32}}'
             '@keyframes tw2{0%,100%{opacity:.42}38%{opacity:.88}}'
             # Every transition is a ramp, and the flats between them are long enough that
             # the window is off or on rather than permanently crossfading.
             '@keyframes bk{0%,46%{opacity:1}58%,94%{opacity:.05}100%{opacity:1}}'
             '@keyframes bo{0%,34%{opacity:.05}44%,88%{opacity:1}100%{opacity:.05}}'
             '@keyframes b3{0%,17%{opacity:1}26%,44%{opacity:.05}53%,71%{opacity:1}'
             '80%,96%{opacity:.05}100%{opacity:1}}'
             '@keyframes b4{0%,9%{opacity:.05}19%,29%{opacity:1}38%,77%{opacity:.05}'
             '86%,96%{opacity:1}100%{opacity:.05}}'
             '@keyframes bl{50%{opacity:.15}}'
             '@keyframes ftin{to{opacity:1}}'
             '@media (prefers-reduced-motion: reduce){'
             '.st,.st2,.bk,.bo,.b3,.b4,.bl{animation:none}.ft{opacity:1;animation:none}}'
             '</style>')

    p.append('<g clip-path="url(#sc%s)">' % t)
    p.append('<rect x="0" y="0" width="1000" height="%d" fill="url(#sky%s)"/>' % (H, t))

    if t == "dark":
        mx, my, mr = MOON
        placed = 0
        while placed < 34:
            x, y = rnd.randint(14, 986), rnd.randint(6, ROOFLINE - 16)
            if (x - mx) ** 2 + (y - my) ** 2 < 46 * 46:
                continue
            if 250 < x < 750 and TEXT_Y - 22 < y < TEXT_Y + 12:
                continue
            period = round(rnd.uniform(7.0, 20.0), 1)
            p.append('<circle class="%s" style="animation-duration:%ss;animation-delay:-%.1fs" '
                     'cx="%d" cy="%d" r="%.1f" fill="#C8DCE6"/>'
                     % (rnd.choice(("st", "st2")), period, rnd.uniform(0, period),
                        x, y, rnd.uniform(.6, 1.5)))
            placed += 1

        # A warm disc and its craters. Nothing behind it and nothing cutting it.
        p.append('<circle cx="%d" cy="%d" r="%d" fill="#F4EBC4"/>' % (mx, my, mr))
        for dx, dy, r in ((5, 4, 3.0), (-6, -3, 2.1), (2, -8, 1.5),
                          (-2, 7, 1.7), (9, -5, 1.2), (-8, 6, 1.1)):
            p.append('<circle cx="%d" cy="%d" r="%.1f" fill="#D9CB99" opacity="0.7"/>'
                     % (mx + dx, my + dy, r))

        lo, hi = COMET_BAND
        p.append(streak(t, "shooting", 52, 1.9, 74.0,
                        ((52, -20, 236, 40), (16, -14, 190, 34), (96, -24, 254, 26))))
        p.append(streak(t, "comet", 104, 3.0, 173.0,
                        ((-130, lo, 470, hi), (250, hi, 900, lo), (-90, hi - 6, 640, lo + 4))))

    for name, count, wmin, wmax, hmin, hmax, lit in LAYERS:
        if name == "near":
            col = k["mid"]
            deck_y, x0, x1, mast = GROUND - 34, 548, 918, 742
            top = GROUND - 168
            p.append('<rect x="%d" y="%d" width="%d" height="5" fill="%s"/>' % (x0, deck_y, x1 - x0, col))
            p.append('<rect x="%d" y="%d" width="6" height="%d" fill="%s"/>'
                     % (mast - 3, top, deck_y - top + 5, col))
            for step in range(1, 8):
                span = step * 24
                for side in (-1, 1):
                    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" '
                             'stroke-width="1.1" opacity="0.85"/>'
                             % (mast, top + 10, mast + side * span, deck_y, col))
            for pier in (x0 + 40, x1 - 40):
                p.append('<rect x="%d" y="%d" width="7" height="%d" fill="%s"/>'
                         % (pier, deck_y, GROUND - deck_y, col))
            p.append('<circle class="bl" cx="%d" cy="%d" r="2.2" fill="%s"/>'
                     % (mast, top - 4, k["win"]))

        col, x = k[name], -20
        while x < 1010 and count > 0:
            bw, bh = rnd.randint(wmin, wmax), rnd.randint(hmin, hmax)
            btop = GROUND - bh
            p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, btop, bw, bh, col))
            if name == "near" and bh > 130 and rnd.random() < .6:
                ax = x + bw // 2
                p.append('<rect x="%d" y="%d" width="2" height="18" fill="%s"/>' % (ax, btop - 18, col))
                p.append('<circle class="bl" style="animation-delay:%.1fs" cx="%d" cy="%d" '
                         'r="2.2" fill="%s"/>' % (rnd.uniform(0, 2), ax + 1, btop - 20, k["win"]))
            if lit:
                unlit = darken(col, .58 if t == "light" else .55)
                # Inset from every edge. Flush against a silhouette that blends into the
                # sky, a window stops reading as part of the building it is on.
                for wx in range(x + 10, x + bw - 12, 12):
                    for wy in range(btop + 16, GROUND - 12, 14):
                        r = rnd.random()
                        if r > .52:
                            p.append('<rect x="%d" y="%d" width="4" height="5" fill="%s"/>'
                                     % (wx, wy, unlit))
                            continue
                        fill = k["win2"] if r < .11 else k["win"]
                        if r < .32:
                            period = round(rnd.uniform(2.2, 10.0), 1)
                            palette = k["cool"] if r < .11 else k["warm"]
                            shifts = ""
                            if r < .17:
                                # A light that changes colour as well as state: someone
                                # switching from a lamp to a screen, which is what a window
                                # at night actually does.
                                order = list(palette) + [palette[0]]
                                keys = ";".join("0.42 0 0.58 1" for _ in order[:-1])
                                shifts = ('<animate attributeName="fill" values="%s" '
                                          'calcMode="spline" keySplines="%s" dur="%.1fs" '
                                          'repeatCount="indefinite"/>'
                                          % (";".join(order), keys, period * 2.7))
                            p.append('<rect class="%s" style="animation-duration:%ss;'
                                     'animation-delay:-%.1fs" x="%d" y="%d" width="4" height="5" '
                                     'fill="%s">%s</rect>'
                                     % (rnd.choice(BLINKS), period, rnd.uniform(0, period),
                                        wx, wy, fill, shifts))
                        else:
                            p.append('<rect x="%d" y="%d" width="4" height="5" fill="%s" '
                                     'opacity="%s"/>' % (wx, wy, fill, k["winop"]))
            x += bw + rnd.randint(3, 14)
            count -= 1

    p.append(plane(t, k, "out", 0.0, False))
    p.append(plane(t, k, "back", 60.0, True))

    p.append('<text class="ft" x="500" y="%d" font-family="%s" font-size="24" '
             'fill="%s" text-anchor="middle">To an artificial mind, '
             'all reality is virtual</text>' % (TEXT_Y, SERIF, c["ink"]))
    p.append('<rect x="0" y="%d" width="1000" height="5" fill="url(#st%s)"/>' % (H - 5, t))
    p.append('</g></svg>')
    return NL.join(p) + NL


for t in ("light", "dark"):
    io.open(os.path.join(OUT, "skyline-%s.svg" % t), "w", encoding="utf-8",
            newline="\n").write(skyline(t))
    print("wrote skyline-%s.svg" % t)

print("text ~26..52 | comet %d..%d | plane %d..%d (wings +-13) | roofline %d"
      % (COMET_BAND[0], COMET_BAND[1], PLANE_TO, PLANE_FROM, ROOFLINE))
