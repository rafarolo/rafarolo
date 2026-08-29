import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_all import carbon, THEMES, MONO, OUT, NL

ROOT = "rolo.rafael.life"
CMD = "$ tree " + ROOT
CH = 8.42
TYPE_S = 1.05


def d(name, note, kids):
    return dict(name=name, note=note, kids=kids)


def f(name, note):
    return dict(name=name, note=note, kids=None)


TREE = [
    d("professional/", "", [
        d("domain/", "the part that does not get replaced", [
            f("securitization", "CRI · CRA · series · lastro"),
            f("settlement", "B3 · custody · liquidation dates"),
            f("accounting", "asset × liability · roll-forward")]),
        d("practice/", "what the days are actually spent on", [
            f("review", "906 usages, 17 callers"),
            f("architecture", "hexagonal · one contract per capability"),
            f("reliability", "0 bugs · 0 vulnerabilities · rating A"),
            f("advocacy", "AI and backend culture for the engineering team")]),
        d("adapters/", "swappable on purpose — that is the point", [
            f("jvm", "kotlin · java · spring boot"),
            f("storage", "postgres · sql server · cosmos"),
            f("cloud", "azure · aks · pulumi · actions"),
            f("signals", "prometheus · grafana · sonarqube")])]),
    d("person/", "", [
        f("industries", "capital markets · banking · insurance · government · e-commerce"),
        f("languages", "português · english · español"),
        f("education", "UNICAMP · three graduate degrees"),
        f("published", "three papers · one biometric lab system")]),
]

NBSP = "&#160;"


def flatten(nodes, prefix="", out=None, depth=1):
    if out is None:
        out = []
    for i, n in enumerate(nodes):
        last = i == len(nodes) - 1
        glyph = "└─" if last else "├─"
        out.append((prefix + glyph + " ", n["name"], n["note"], n["kids"] is not None, depth))
        if n["kids"]:
            flatten(n["kids"], prefix + (NBSP * 3 if last else "│" + NBSP * 2), out, depth + 1)
    return out


def archetype(t):
    c = THEMES[t]
    rows = flatten(TREE)
    h = 44 + 34 + (len(rows) + 1) * 21 + 26
    w = CH * len(CMD)

    alt = ("A terminal typing tree %s. Under professional: domain, which does not get replaced; "
           "practice; and adapters, swappable on purpose. Under person: languages, education, "
           "published work." % ROOT)
    p = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 %d" width="1000" height="%d" '
         'role="img" aria-label="%s">' % (h, h, alt)]
    p.append('<defs>')
    p.append(carbon(t, "ra") + '<clipPath id="ra%s"><rect x="0" y="0" width="1000" height="%d" rx="10"/></clipPath>' % (t, h))
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
    p.append('<rect x="0" y="0" width="1000" height="%d" fill="url(#cfra%s)"/>' % (h, t))
    p.append('<rect x="0" y="0" width="3" height="%d" fill="%s"/>' % (h, c["acc"]))
    for i, col in enumerate((c["g2"], c["g1"], c["g0"])):
        p.append('<circle cx="%d" cy="22" r="4.5" fill="%s" opacity="0.85"/>' % (26 + i * 15, col))

    p.append('<g font-family="%s" font-size="14">' % MONO)
    p.append('<g clip-path="url(#tp%s)"><text x="44" y="40" fill="%s" font-weight="600">%s</text></g>'
             % (t, c["ink"], CMD))
    p.append('<rect class="caret" x="%.1f" y="28" width="7.5" height="14" fill="%s"/>' % (44 + w + 1, c["acc"]))

    y = 78
    base = TYPE_S + .35
    p.append('<text class="ln" style="animation-delay:%.2fs" x="44" y="%d" font-size="14" '
             'font-weight="700" fill="%s">%s</text>' % (base, y, c["ink"], ROOT))
    y += 21

    for i, (prefix, name, note, is_dir, depth) in enumerate(rows):
        dl = base + .07 + i * .045
        fill = c["acc"] if is_dir else c["mut"]
        weight = "700" if is_dir else "400"
        if is_dir and depth == 1:
            p.append('<circle class="dot" style="animation-delay:%.2fs" cx="34" cy="%d" r="4" '
                     'fill="%s"/>' % (dl, y - 4, c["acc"]))
        p.append('<text class="ln" style="animation-delay:%.2fs" x="44" y="%d" fill="%s" '
                 'font-weight="%s">%s%s</text>' % (dl, y, fill, weight, prefix, name))
        if note:
            p.append('<text class="ln" style="animation-delay:%.2fs" x="380" y="%d" font-size="12.5" '
                     '%sfill="%s">%s</text>'
                     % (dl + .04, y, 'font-style="italic" ' if is_dir else "", c["dim"], note))
        y += 21

    p.append('</g></g></svg>')
    return NL.join(p) + NL


for t in ("light", "dark"):
    io.open(os.path.join(OUT, "archetype-%s.svg" % t), "w", encoding="utf-8",
            newline="\n").write(archetype(t))
    print("wrote archetype-%s.svg" % t)
