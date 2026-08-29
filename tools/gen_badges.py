import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_all import THEMES, SANS, OUT, NL

BLACK = "#0D1319"
LOGO = {
    "linkedin": ('<rect x="0" y="5" width="3.4" height="11" rx="0.4"/>'
                 '<circle cx="1.7" cy="1.9" r="2.05"/>'
                 '<path d="M6 16V5h3.3v1.5C9.9 5.4 11.1 4.7 12.5 4.7c2.4 0 3.9 1.6 3.9 4.3V16h-3.5V9.7'
                 'c0-1.4-.6-2.2-1.8-2.2-1.1 0-1.8.8-1.8 2.2V16H6z"/>'),
    "stack": ('<path d="M13.2 15.4v-4h1.6V17H2.6v-5.6h1.6v4z"/>'
              '<path d="M5.6 11.1l7.8 1.6.3-1.6-7.8-1.6zM6.6 7.4l7.2 3.4.7-1.5-7.2-3.4zM8.6 3.9'
              'l6.1 5.1 1-1.2-6.1-5.1zM12.6.4l-1.3 1 4.7 6.4 1.3-1zM5.4 15.4h8v-1.6h-8z"/>'),
}


def badge(name, logo, label, brand, msg=" RAFAROLO"):
    fs, ls = 11.0, 1.15
    cw = fs * .70 + ls
    x_lab = 9 + 16 + 8
    lw = x_lab + len(label) * cw + 11
    x_msg = lw + 11
    w, h = x_msg + len(msg.strip()) * cw + 12, 28
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %d" width="%.0f" height="%d" '
         'role="img" aria-label="%s: rafarolo">' % (w, h, w, h, label.title())]
    p.append('<rect x="0" y="0" width="%.1f" height="%d" fill="%s"/>' % (lw, h, brand))
    p.append('<rect x="%.1f" y="0" width="%.1f" height="%d" fill="%s"/>' % (lw, w - lw, h, BLACK))
    p.append('<g transform="translate(9 6)" fill="#FFFFFF">%s</g>' % logo)
    p.append('<g font-family="%s" font-size="%.1f" font-weight="700" letter-spacing="%.2f" '
             'fill="#FFFFFF">' % (SANS, fs, ls))
    p.append('<text x="%.1f" y="18.5">%s</text>' % (x_lab, label))
    p.append('<text x="%.1f" y="18.5">%s</text>' % (x_msg, msg.strip()))
    p.append('</g></svg>')
    return NL.join(p) + NL


def divider(t):
    c = THEMES[t]
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 22" width="1000" height="22" '
         'role="presentation" aria-hidden="true">']
    for i, op in enumerate((".3", ".62", "1", ".62", ".3")):
        p.append('<circle cx="%d" cy="11" r="%.1f" fill="%s" opacity="%s"/>'
                 % (476 + i * 12, 2.0 if i in (0, 4) else (2.6 if i in (1, 3) else 3.4), c["acc"], op))
    p.append('</svg>')
    return NL.join(p) + NL


io.open(os.path.join(OUT, "linkedin.svg"), "w", encoding="utf-8", newline="\n").write(
    badge("linkedin", LOGO["linkedin"], "LINKEDIN", "#0A66C2"))
io.open(os.path.join(OUT, "stackexchange.svg"), "w", encoding="utf-8", newline="\n").write(
    badge("stack", LOGO["stack"], "STACK EXCHANGE", "#F48024"))
for t in ("light", "dark"):
    io.open(os.path.join(OUT, "dot-%s.svg" % t), "w", encoding="utf-8", newline="\n").write(divider(t))
print("wrote linkedin.svg, stackexchange.svg, dot-light.svg, dot-dark.svg")
