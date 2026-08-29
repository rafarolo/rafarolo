"""Stamp every asset URL in the README with a hash of the file it points at.

GitHub proxies README images and caches them by URL. These paths never change, so an
updated drawing can keep serving from the old copy long after it was pushed. A hand-bumped
counter fixes that only for as long as somebody remembers to bump it; a content hash bumps
itself, and only for the assets that actually changed.

Run after regenerating anything under assets/:

    python tools/stamp_assets.py
"""

import hashlib
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
PATTERN = re.compile(r'(assets/([a-z0-9-]+\.svg))(\?v=[0-9a-f]+)?')


def digest(name):
    path = os.path.join(ROOT, "assets", name)
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()[:8]


def main():
    text = io.open(README, encoding="utf-8").read()
    seen, missing = {}, []

    def stamp(match):
        name = match.group(2)
        if not os.path.exists(os.path.join(ROOT, "assets", name)):
            missing.append(name)
            return match.group(0)
        seen[name] = seen.get(name) or digest(name)
        return "%s?v=%s" % (match.group(1), seen[name])

    stamped = PATTERN.sub(stamp, text)

    if missing:
        print("referenced but not on disk: %s" % ", ".join(sorted(set(missing))))
        return 1

    if stamped != text:
        io.open(README, "w", encoding="utf-8", newline="\n").write(stamped)

    for name in sorted(seen):
        print("%-24s %s" % (name, seen[name]))
    print("%d assets stamped, README %s" % (len(seen), "rewritten" if stamped != text else "unchanged"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
