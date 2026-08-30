import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_assets import THEMES, SANS, OUT, NL

BLACK = "#0D1319"
FS, LS = 11.0, 1.15
CW = FS * .70 + LS

LOGO = {
    "linkedin": ('<rect x="0" y="5" width="3.4" height="11" rx="0.4"/>'
                 '<circle cx="1.7" cy="1.9" r="2.05"/>'
                 '<path d="M6 16V5h3.3v1.5C9.9 5.4 11.1 4.7 12.5 4.7c2.4 0 3.9 1.6 3.9 4.3V16h-3.5V9.7'
                 'c0-1.4-.6-2.2-1.8-2.2-1.1 0-1.8.8-1.8 2.2V16H6z"/>'),
    "stack": ('<path d="M13.2 15.4v-4h1.6V17H2.6v-5.6h1.6v4z"/>'
              '<path d="M5.6 11.1l7.8 1.6.3-1.6-7.8-1.6zM6.6 7.4l7.2 3.4.7-1.5-7.2-3.4zM8.6 3.9'
              'l6.1 5.1 1-1.2-6.1-5.1zM12.6.4l-1.3 1 4.7 6.4 1.3-1zM5.4 15.4h8v-1.6h-8z"/>'),
    "pin": ('<path d="M8 0C4.9 0 2.4 2.5 2.4 5.6 2.4 9.8 8 16.4 8 16.4s5.6-6.6 5.6-10.8'
            'C13.6 2.5 11.1 0 8 0zm0 7.7a2.1 2.1 0 1 1 0-4.2 2.1 2.1 0 0 1 0 4.2z"/>'),
}


def badge(logo, label, brand, msg=None, aria=None):
    x_lab = 9 + 16 + 8
    lw = x_lab + len(label) * CW + 11
    w = lw if msg is None else lw + 11 + len(msg) * CW + 12
    h = 28
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %d" width="%.0f" height="%d" '
         'role="img" aria-label="%s">' % (w, h, w, h, aria or label.title())]
    p.append('<rect x="0" y="0" width="%.1f" height="%d" fill="%s"/>' % (lw, h, brand))
    if msg is not None:
        p.append('<rect x="%.1f" y="0" width="%.1f" height="%d" fill="%s"/>' % (lw, w - lw, h, BLACK))
    p.append('<g transform="translate(9 6)" fill="#FFFFFF">%s</g>' % logo)
    p.append('<g font-family="%s" font-size="%.1f" font-weight="700" letter-spacing="%.2f" '
             'fill="#FFFFFF">' % (SANS, FS, LS))
    p.append('<text x="%.1f" y="18.5">%s</text>' % (x_lab, label))
    if msg is not None:
        p.append('<text x="%.1f" y="18.5">%s</text>' % (lw + 11, msg))
    p.append('</g></svg>')
    return NL.join(p) + NL


CYCLE = 4.6
STEP = 0.10


def divider(t):
    """A pulse crossing the dots left to right, then a long wait.

    The graduated sizes are what give the divider its shape, so they stay; only the light
    moves. A wave every four and a half seconds reads as a separator that is alive rather
    than as something asking to be looked at."""
    c = THEMES[t]
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 22" width="1000" height="22" '
         'role="presentation" aria-hidden="true">']
    for i, op in enumerate((".3", ".62", "1", ".62", ".3")):
        r = 2.0 if i in (0, 4) else (2.6 if i in (1, 3) else 3.4)
        lit = min(1.0, float(op) + 0.55)
        # Scaling about the centre is the same drawing as a larger radius, and it does not
        # force the geometry to be recomputed on every frame the way animating r does.
        peak = (r + 1.1) / r
        p.append('<g transform="translate(%d 11)">'
                 '<circle cx="0" cy="0" r="%.1f" fill="%s" opacity="%s">'
                 '<animate attributeName="opacity" values="%s;%.2f;%s;%s" '
                 'keyTimes="0;0.05;0.13;1" begin="%.2fs" dur="%.1fs" '
                 'repeatCount="indefinite"/></circle>'
                 '<animateTransform attributeName="transform" type="scale" '
                 'values="1;%.3f;1;1" keyTimes="0;0.05;0.13;1" begin="%.2fs" dur="%.1fs" '
                 'repeatCount="indefinite" additive="sum"/>'
                 '</g>'
                 % (476 + i * 12, r, c["acc"], op,
                    op, lit, op, op, i * STEP, CYCLE,
                    peak, i * STEP, CYCLE))
    p.append('</svg>')
    return NL.join(p) + NL


OUTS = {
    "linkedin.svg": badge(LOGO["linkedin"], "LINKEDIN", "#0A66C2", "RAFAROLO", "LinkedIn: rafarolo"),
    "stackexchange.svg": badge(LOGO["stack"], "STACK EXCHANGE", "#F48024", None, "Stack Exchange profile"),
    "location.svg": badge(LOGO["pin"], "SÃO PAULO", "#0E5468", "BRASIL", "São Paulo, Brasil"),
}
for name, svg in OUTS.items():
    io.open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n").write(svg)
for t in ("light", "dark"):
    io.open(os.path.join(OUT, "dot-%s.svg" % t), "w", encoding="utf-8", newline="\n").write(divider(t))
print("wrote", ", ".join(sorted(OUTS)) + ", dot-light.svg, dot-dark.svg")
