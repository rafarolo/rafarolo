# Where the figures come from

Everything on the page was measured on **29 August 2026**. Nothing is estimated, and nothing
should be edited without re-measuring it, because the whole argument of the page is that the
numbers survive being checked.

Each figure below names the generator that holds it and the command that produced it.

---

## Pull requests, reviews, people — `gen_banner.py`, `gen_prs.py`, `gen_all.py`

```bash
gh search prs --author=rafarolo   --owner=virgoinc --limit 1000 --json number | jq length
gh search prs --reviewed-by=rafarolo --owner=virgoinc --limit 1000 --json number,author \
  | jq '[.[] | select(.author.login != "rafarolo")] | length'
```

Reviews must exclude your own pull requests or the figure counts self-reviews.

Per year, for the chart in `gen_prs.py`:

```bash
for y in 2023 2024 2025 2026; do
  gh search prs --author=rafarolo --owner=virgoinc \
    --created="$y-01-01..$y-12-31" --limit 1000 --json number | jq length
done
```

Distinct people reviewed, and the merged share for the rings:

```bash
gh search prs --reviewed-by=rafarolo --owner=virgoinc --limit 1000 --json author \
  | jq '[.[].author.login] | unique | length'
gh search prs --author=rafarolo --owner=virgoinc --limit 1000 --json state \
  | jq '[.[] | select(.state=="MERGED")] | length'
```

**When 2026 stops being partial**, drop the asterisk, the "8 of 12 months" label and the
projection from `gen_prs.py`, and set `DAYS_ELAPSED = DAYS_IN_YEAR`.

## Radar: depth against focus — `gen_radar.py`

Depth is years since the first role in which an area appears, from the CV. Focus is each
area's share of the last twelve months of pull requests, classified by title — the rules and
the counts are in `gen_radar.py`'s `AXES`. Re-run the classification over a fresh window and
update both the numbers and the footnote saying how many of the total matched.

## Years with each technology — `gen_tenure.py`

From the LinkedIn experience history, counted from the first role in which each one appears.
Export the profile to PDF and read the dates; there is no API that gives this.

## Coverage, sectors, platform size — `gen_all.py`, `gen_banner.py`, `README.md`

SonarQube for the coverage pair, the CV for the sector count, and the platform's own
repository count. These move slowly; check them when the rest is refreshed.

---

## After changing any of them

```bash
python tools/<the generator you touched>.py
python tools/stamp_assets.py          # always last
```

The README's `<details>` fallbacks hold the same figures as the drawings. Change one and the
other disagrees silently, so change both.
