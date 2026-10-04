# Where the figures come from

Everything on the page was measured on **4 October 2026**. Nothing is estimated, and
nothing should be edited without re-measuring it, because the whole argument of the page is
that the numbers survive being checked.

Each figure below names the generator that holds it and the command that produced it.

---

## The 1000-result ceiling

`gh search prs` returns at most 1000 matches and says nothing when it truncates. The
reviewed-by query passed that ceiling in 2026: asked flat it answers 883, and asked year by
year it answers 963. **Every total below is a sum of per-year queries for that reason.**
Check it: if a flat query comes back at exactly 1000, it is not a count, it is a limit.

## Pull requests, reviews, people — `gen_banner.py`, `gen_prs.py`, `gen_assets.py`

```bash
for y in 2023 2024 2025 2026; do
  gh search prs --author=rafarolo --owner=virgoinc \
    --created="$y-01-01..$y-12-31" --limit 1000 --json number | jq length
  gh search prs --reviewed-by=rafarolo --owner=virgoinc \
    --created="$y-01-01..$y-12-31" --limit 1000 --json number,author \
    | jq '[.[] | select(.author.login != "rafarolo")] | length'
done
```

Reviews must exclude your own pull requests or the figure counts self-reviews. October
2026: 964 authored, 963 reviewed for others.

Distinct people reviewed — 17, again as a union across the years, not one flat query:

```bash
for y in 2023 2024 2025 2026; do
  gh search prs --reviewed-by=rafarolo --owner=virgoinc \
    --created="$y-01-01..$y-12-31" --limit 1000 --json author | jq -r '.[].author.login'
done | sort -u | grep -vc rafarolo
```

The merged share for the rings, which `gen_assets.py` still draws but the README no longer shows. **`state` comes back lowercase** — the query here asked for
`"MERGED"` and quietly answered zero:

```bash
gh search prs --author=rafarolo --owner=virgoinc --limit 1000 --json state \
  | jq '[.[] | select(.state=="merged")] | length'
```

814 merged of 964 opened, which is the 84% on the first ring. The denominator is everything
opened, so the 57 still open count against it; that is deliberate, and it is the same
denominator the figure has always used.

**When 2026 stops being partial**, drop the asterisk, the "9 of 12 months" label and the
projection from `gen_prs.py`, and set `DAYS_ELAPSED = DAYS_IN_YEAR`. Until then
`DAYS_ELAPSED` is the day of the year the measurement was taken — 277 for 4 October —
and the projection is every partial figure scaled by `DAYS_IN_YEAR / DAYS_ELAPSED`, which
at 277 days is +32%.

## Radar: depth against focus — `gen_radar.py`

Depth is years since the first role in which an area appears, from the CV.

Focus is each area's share of the last twelve months of pull requests, classified by title.
The classifier is `RULES` in `gen_radar.py`: the first area whose keywords appear in a
lowercased, accent-stripped title, padded with one space at each end, takes it. Observability
comes first, so a title about logging a denied access counts as logging; backend comes last
because every service here is a JVM service. A title matching nothing is not counted, and `MATCHED` and `WINDOW` hold how
many of each — 292 of 474 in the window to 4 October 2026.

Observability counts the request audit trail (`lib-audit`, `audit-api`) alongside metrics,
logs and traces: it records every request a service answers, which is what a log is for.
An `npm audit` or an audit of duplicated tasks is not counted, which is why those keywords
are spelled out instead of a bare `audit`.

To re-run it over a fresh window, fetch the titles and apply `RULES` to them:

```bash
gh search prs --author=rafarolo --owner=virgoinc \
  --created="2025-10-04..2026-10-04" --limit 1000 --json title > /tmp/window.json
```

Then update `AXES`, `MATCHED`, `WINDOW` and the three `NOTES` together — the notes name
which area leads, and after this window it is security, with observability second.

## Years with each technology — `gen_tenure.py`

From the LinkedIn experience history, counted from the first role in which each one appears.
Export the profile to PDF and read the dates; there is no API that gives this.

## Main stack today — `README.md`

The Core Technologies line of the current role on LinkedIn, regrouped by layer, with Azure AD
under its current name, Entra ID. Versions are the ones the platform runs, not the latest
released; change them when the platform moves, not when a release comes out.

## Coverage, sectors, platform size — `gen_assets.py`, `gen_banner.py`, `README.md`

SonarQube for the coverage pair, and the platform's own repository count for its size.
These move slowly; check them when the rest is refreshed.

The sector count is the only figure here that is not a measurement, so it is held to the
same rule as the ones that are: it counts what the page can name. The banner said eight
against five named anywhere in the repository, and is now five -- the `industries` line in
`gen_archetype.py`, which the README repeats as a bullet. Adding a sector means adding it
in all three places, and the count follows from the list rather than the other way round.

---

## After changing any of them

```bash
python tools/<the generator you touched>.py
python tools/stamp_assets.py          # always last
```

The README's `<details>` fallbacks and `alt` texts hold the same figures as the drawings.
Change one and the other disagrees silently, so change both.
