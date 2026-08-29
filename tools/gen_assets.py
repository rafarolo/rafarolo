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


def banner(t):
    c = THEMES[t]
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 196" width="1000" height="196" '
         'role="img" aria-label="Rafael Rolo, Specialist and Tech Lead in Capital Markets. '
         '17 years on the JVM, 798 pull requests authored, 906 code reviews for others, eight '
         'sectors served. Reviews '
         '">']
    p.append('<defs>')
    p.append('<linearGradient id="s%s" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>' % (t, c["g0"], c["g1"], c["g2"]))
    p.append('<clipPath id="r%s"><rect x="0" y="0" width="1000" height="196" rx="10"/></clipPath>' % t)
    p.append('</defs>')
    p.append('<style>'
             '.fade{opacity:0;animation:f .55s ease forwards}'
             '.bar{transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);'
             'animation:g .75s cubic-bezier(.2,.85,.25,1) forwards}'
             '.live{animation:g .75s cubic-bezier(.2,.85,.25,1) forwards,pulse 3.4s ease-in-out 1.6s infinite}'
             '@keyframes f{to{opacity:1}}@keyframes g{to{transform:scaleY(1)}}'
             '@keyframes pulse{0%,100%{opacity:1}50%{opacity:.62}}'
             '@media (prefers-reduced-motion: reduce){'
             '.fade{opacity:1;animation:none}.bar,.live{transform:scaleY(1);animation:none}}'
             '</style>')
    p.append('<g clip-path="url(#r%s)">' % t)
    p.append('<rect x="0" y="0" width="1000" height="196" fill="%s"/>' % c["bg"])
    p.append('<rect x="0" y="0" width="4" height="196" fill="url(#s%s)"/>' % t)
    p.append('<g font-family="%s">' % SANS)
    p.append('<text class="fade" x="48" y="58" font-size="36" font-weight="700" fill="%s" '
             'letter-spacing="-0.4">Rafael Rôlo</text>' % c["ink"])
    p.append('<text class="fade" style="animation-delay:.1s" x="48" y="86" font-size="12" '
             'font-weight="600" fill="%s" letter-spacing="2.4">SPECIALIST &amp; TECH LEAD · '
             'CAPITAL MARKETS</text>' % c["role"])
    p.append('<line class="fade" style="animation-delay:.18s" x1="48" y1="110" x2="952" y2="110" '
             'stroke="%s" stroke-width="1"/>' % c["line"])
    for i, (val, lab) in enumerate(BIG):
        x, d = 60 + i * 228, 0.26 + i * 0.08
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="166" font-size="42" '
                 'font-weight="700" fill="%s" letter-spacing="-1">%s</text>' % (d, x, c["ink"], val))
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="189" font-size="12" '
                 'font-weight="600" fill="%s" letter-spacing="1.5">%s</text>' % (d + .06, x + 1, c["mut"], lab))
    p.append('<text class="fade" style="animation-delay:1.15s" x="60" y="175" font-size="8.5" '
             'font-weight="600" fill="%s" letter-spacing="1.1">PRIVATE CORPORATE REPOSITORIES · '
             'MEASURED AUGUST 2026</text>' % c["dim"])
    p.append('</g>')
    p.append('<rect x="0" y="191" width="1000" height="5" fill="url(#s%s)"/>' % t)
    p.append('</g></svg>')
    return "\n".join(p) + "\n"


RINGS = [(0.88, "88%", "TEST COVERAGE", "core service, up from 74.7%"),
         (0.53, "53%", "OF EVERY PR I TOUCHED", "906 reviews against 798 of my own"),
         (0.89, "89%", "PULL REQUESTS MERGED", "707 merged of 798 opened")]
RR = 46.0
RC = 2 * math.pi * RR


def rings(t):
    c = THEMES[t]
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 212" width="1000" height="212" '
         'role="img" aria-label="Three proportions. Test coverage 88 percent, up from 74.7. '
         '53 percent of every pull request touched belonged to someone else: 906 reviews against '
         '798 of my own. 89 percent of pull requests opened were merged: 707 of 798.">']
    p.append('<defs><clipPath id="rg%s"><rect x="0" y="0" width="1000" height="212" rx="10"/>'
             '</clipPath></defs>' % t)
    css = ['<style>.lb{opacity:0;animation:fa .5s ease forwards}@keyframes fa{to{opacity:1}}']
    for i, (frac, _, _, _) in enumerate(RINGS):
        css.append('.a%d{stroke-dasharray:%.1f;stroke-dashoffset:%.1f;'
                   'animation:k%d 1.15s cubic-bezier(.25,.9,.3,1) %.2fs forwards}'
                   % (i, RC, RC, i, .25 + i * .16))
        css.append('@keyframes k%d{to{stroke-dashoffset:%.1f}}' % (i, RC * (1 - frac)))
    css.append('@media (prefers-reduced-motion: reduce){.lb{opacity:1;animation:none}')
    for i, (frac, _, _, _) in enumerate(RINGS):
        css.append('.a%d{stroke-dashoffset:%.1f;animation:none}' % (i, RC * (1 - frac)))
    css.append('}</style>')
    p.append("".join(css))
    p.append('<g clip-path="url(#rg%s)">' % t)
    p.append('<rect x="0" y="0" width="1000" height="212" fill="%s"/>' % c["panel"])
    p.append('<g font-family="%s">' % SANS)
    for i, (frac, big, lab, sub) in enumerate(RINGS):
        cx, cy = 190 + i * 310, 86
        p.append('<circle cx="%d" cy="%d" r="%.1f" fill="none" stroke="%s" stroke-width="11"/>'
                 % (cx, cy, RR, c["track"]))
        p.append('<circle class="a%d" cx="%d" cy="%d" r="%.1f" fill="none" stroke="%s" '
                 'stroke-width="11" stroke-linecap="round" transform="rotate(-90 %d %d)"/>'
                 % (i, cx, cy, RR, c["acc"], cx, cy))
        p.append('<text x="%d" y="%d" font-size="30" font-weight="700" fill="%s" '
                 'text-anchor="middle" letter-spacing="-1">%s</text>' % (cx, cy + 10, c["ink"], big))
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
