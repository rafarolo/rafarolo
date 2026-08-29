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

BIG = [("17", "YEARS ON THE JVM"), ("798", "PULL REQUESTS"), ("906", "CODE REVIEWS")]
YEARS = [("'23", 158, 201), ("'24", 173, 221), ("'25", 217, 278), ("'26", 251, 206)]
SCALE = 58.0 / 278.0
BASE = 196


def banner(t):
    c = THEMES[t]
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 250" width="1000" height="250" '
         'role="img" aria-label="Rafael M. Rolo, Specialist and Tech Lead in Capital Markets. '
         '17 years on the JVM, 798 pull requests authored, 906 code reviews for others. Reviews '
         'given exceed pull requests authored in every completed year.">']
    p.append('<defs>')
    p.append('<linearGradient id="s%s" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>' % (t, c["g0"], c["g1"], c["g2"]))
    p.append('<clipPath id="r%s"><rect x="0" y="0" width="1000" height="250" rx="10"/></clipPath>' % t)
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
    p.append('<rect x="0" y="0" width="1000" height="250" fill="%s"/>' % c["bg"])
    p.append('<rect x="0" y="0" width="4" height="250" fill="url(#s%s)"/>' % t)
    p.append('<g font-family="%s">' % SANS)
    p.append('<text class="fade" x="48" y="58" font-size="36" font-weight="700" fill="%s" '
             'letter-spacing="-0.4">Rafael M. Rôlo</text>' % c["ink"])
    p.append('<text class="fade" style="animation-delay:.1s" x="48" y="86" font-size="12" '
             'font-weight="600" fill="%s" letter-spacing="2.4">SPECIALIST &amp; TECH LEAD · '
             'CAPITAL MARKETS</text>' % c["role"])
    p.append('<line class="fade" style="animation-delay:.18s" x1="48" y1="110" x2="952" y2="110" '
             'stroke="%s" stroke-width="1"/>' % c["line"])
    for i, (val, lab) in enumerate(BIG):
        x, d = 48 + i * 195, 0.26 + i * 0.09
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="166" font-size="42" '
                 'font-weight="700" fill="%s" letter-spacing="-1">%s</text>' % (d, x, c["ink"], val))
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="188" font-size="10.5" '
                 'font-weight="600" fill="%s" letter-spacing="1.5">%s</text>' % (d + .06, x + 1, c["mut"], lab))
    p.append('<text class="fade" style="animation-delay:.55s" x="700" y="128" font-size="10" '
             'font-weight="600" fill="%s" letter-spacing="1.5">PULL REQUESTS PER YEAR</text>' % c["mut"])
    for i, (yr, a, r) in enumerate(YEARS):
        gx, ha, hr = 700 + i * 63, a * SCALE, r * SCALE
        d, last = 0.62 + i * 0.11, i == len(YEARS) - 1
        p.append('<rect class="bar" style="animation-delay:%.2fs" x="%d" y="%.1f" width="24" '
                 'height="%.1f" rx="1.5" fill="%s" opacity="0.38"/>' % (d, gx, BASE - ha, ha, c["acc"]))
        p.append('<rect class="%s" style="animation-delay:%.2fs" x="%d" y="%.1f" width="24" '
                 'height="%.1f" rx="1.5" fill="%s"/>'
                 % ("live" if last else "bar", d + .05, gx + 27, BASE - hr, hr, c["acc"]))
        p.append('<text class="fade" style="animation-delay:%.2fs" x="%d" y="210" font-size="9" '
                 'font-weight="600" fill="%s" text-anchor="middle">%s</text>' % (d + .1, gx + 25, c["dim"], yr))
    p.append('<g class="fade" style="animation-delay:1.15s">')
    p.append('<circle cx="704" cy="226" r="4" fill="%s" opacity="0.38"/>' % c["acc"])
    p.append('<text x="713" y="229" font-size="8.5" font-weight="600" fill="%s" '
             'letter-spacing="1">AUTHORED</text>' % c["dim"])
    p.append('<circle cx="794" cy="226" r="4" fill="%s"/>' % c["acc"])
    p.append('<text x="803" y="229" font-size="8.5" font-weight="600" fill="%s" '
             'letter-spacing="1">REVIEWED FOR OTHERS</text>' % c["dim"])
    p.append('</g>')
    p.append('<text class="fade" style="animation-delay:1.15s" x="48" y="229" font-size="8.5" '
             'font-weight="600" fill="%s" letter-spacing="1.1">PRIVATE CORPORATE REPOSITORIES · '
             'MEASURED AUGUST 2026 · 2026 PARTIAL</text>' % c["dim"])
    p.append('</g>')
    p.append('<rect x="0" y="245" width="1000" height="5" fill="url(#s%s)"/>' % t)
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
        p.append('<text x="%d" y="%d" font-size="28" font-weight="700" fill="%s" '
                 'text-anchor="middle" letter-spacing="-1">%s</text>' % (cx, cy + 10, c["ink"], big))
        p.append('<text class="lb" style="animation-delay:%.2fs" x="%d" y="170" font-size="10.5" '
                 'font-weight="700" fill="%s" text-anchor="middle" letter-spacing="1.5">%s</text>'
                 % (.7 + i * .12, cx, c["mut"], lab))
        p.append('<text class="lb" style="animation-delay:%.2fs" x="%d" y="188" font-size="10.5" '
                 'fill="%s" text-anchor="middle">%s</text>' % (.78 + i * .12, cx, c["dim"], sub))
    p.append('</g></g></svg>')
    return "\n".join(p) + "\n"


GROUPS = [
    ("domain/", "the part that does not get replaced", [
        ("securitization", "CRI · CRA · series · lastro"),
        ("settlement", "B3 · custody · liquidation dates"),
        ("accounting", "asset × liability · roll-forward")]),
    ("application/", "what the days are actually spent on", [
        ("review", "906 usages, 17 callers"),
        ("architecture", "hexagonal · one contract per capability"),
        ("reliability", "0 bugs · 0 vulnerabilities · rating A")]),
    ("adapters/", "swappable on purpose — that is the point", [
        ("jvm", "kotlin · java · spring boot"),
        ("storage", "postgres · sql server · cosmos"),
        ("cloud", "azure · aks · pulumi · actions"),
        ("signals", "prometheus · grafana · sonarqube")]),
]
CMD = "$ tree rolo.m.rafael"
CH = 7.82
TYPE_S = 1.0


def archetype(t):
    c = THEMES[t]
    n_rows = sum(1 + len(v) for _, _, v in GROUPS)
    h = 44 + 30 + n_rows * 21 + (len(GROUPS) - 1) * 8 + 26
    w = CH * len(CMD)
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" width="1000" height="%d" '
         'role="img" aria-label="A terminal typing the command tree rolo.m.rafael, whose output '
         'is a package tree: a domain package that does not get replaced, an application package, '
         'and adapter packages that are swappable on purpose.">' % (h, h)]
    p.append('<defs>')
    p.append('<clipPath id="ra%s"><rect x="0" y="0" width="1000" height="%d" rx="10"/></clipPath>' % (t, h))
    p.append('<clipPath id="tp%s"><rect class="type" x="44" y="24" width="%.1f" height="22"/></clipPath>'
             % (t, w))
    p.append('</defs>')
    p.append('<style>'
             '.type{transform-box:fill-box;transform-origin:0 50%%;transform:scaleX(0);'
             'animation:tw %.2fs steps(%d,end) .25s forwards}'
             '.caret{opacity:0;animation:show 0s linear %.2fs forwards,blink 1.06s step-end %.2fs infinite}'
             '.ln{opacity:0;animation:fa .34s ease forwards}'
             '.dot{transform-box:fill-box;transform-origin:50%% 50%%;transform:scale(0);'
             'animation:pop .4s cubic-bezier(.3,1.5,.5,1) forwards}'
             '@keyframes tw{to{transform:scaleX(1)}}@keyframes fa{to{opacity:1}}'
             '@keyframes pop{to{transform:scale(1)}}@keyframes show{to{opacity:1}}'
             '@keyframes blink{50%%{opacity:0}}'
             '@media (prefers-reduced-motion: reduce){'
             '.type{transform:scaleX(1);animation:none}.ln{opacity:1;animation:none}'
             '.dot{transform:scale(1);animation:none}.caret{opacity:1;animation:none}}'
             '</style>' % (TYPE_S, len(CMD), TYPE_S + .25, TYPE_S + .25))
    p.append('<g clip-path="url(#ra%s)">' % t)
    p.append('<rect x="0" y="0" width="1000" height="%d" fill="%s"/>' % (h, c["panel"]))
    p.append('<rect x="0" y="0" width="3" height="%d" fill="%s"/>' % (h, c["acc"]))
    for i, col in enumerate((c["g2"], c["g1"], c["g0"])):
        p.append('<circle cx="%d" cy="22" r="4.5" fill="%s" opacity="0.85"/>' % (26 + i * 15, col))
    p.append('<g font-family="%s" font-size="13">' % MONO)
    p.append('<g clip-path="url(#tp%s)"><text x="44" y="40" fill="%s" font-weight="600">%s</text></g>'
             % (t, c["ink"], CMD))
    p.append('<rect class="caret" x="%.1f" y="28" width="7.5" height="14" fill="%s"/>' % (44 + w + 1, c["acc"]))
    y, n = 74, 0
    for gi, (gname, gnote, leaves) in enumerate(GROUPS):
        last_group = gi == len(GROUPS) - 1
        d = TYPE_S + .35 + n * .05
        p.append('<circle class="dot" style="animation-delay:%.2fs" cx="50" cy="%d" r="4" fill="%s"/>'
                 % (d, y - 4, c["acc"]))
        p.append('<text class="ln" style="animation-delay:%.2fs" x="62" y="%d" font-weight="700" '
                 'fill="%s">%s %s</text>' % (d, y, c["acc"], "└─" if last_group else "├─", gname))
        p.append('<text class="ln" style="animation-delay:%.2fs" x="360" y="%d" font-size="11.5" '
                 'font-style="italic" fill="%s">%s</text>' % (d + .04, y, c["dim"], gnote))
        y += 21
        n += 1
        for li, (lname, lnote) in enumerate(leaves):
            d = TYPE_S + .35 + n * .05
            trunk = "&#160;" if last_group else "│"
            glyph = "└─" if li == len(leaves) - 1 else "├─"
            p.append('<text class="ln" style="animation-delay:%.2fs" x="84" y="%d" fill="%s">'
                     '%s&#160;&#160;%s %s</text>' % (d, y, c["mut"], trunk, glyph, lname))
            p.append('<text class="ln" style="animation-delay:%.2fs" x="360" y="%d" font-size="11.5" '
                     'fill="%s">%s</text>' % (d + .04, y, c["dim"], lnote))
            y += 21
            n += 1
        y += 8
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
                for wx in range(x + 7, x + bw - 6, 11):
                    for wy in range(top + 11, GROUND - 8, 13):
                        r = rnd.random()
                        if r > .52:
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
    p.append('<text class="ft" x="500" y="56" font-family="%s" font-size="22" font-style="italic" fill="%s" text-anchor="middle">To an artificial mind, all reality is virtual.</text>' % (SERIF, c["ink"]))
    p.append('<text class="ft" style="animation-delay:.35s" x="500" y="84" font-family="%s" font-size="10" font-weight="700" letter-spacing="4" fill="%s" text-anchor="middle" opacity="0.8">SÃO PAULO · BRAZIL</text>' % (SANS, c["dim"]))
    p.append('<rect x="0" y="255" width="1000" height="5" fill="url(#st%s)"/>' % t)
    p.append('</g></svg>')
    return "\n".join(p) + "\n"


for t in ("light", "dark"):
    for name, fn in (("banner", banner), ("rings", rings), ("archetype", archetype), ("skyline", skyline)):
        io.open(os.path.join(OUT, "%s-%s.svg" % (name, t)), "w", encoding="utf-8",
                newline="\n").write(fn(t))
    print("wrote banner/rings/archetype/skyline for", t)


# ---------------------------------------------------------------- linkedin badge

def badge():
    lab, msg = "LINKEDIN", "RAFAROLO"
    fs, ls = 11.0, 1.15
    cw = fs * .70 + ls
    x_lab = 9 + 16 + 8
    x_div = x_lab + len(lab) * cw + 10
    x_msg = x_div + 11
    w, h = x_msg + len(msg) * cw + 12, 28
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %d" width="%.0f" height="%d" '
         'role="img" aria-label="LinkedIn: rafarolo">' % (w, h, w, h)]
    p.append('<rect x="0" y="0" width="%.0f" height="%d" fill="#0A66C2"/>' % (w, h))
    p.append('<g transform="translate(9 6)" fill="#FFFFFF">')
    p.append('<rect x="0" y="5" width="3.4" height="11" rx="0.4"/>')
    p.append('<circle cx="1.7" cy="1.9" r="2.05"/>')
    p.append('<path d="M6 16V5h3.3v1.5C9.9 5.4 11.1 4.7 12.5 4.7c2.4 0 3.9 1.6 3.9 4.3V16h-3.5V9.7'
             'c0-1.4-.6-2.2-1.8-2.2-1.1 0-1.8.8-1.8 2.2V16H6z"/>')
    p.append('</g>')
    p.append('<rect x="%.1f" y="8" width="1" height="12" fill="#FFFFFF" opacity="0.38"/>' % x_div)
    p.append('<g font-family="%s" font-size="%.1f" font-weight="700" letter-spacing="%.2f" '
             'fill="#FFFFFF">' % (SANS, fs, ls))
    p.append('<text x="%.1f" y="18.5">%s</text>' % (x_lab, lab))
    p.append('<text x="%.1f" y="18.5" opacity="0.92">%s</text>' % (x_msg, msg))
    p.append('</g></svg>')
    return NL.join(p) + NL


io.open(os.path.join(OUT, "linkedin.svg"), "w", encoding="utf-8", newline="\n").write(badge())
print("wrote linkedin.svg")
