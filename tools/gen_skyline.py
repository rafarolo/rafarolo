import io, os, sys, random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_assets import THEMES, SANS, OUT, NL

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
                  star="#5A7784", trail="#2C7F8C", head="#0E5468",
                  moon="#E9DEB0", crater="#C6B686",
                  warm=("#B08243", "#C2954E", "#8A6A34"), cool=("#0E5468", "#2C7F8C")),
    "dark":  dict(top="#0A1015", horizon="#16303B", far="#101F27", mid="#0A151B",
                  near="#050C10", win="#C9A468", win2="#56AEC2", winop=".95",
                  star="#C8DCE6", trail="#DCEEF6", head="#FFFFFF",
                  moon="#F4EBC4", crater="#D9CB99",
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


SKY_CYCLE = 150.0
SLOTS = 6          # the meteor takes the even ones, the comet the odd
TRAVEL = 0.019     # fraction of the cycle a crossing is on screen


def star(cx, cy, r):
    """A four-pointed sparkle for the head of a streak. A dot is a dot; the points are what
    make it read as a star travelling rather than a bead on a wire."""
    a, b = r * 0.29, r * 0.72
    return ("M%.1f %.1f l%.1f %.1f l%.1f %.1f l%.1f %.1f l%.1f %.1f "
            "l%.1f %.1f l%.1f %.1f l%.1f %.1f z"
            % (cx, cy - r, a, b, b, a, -b, a, -a, b, -a, -b, -b, -a, b, -a))


def streak(t, head, name, length, width, slots, runs):
    """One shared cycle with the two objects on alternating slots, so they can never be on
    screen together. Independent cycles drift into each other eventually -- 74 and 173
    seconds coincide sooner than it sounds.

    SMIL cannot roll a die either, so the variety is written in: each crossing has its own
    height and angle, and the object is parked off screen between them."""
    dy = int(length * 0.55)
    pos, times, fade, ftimes = [], [], [], []
    for slot, (x0, y0, x1, y1) in zip(slots, runs):
        base = slot / float(SLOTS)
        pos += ["%d %d" % (x0, y0), "%d %d" % (x1, y1), "%d %d" % (x1, y1)]
        times += ["%.4f" % base, "%.4f" % (base + TRAVEL),
                  "%.4f" % (base + 1.0 / SLOTS - 0.0005)]
        fade += ["0", "1", "1", "0"]
        ftimes += ["%.4f" % base, "%.4f" % (base + TRAVEL * 0.16),
                   "%.4f" % (base + TRAVEL * 0.82), "%.4f" % (base + TRAVEL)]
    if float(times[-1]) < 1:
        pos.append(pos[-1]); times.append("1")
        fade.append("0"); ftimes.append("1")
    return ('<g opacity="0">'
            '<line x1="0" y1="0" x2="%d" y2="%d" stroke="url(#%s%s)" stroke-width="%.1f" '
            'stroke-linecap="round"/>'
            '<path d="%s" fill="%s"/>'
            '<animate attributeName="opacity" values="%s" keyTimes="%s" dur="%.1fs" '
            'repeatCount="indefinite"/>'
            '<animateTransform attributeName="transform" type="translate" values="%s" '
            'keyTimes="%s" dur="%.1fs" repeatCount="indefinite"/>'
            '</g>' % (length, dy, name, t, width, star(length, dy, width * 2.7), head,
                      ";".join(fade), ";".join(ftimes), SKY_CYCLE,
                      ";".join(pos), ";".join(times), SKY_CYCLE))


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
                 '<stop offset="0" stop-color="%s" stop-opacity="0"/>'
                 '<stop offset="0.6" stop-color="%s" stop-opacity="0.45"/>'
                 '<stop offset="1" stop-color="%s" stop-opacity="1"/></linearGradient>'
                 % (name, t, k["trail"], k["trail"], k["head"]))
    p.append('<clipPath id="sc%s"><rect x="0" y="0" width="1000" height="%d" rx="10"/>'
             '</clipPath>' % (t, H))
    p.append('</defs>')

    p.append('<style>'
             + "".join('.st%d{animation-name:tw%d;animation-timing-function:ease-in-out;'
                       'animation-iteration-count:infinite}' % (i, i) for i in range(1, 5))
             + "".join('.%s{animation-name:%s;animation-timing-function:ease-in-out;'
                       'animation-iteration-count:infinite}' % (b, b) for b in BLINKS) +
             '.bl{animation:bl 2.6s step-end infinite}'
             '.ft{opacity:0;animation:ftin .9s ease .2s forwards}'
             # Four rhythms, none of them symmetrical. A star that dims and brightens on a
             # even beat reads as a signal; a real one holds, flickers, holds again.
             # All four run the full range, from all but invisible to solid. Two of them
             # only dipped to a half and read as nothing at this size. The positions stay
             # irregular and every one holds somewhere, so it is still a night sky and not
             # a row of indicator lamps.
             '@keyframes tw1{0%,24%{opacity:1}39%{opacity:.04}55%{opacity:.92}'
             '69%{opacity:.07}85%,100%{opacity:1}}'
             '@keyframes tw2{0%,51%{opacity:1}62%{opacity:.05}77%{opacity:.98}'
             '87%{opacity:.09}100%{opacity:1}}'
             '@keyframes tw3{0%{opacity:.06}17%{opacity:1}43%{opacity:.04}'
             '64%{opacity:.95}82%{opacity:.12}100%{opacity:.06}}'
             '@keyframes tw4{0%,36%{opacity:.97}47%{opacity:.03}58%{opacity:.55}'
             '71%{opacity:1}88%,100%{opacity:.97}}'
             # Every transition is a ramp, and the flats between them are long enough that
             # the window is off or on rather than permanently crossfading.
             '@keyframes bk{0%,46%{opacity:1}58%,94%{opacity:0}100%{opacity:1}}'
             '@keyframes bo{0%,34%{opacity:0}44%,88%{opacity:1}100%{opacity:0}}'
             '@keyframes b3{0%,17%{opacity:1}26%,44%{opacity:0}53%,71%{opacity:1}'
             '80%,96%{opacity:0}100%{opacity:1}}'
             '@keyframes b4{0%,9%{opacity:0}19%,29%{opacity:1}38%,77%{opacity:0}'
             '86%,96%{opacity:1}100%{opacity:0}}'
             '@keyframes bl{50%{opacity:.15}}'
             # Colour as CSS rather than as sixty SMIL animations. Same stops, same easing;
             # SMIL interpolates a paint attribute outside the animation pipeline the rest
             # of this panel already runs in.
             + ''.join('@keyframes %s{%s}' % (name, ''.join(
                 '%d%%{fill:%s}' % (round(100.0 * j / (len(stops) - 1)), col)
                 for j, col in enumerate(list(stops) + [stops[0]])))
                 for name, stops in (('cw', k['warm']), ('cc', k['cool']))) +
             '@keyframes ftin{to{opacity:1}}'
             # Nothing in this panel's CSS moves anything: the windows and the stars only
             # change opacity, and a gentle cross-fade is the sort of thing the reduced
             # motion setting is meant to leave alone. What it should stop is travel, and
             # everything that travels here -- the aircraft, the meteor, the comet -- is
             # SMIL, which the setting does not reach anyway. Disabling these was blanket
             # caution that switched off the whole city for anyone who has it on.
             '@media (prefers-reduced-motion: reduce){.ft{opacity:1;animation:none}}'
             '</style>')

    p.append('<g clip-path="url(#sc%s)">' % t)
    p.append('<rect x="0" y="0" width="1000" height="%d" fill="url(#sky%s)"/>' % (H, t))

    if True:
        mx, my, mr = MOON
        placed = 0
        while placed < 34:
            x, y = rnd.randint(14, 986), rnd.randint(6, ROOFLINE - 16)
            if (x - mx) ** 2 + (y - my) ** 2 < 46 * 46:
                continue
            if 250 < x < 750 and TEXT_Y - 22 < y < TEXT_Y + 12:
                continue
            period = round(rnd.uniform(6.0, 26.0), 1)
            # A four-pointed star loses more area to its notches than a disc of the same
            # radius, so it has to be drawn larger to read at all.
            shape = star(x, y, rnd.uniform(2.4, 5.0))
            if rnd.random() < 0.10:
                # A sky where every point moves is a sky nobody believes. Some just sit.
                p.append('<path d="%s" fill="%s" opacity="%.2f"/>'
                         % (shape, k["star"], rnd.uniform(.55, .95)))
            else:
                p.append('<path class="st%d" style="animation-duration:%ss;'
                         'animation-delay:-%.1fs" d="%s" fill="%s"/>'
                         % (rnd.randint(1, 4), period, rnd.uniform(0, period), shape, k["star"]))
            placed += 1

        # A warm disc and its craters. Nothing behind it and nothing cutting it.
        p.append('<circle cx="%d" cy="%d" r="%d" fill="%s"/>' % (mx, my, mr, k["moon"]))
        for dx, dy, r in ((5, 4, 3.0), (-6, -3, 2.1), (2, -8, 1.5),
                          (-2, 7, 1.7), (9, -5, 1.2), (-8, 6, 1.1)):
            p.append('<circle cx="%d" cy="%d" r="%.1f" fill="%s" opacity="0.7"/>'
                     % (mx + dx, my + dy, r, k["crater"]))

        lo, hi = COMET_BAND
        p.append(streak(t, k["head"], "shooting", 52, 1.9, (0, 2, 4),
                        ((52, -20, 236, 40), (16, -14, 190, 34), (96, -24, 254, 26))))
        # Close to the meteor in size on purpose: alternating every twenty-five
        # seconds, two streaks of the same family read as one thing recurring,
        # where a long bright one against a short faint one reads as two.
        p.append(streak(t, k["head"], "comet", 68, 2.2, (1, 3, 5),
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
                for wx in range(x + 10, x + bw - 13, 13):
                    for wy in range(btop + 16, GROUND - 13, 16):
                        r = rnd.random()
                        if r > .52:
                            p.append('<rect x="%d" y="%d" width="5" height="7" fill="%s"/>'
                                     % (wx, wy, unlit))
                            continue
                        fill = k["win2"] if r < .11 else k["win"]
                        if r < .32:
                            # Nine to thirty-eight seconds. A window is not a pilot light: at a couple of
                            # seconds it reads as a fault indicator rather than as somebody
                            # in a room. Two of the four patterns change twice per period, so
                            # the fastest state change here is still four seconds apart.
                            period = round(rnd.uniform(9.0, 38.0), 1)
                            names, durs, delays = [rnd.choice(BLINKS)], ['%ss' % period], []
                            delays.append('-%.1fs' % rnd.uniform(0, period))
                            if r < .17:
                                # A light that changes colour as well as state: someone
                                # moving from a lamp to a screen. On its own period, so
                                # the two changes never arrive together.
                                names.append('cc' if r < .11 else 'cw')
                                durs.append('%.1fs' % (period * 2.7))
                                delays.append('0s')
                            p.append('<rect style="animation-name:%s;animation-duration:%s;'
                                     'animation-delay:%s;animation-timing-function:ease-in-out;'
                                     'animation-iteration-count:infinite" x="%d" y="%d" '
                                     'width="5" height="7" fill="%s"/>'
                                     % (','.join(names), ','.join(durs), ','.join(delays),
                                        wx, wy, fill))
                        else:
                            p.append('<rect x="%d" y="%d" width="5" height="7" fill="%s" '
                                     'opacity="%s"/>' % (wx, wy, fill, k["winop"]))
            x += bw + rnd.randint(3, 14)
            count -= 1

    p.append(plane(t, k, "out", 0.0, False))
    p.append(plane(t, k, "back", 60.0, True))

    # The line drifts through the same three colours as the strip that closes the panel,
    # so it belongs to the page rather than being tinted for the sake of it. Ink to gold and
    # back, never through a tone that loses contrast against its own sky.
    palette = (c["ink"], c["g1"], c["g2"], c["g0"], c["ink"])
    # Bold sans rather than the serif. A serif at 24px against a gradient loses its thin
    # strokes to antialiasing; a hinted sans at 700 holds every stem.
    p.append('<text class="ft" x="500" y="%d" font-family="%s" font-size="25" '
             'font-weight="700" letter-spacing="0.3" '
             'fill="%s" text-anchor="middle">To an artificial mind, all reality is virtual'
             '<animate attributeName="fill" values="%s" calcMode="spline" keySplines="%s" '
             'dur="26s" repeatCount="indefinite"/></text>'
             % (TEXT_Y, SANS, c["ink"], ";".join(palette),
                ";".join("0.42 0 0.58 1" for _ in palette[:-1])))
    p.append('<rect x="0" y="%d" width="1000" height="5" fill="url(#st%s)"/>' % (H - 5, t))
    p.append('</g></svg>')
    return NL.join(p) + NL


for t in ("light", "dark"):
    io.open(os.path.join(OUT, "skyline-%s.svg" % t), "w", encoding="utf-8",
            newline="\n").write(skyline(t))
    print("wrote skyline-%s.svg" % t)

print("text ~26..52 | comet %d..%d | plane %d..%d (wings +-13) | roofline %d"
      % (COMET_BAND[0], COMET_BAND[1], PLANE_TO, PLANE_FROM, ROOFLINE))
