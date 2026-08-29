# tools

Every drawing in `assets/` comes out of a generator here. Editing an SVG by hand drifts the
light and dark pair apart on the next change, so change the generator and re-run it.

```
python tools/gen_assets.py      banner ground, rings, skyline
python tools/gen_banner.py      the header and its rain
python tools/gen_prs.py         pull requests per year
python tools/gen_timeline.py    selected work
python tools/gen_radar.py       depth against focus
python tools/gen_tenure.py      years with each technology
python tools/gen_archetype.py   the package tree
python tools/gen_badges.py      the three contact badges

python tools/stamp_assets.py    always last
```

`stamp_assets.py` rewrites each asset URL in the README with a hash of the file it points
at. GitHub proxies README images and caches them by URL: without this an updated drawing
keeps serving from the old copy, which looks exactly like a change that never landed.
