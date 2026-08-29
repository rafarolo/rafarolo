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
# Bump when a URL has to change even though its file has not -- the proxy caches by URL,
# so a version that was fetched while the wrong drawing was in the repository keeps serving
# that drawing for as long as the URL stays the same.
SALT = "b"

PATTERN = re.compile(r'(assets/([a-z0-9-]+\.svg))(\?v=[0-9a-z]+)?')


def digest(name):
    """Hash the bytes the repository holds, not the bytes on this disk.

    Git rewrites line endings in the working tree on Windows, so hashing the file as it
    sits here produces a value that never matches what is served, and the stamp stops
    meaning anything. Normalising first makes it stable on any machine."""
    path = os.path.join(ROOT, "assets", name)
    with open(path, "rb") as handle:
        content = handle.read().replace(b"\r\n", b"\n")
    return hashlib.sha256(content).hexdigest()[:8] + SALT


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
