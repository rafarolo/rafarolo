import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_assets import THEMES, OUT, NL

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

SIZE = 24
SHOWN = 20
PULSE = 6.0
STRIPE = {"light": ("#FFFFFF", "#F6F8FA"), "dark": ("#0D1117", "#151B23")}


def node(t, i, major):
    c = THEMES[t]
    mid = SIZE / 2
    r = 6 if major else 4.5
    pop = .22 + i * .1
    wave = 1.2 + i * .35
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="presentation" aria-hidden="true">' % (SIZE, SIZE, SHOWN, SHOWN)]
    p.append('<style>'
             '.nd,.hl{transform-origin:%gpx %gpx}'
             '.nd{transform:scale(0);animation:pp .38s cubic-bezier(.3,1.6,.5,1) %.2fs forwards}'
             '.hl{opacity:0;animation:hl %.1fs ease-out %.2fs infinite}'
             '@keyframes pp{to{transform:scale(1)}}'
             '@keyframes hl{0%%{opacity:.6;transform:scale(1)}20%%{opacity:0;transform:scale(1.9)}'
             '100%%{opacity:0;transform:scale(1.9)}}'
             '@media (prefers-reduced-motion: reduce){.nd{transform:none;animation:none}'
             '.hl{display:none}}'
             '</style>' % (mid, mid, pop, PULSE, wave))
    p.append('<rect width="%d" height="%d" fill="%s"/>' % (SIZE, SIZE, STRIPE[t][i % 2]))
    p.append('<circle class="hl" cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="1.5"/>'
             % (mid, mid, r, c["acc"]))
    p.append('<circle class="nd" cx="%g" cy="%g" r="%g" fill="%s" stroke="%s" stroke-width="%g"/>'
             % (mid, mid, r, c["acc"] if major else "none", c["acc"], 2.5 if major else 2))
    p.append('</svg>')
    return NL.join(p) + NL


def picture(i):
    return ('<picture><source media="(prefers-color-scheme: dark)" srcset="assets/tl-%d-dark.svg">'
            '<img src="assets/tl-%d-light.svg" width="%d" height="%d" alt=""></picture>'
            % (i, i, SHOWN, SHOWN))


for t in ("light", "dark"):
    for i, item in enumerate(ITEMS):
        io.open(os.path.join(OUT, "tl-%d-%s.svg" % (i, t)), "w", encoding="utf-8",
                newline="\n").write(node(t, i, item[3]))
    print("wrote tl-*-%s.svg" % t)

# U+2011 non-breaking hyphen: an en dash is a line-break opportunity and splits the cell
rows = NL.join("| %s | `%s` | **%s** | %s |"
               % (picture(n), i[0].replace(u"–", u"‑"), i[1], i[2]) for n, i in enumerate(ITEMS))
io.open(os.path.join(os.path.dirname(OUT), "_timeline_table.md"), "w",
        encoding="utf-8", newline="\n").write(rows + NL)
print("wrote table")
