# tools

Every drawing in `assets/` comes out of a generator here. Editing an SVG by hand drifts the
light and dark pair apart on the next change, so change the generator and re-run it.

```
python tools/gen_assets.py      the three rings, and the palette the rest import
python tools/gen_banner.py      the header and its rain
python tools/gen_prs.py         pull requests per year
python tools/gen_timeline.py    the nodes beside selected work, and its table
python tools/gen_radar.py       depth against focus
python tools/gen_tenure.py      years with each technology
python tools/gen_archetype.py   the package tree
python tools/gen_badges.py      the three contact badges

python tools/stamp_assets.py    always last
```

See [NUMBERS.md](NUMBERS.md) for where every figure on the page came from and the command
that produced it. They were measured on 21 September 2026 and should be re-measured, not
edited. Read the note at the top of it before running anything: `gh search prs` caps at
1000 results without saying so, and the reviewed-by query is past that cap.

`stamp_assets.py` rewrites each asset URL in the README with a hash of the file it points
at. GitHub proxies README images and caches them by URL: without this an updated drawing
keeps serving from the old copy, which looks exactly like a change that never landed.

## Weight

Every drawing is an `<img>` in a README, so its bytes and its animated element count are
both paid on every page view. Two rules hold the size down, and both are easy to undo by
accident:

- **Repeat a shape, do not re-emit it.** The banner's rain is two trail lengths against
  eight starting letters, so sixteen `<g>` in `<defs>` cover all forty columns twice over.
- **Share a style, do not inline it.** The skyline's lit windows are grouped by how they
  blink and drawn as one `<path>` per group -- `M123 456h5v7h-5z` a window -- instead of a
  `<rect>` carrying its own animation.

Between them the assets went from 376 KB to 224 KB with nothing removed from the page.
What a reader actually downloads is one of each light/dark pair: 189 KB to 113 KB.
