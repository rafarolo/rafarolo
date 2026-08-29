import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_all import glass_bg, glass_defs, glass_style, THEMES, SANS, OUT, NL

ROWS = [
    (17, ["Java"]),
    (14, ["PostgreSQL"]),
    (12, ["MongoDB"]),
    (11, ["Spring Boot", "SQL Server"]),
    (7, ["Spring Security", "OpenAPI", "Kubernetes", "Docker", "SonarQube"]),
    (5, ["AWS", "Prometheus", "Grafana"]),
    (3, ["Kotlin", "Azure", "Pulumi", "GitHub Actions", "Cosmos DB", "GraphQL", "OpenTelemetry"]),
    (2, ["Airflow", "Spring AI"]),
    (1, ["GCP"]),
]

PROTOCOLS = ["OAuth2", "OpenID Connect", "JWT", "Keycloak", "Entra ID", "FAPI", "Workload Identity"]

TOP = 96
STEP = 34
BAR_X = 96
BAR_W = 232
CHIP_X = 356
MAX_YEARS = max(y for y, _ in ROWS)
CH = 6.5
CHIP_PAD = 9
CHIP_GAP = 7
CHIP_H = 21


def chip_width(label):
    return len(label) * CH + CHIP_PAD * 2


def tenure(t):
    c = THEMES[t]
    body = TOP + len(ROWS) * STEP
    h = body + 96

    alt = "Years with each technology, longest first. " + "; ".join(
        "%d years: %s" % (y, ", ".join(n)) for y, n in ROWS
    ) + ". Standards without a tenure: " + ", ".join(PROTOCOLS) + "."

    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" width="1000" height="%d" '
         'role="img" aria-label="%s">' % (h, h, alt)]
    p.append('<defs>' + glass_defs(t, "tn") +
             '<clipPath id="tn%s"><rect x="0" y="0" width="1000" height="%d" rx="10"/></clipPath>'
             '<linearGradient id="bg%s" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
             '</defs>' % (t, h, t, c["acc"], c["g1"]))
    p.append('<style>.t{opacity:0;animation:fi .45s ease forwards}'
             '@keyframes fi{to{opacity:1}}'
             '@media (prefers-reduced-motion: reduce){.t{opacity:1;animation:none}}'
             + glass_style(14) + '</style>')
    p.append('<g clip-path="url(#tn%s)">' % t)
    p.append(glass_bg(t, "tn", 1000, h))
    p.append('<g font-family="%s">' % SANS)

    p.append('<text class="t" x="%d" y="52" font-size="12" font-weight="700" fill="%s" '
             'letter-spacing="1.8">YEARS WITH EACH</text>' % (52, c["mut"]))
    p.append('<text class="t" style="animation-delay:.08s" x="%d" y="52" font-size="12" '
             'fill="%s">counted from the first role in which it appears</text>' % (232, c["dim"]))

    for i, (years, names) in enumerate(ROWS):
        y = TOP + i * STEP
        d = .2 + i * .07
        w = BAR_W * years / float(MAX_YEARS)

        p.append('<text class="t" style="animation-delay:%.2fs" x="%d" y="%d" font-size="15" '
                 'font-weight="700" fill="%s" text-anchor="end">%dy</text>'
                 % (d, BAR_X - 14, y + 5, c["ink"], years))
        p.append('<rect x="%d" y="%.1f" width="%d" height="10" rx="5" fill="%s" opacity="0.30"/>'
                 % (BAR_X, y - 5, BAR_W, c["line"]))
        p.append('<rect x="%d" y="%.1f" width="0" height="10" rx="5" fill="url(#bg%s)">'
                 '<animate attributeName="width" from="0" to="%.1f" begin="%.2fs" dur="0.9s" '
                 'calcMode="spline" keySplines="0.25 0.9 0.3 1" fill="freeze"/></rect>'
                 % (BAR_X, y - 5, t, w, d))

        x = CHIP_X
        for name in names:
            cw = chip_width(name)
            p.append('<g class="t" style="animation-delay:%.2fs">' % (d + .25))
            p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="5" fill="%s" '
                     'opacity="0.55"/>' % (x, y - CHIP_H / 2.0 - 1, cw, CHIP_H, c["bg"]))
            p.append('<text x="%.1f" y="%d" font-size="12" fill="%s">%s</text>'
                     % (x + CHIP_PAD, y + 4, c["ink"], name))
            p.append('</g>')
            x += cw + CHIP_GAP

    y = body + 26
    p.append('<line class="t" style="animation-delay:.9s" x1="52" y1="%d" x2="948" y2="%d" '
             'stroke="%s" stroke-width="1"/>' % (y - 18, y - 18, c["line"]))
    p.append('<text class="t" style="animation-delay:.95s" x="52" y="%d" font-size="12" '
             'fill="%s">Standards and protocols, which have no tenure worth quoting</text>'
             % (y + 4, c["dim"]))

    x = 52
    y += 30
    for name in PROTOCOLS:
        cw = chip_width(name)
        p.append('<g class="t" style="animation-delay:1.0s">')
        p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="5" fill="none" '
                 'stroke="%s" stroke-width="1" opacity="0.7"/>'
                 % (x, y - CHIP_H / 2.0 - 1, cw, CHIP_H, c["line"]))
        p.append('<text x="%.1f" y="%d" font-size="12" fill="%s">%s</text>'
                 % (x + CHIP_PAD, y + 4, c["mut"], name))
        p.append('</g>')
        x += cw + CHIP_GAP

    p.append('</g></g></svg>')
    return NL.join(p) + NL


for t in ("light", "dark"):
    io.open(os.path.join(OUT, "tenure-%s.svg" % t), "w", encoding="utf-8",
            newline="\n").write(tenure(t))
    print("wrote tenure-%s.svg" % t)

widest = max(CHIP_X + sum(chip_width(n) + CHIP_GAP for n in names) for _, names in ROWS)
print("chip column ends at %.0f (canvas 1000)" % widest)
print("protocol row ends at %.0f" % (52 + sum(chip_width(n) + CHIP_GAP for n in PROTOCOLS)))
