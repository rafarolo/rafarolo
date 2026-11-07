import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_assets import glass_bg, glass_defs, glass_style, THEMES, SANS, OUT, NL
from gen_badges import LOGO

ORANGE = "#FF5E00"
MEDAL = [("6", "#F1B600"), ("43", "#9A9B9E"), ("61", "#AB8A5F")]
BIG = [(60, "6.3M", "REACHED"), (232, "5,486", "REPUTATION"), (404, "174", "ANSWERS"),
       (546, "7,560", "UPVOTES GIVEN")]
MEDALS_X = 734


def panel(t):
    c = THEMES[t]
    w, h = 1000, 150
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="img" aria-label="Stack Overflow, member since December 2015: 6.3 million reached, 5,486 reputation, 174 answers, 7,560 upvotes given, '
         '6 gold, 43 silver and 61 bronze medals.">' % (w, h, w, h)]
    p.append('<defs>' + glass_defs(t, "so") + '<clipPath id="so%s"><rect x="0" y="0" width="%d" '
             'height="%d" rx="10"/></clipPath></defs>' % (t, w, h))
    p.append('<style>.t{opacity:0;animation:fi .4s ease forwards}@keyframes fi{to{opacity:1}}'
             '@media (prefers-reduced-motion: reduce){.t{opacity:1;animation:none}}'
             + glass_style(5) + '</style>')
    p.append('<g clip-path="url(#so%s)">' % t)
    p.append(glass_bg(t, "so", w, h))
    p.append('<rect x="0" y="0" width="%d" height="4" fill="%s"/>' % (w, ORANGE))
    p.append('<g font-family="%s">' % SANS)
    p.append('<g transform="translate(60 22)" fill="%s">%s</g>' % (ORANGE, LOGO["stack"]))
    p.append('<text x="86" y="37" font-size="12" font-weight="700" letter-spacing="1.8" fill="%s">'
             'STACK OVERFLOW · MEMBER SINCE DECEMBER 2015</text>' % c["mut"])
    for i, (x, val, lab) in enumerate(BIG):
        d = .15 + i * .07
        p.append('<text class="t" style="animation-delay:%.2fs" x="%d" y="98" font-size="40" '
                 'font-weight="700" fill="%s" letter-spacing="-1">%s</text>' % (d, x, c["ink"], val))
        p.append('<text class="t" style="animation-delay:%.2fs" x="%d" y="122" font-size="11.5" '
                 'font-weight="600" fill="%s" letter-spacing="1.6">%s</text>' % (d + .05, x + 1, c["mut"], lab))
    x, d = MEDALS_X, .43
    p.append('<g class="t" style="animation-delay:%.2fs">' % d)
    cx = x + 8
    for n, col in MEDAL:
        p.append('<circle cx="%d" cy="84" r="7" fill="%s"/>' % (cx, col))
        p.append('<text x="%d" y="98" font-size="40" font-weight="700" fill="%s" letter-spacing="-1">%s</text>'
                 % (cx + 13, c["ink"], n))
        cx += 13 + len(n) * 23 + 18
    p.append('</g>')
    p.append('<text class="t" style="animation-delay:.48s" x="%d" y="122" font-size="11.5" font-weight="600" '
             'fill="%s" letter-spacing="1.6">MEDALS</text>' % (x + 1, c["mut"]))
    p.append('</g></g></svg>')
    return NL.join(p) + NL


def wr(name, svg):
    io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n").write(svg)


for t in ("light", "dark"):
    wr("so-panel-%s.svg" % t, panel(t))
print("wrote so-panel-light.svg, so-panel-dark.svg")
