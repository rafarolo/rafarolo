import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_assets import glass_bg, glass_defs, glass_style, THEMES, SANS, OUT, NL

# year, headline, detail, major
ITEMS = [
    ("2025–2026", "OpenSec, an API for partners",
     "22 endpoints across 8 service families · documentation kits built by an automated pipeline", True),
    ("2023–2026", "New cluster, new region, one pipeline",
     "every application rewritten into a single GitHub Actions pipeline · Azure subscription and AKS migration", True),
    ("2023–2026", "Passwordless, and routes that stay inside",
     "Entra ID workload identities on SQL Server and Postgres · service-to-service traffic on cluster-internal DNS", False),
    ("2023–2026", "Kotlin as the platform language",
     "off Python, JavaScript and TypeScript · hexagonal architecture · R$130B+ in issued assets", True),
    ("2021–2023", "Open Banking, certified",
     "every BACEN and FEBRABAN phase through Raidiam conformance · insurance home in a 22M-customer bank app", False),
    ("2020–2021", "Claims analytics on GCP",
     "predictive engine for suspicious claims at a 7M-client insurer, beside a COBOL/CICS core", False),
    ("2019–2020", "WebSphere to Kubernetes",
     "retail insurance systems onto Liberty on IBM Cloud Private, OpenShift pipeline", False),
    ("2014–2015", "A study area, ten times faster",
     "found the data bottleneck in a geomarketing platform's core calculation", False),
]

ROW = 74
TOP = 46
SPINE = 128


def timeline(t):
    c = THEMES[t]
    h = TOP + len(ITEMS) * ROW + 18
    y_last = TOP + (len(ITEMS) - 1) * ROW

    alt = "; ".join("%s %s: %s" % (i[0], i[1], i[2]) for i in ITEMS)
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" width="1000" height="%d" '
         'role="img" aria-label="Timeline of selected work. %s">' % (h, h, alt)]
    p.append('<defs>' + glass_defs(t, "tl") + '<clipPath id="tl%s"><rect x="0" y="0" width="1000" height="%d" rx="10"/>'
             '</clipPath></defs>' % (t, h))
    p.append('<style>'
             '.sp{transform-box:fill-box;transform-origin:50% 0;transform:scaleY(0);'
             'animation:dn 1.1s cubic-bezier(.3,.8,.3,1) .1s forwards}'
             '.nd{transform-box:fill-box;transform-origin:50% 50%;transform:scale(0);'
             'animation:pp .45s cubic-bezier(.3,1.6,.5,1) forwards}'
             '.tx{opacity:0;animation:fi .45s ease forwards}'
             '@keyframes dn{to{transform:scaleY(1)}}@keyframes pp{to{transform:scale(1)}}'
             '@keyframes fi{to{opacity:1}}'
             '@media (prefers-reduced-motion: reduce){.sp{transform:scaleY(1);animation:none}'
             '.nd{transform:scale(1);animation:none}.tx{opacity:1;animation:none}}'
             + glass_style(15) + '</style>')
    p.append('<g clip-path="url(#tl%s)">' % t)
    p.append(glass_bg(t, "tl", 1000, h))
    p.append('<rect class="sp" x="%d" y="%d" width="2" height="%d" fill="%s" opacity="0.45"/>'
             % (SPINE - 1, TOP - 22, y_last - TOP + 44, c["acc"]))
    p.append('<g font-family="%s">' % SANS)

    for i, (yr, head, det, major) in enumerate(ITEMS):
        y = TOP + i * ROW
        d = .3 + i * .13
        r = 9 if major else 5.5
        p.append('<circle class="nd" style="animation-delay:%.2fs" cx="%d" cy="%d" r="%.1f" '
                 'fill="%s" stroke="%s" stroke-width="%d"/>'
                 % (d, SPINE, y, r, c["acc"] if major else c["panel"], c["acc"], 3 if major else 2.5))
        p.append('<text class="tx" style="animation-delay:%.2fs" x="%d" y="%d" font-size="14" '
                 'font-weight="700" fill="%s" text-anchor="end" letter-spacing="0.3">%s</text>'
                 % (d + .05, SPINE - 24, y + 5, c["acc"], yr))
        p.append('<text class="tx" style="animation-delay:%.2fs" x="%d" y="%d" font-size="%d" '
                 'font-weight="700" fill="%s" letter-spacing="-0.2">%s</text>'
                 % (d + .08, SPINE + 26, y + 1, 19 if major else 17, c["ink"], head))
        p.append('<text class="tx" style="animation-delay:%.2fs" x="%d" y="%d" font-size="14" '
                 'fill="%s">%s</text>' % (d + .12, SPINE + 26, y + 24, c["dim"], det))

    p.append('</g></g></svg>')
    return NL.join(p) + NL


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


for t in ("light", "dark"):
    io.open(os.path.join(OUT, "timeline-%s.svg" % t), "w", encoding="utf-8",
            newline="\n").write(timeline(t))
    print("wrote timeline-%s.svg" % t)

# U+2011 non-breaking hyphen: an en dash is a line-break opportunity and splits the cell
rows = NL.join("| `%s` | **%s** | %s |"
               % (i[0].replace(u"–", u"‑"), i[1], i[2]) for i in ITEMS)
io.open(os.path.join(os.path.dirname(OUT), "_timeline_table.md"), "w",
        encoding="utf-8", newline="\n").write(rows + NL)
print("wrote table fallback")
