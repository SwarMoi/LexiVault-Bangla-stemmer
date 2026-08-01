# Session status — 2026-08-01

Read this first when picking the stemmer work back up.

## What we did this session

1. **Fixed and logged a real bug**: `der_initial_dict`'s `অন` prefix rule
   over-fires on `অনমনীয়` ("inflexible"), stripping it to `মনীয়` (not a
   real word) instead of the correct `অ` + `নমনীয়`. Logged to `to_fix.md`
   with root cause traced through `apply_ffth_rule`. Committed + pushed
   (`a0921a9`).

2. **Found and integrated two external academic gold sets** to benchmark
   the stemmer against something other than our own validation CSVs:
   - **Dasgupta & Ng (2007)**, 4,110 hand-segmented Bengali words —
     official site dead, recovered via a 2021 Wayback Machine snapshot.
   - **Ahmed et al. (2021, IEEE)**, "Gold Dataset for the Evaluation of
     Bangla Stemmer" — paywalled, fetched via Queen Mary University of
     London's institutional IEEE Xplore access. The PDF's embedded font
     doesn't map to standard Unicode, so all 215 rule+example lines were
     hand-transcribed from visually-read zoomed screenshots (confirmed:
     plain text extraction/scraping would have produced corrupted Bangla
     either way — this isn't a PDF-vs-HTML problem, IEEE has no full-text
     HTML for conference papers anyway).

   Both sources are in `data/external_gold/<source>/` with a `SOURCE.md`
   each documenting provenance, license status (neither states one — kept
   as research-reference, not redistribution-cleared), and caveats.
   `evaluate_dasgupta_ng.py` and `evaluate_ahmed_et_al.py` (repo root) run
   the comparisons. Committed + pushed (`dd97d63`).

3. **Read Thompson, *Bengali* (2012), ch. 4 "Word formation" (printed
   pages 36–46)** in full — a commercial linguistics textbook, not one of
   the two academic papers above — to expand `der_initial_dict`/
   `der_final_dict` beyond the original handful of prefixes/suffixes.
   Added 10 new prefixes and 7 new suffixes, all cited from the book with
   a page reference in the code comments.

   **Caught two real regressions** by re-running the `output_validated.csv`
   `Correct=1` baseline after adding everything (37 words correct → still
   94/94 baseline, this is the important number): `প্র-` broke `প্রজাপতি`
   ("butterfly", not a real `প্র-`+root word) and `-তা` broke `দুর্লতা`/
   `দুশ্চিন্তা`. Both reverted, with the failing examples documented in
   `to_fix.md` so nobody re-adds them without knowing why they were pulled.
   Baseline is back to clean **94/94**.

   Also logged (not added, deliberately) every other affix from that
   chapter that looked too collision-prone without a lexicon: bare `আ-`,
   `নি-`, `সু-`, the `-আমি` suffix (collides with the pronoun "আমি" = "I"),
   `-পর` (collides with the common word "পর" = "other/after"), and every
   suffix needing a root-vowel change to strip correctly (`-ik`, `-o`,
   etc. — same "no vowel-harmony machinery" gap as the already-flagged
   `ে.ে` bug).

   **Not yet committed** — staged locally for the commit below, not pushed.

## Current repo state (as of this session's end)

- `to_fix.md` now has **7 open issues**, all needing linguistic judgment
  before any further rule changes — see that file for the full list.
- `output/corpus_sample_validated.csv` is **still mid-review** — it showed
  as open/locked in a spreadsheet app all session (git status: deleted,
  unstaged). Untouched by anything done here. **This is still the actual
  next concrete step**, unrelated to everything else in this file.
- **`Bengali (Thompson).pdf` is sitting untracked in the repo root** — a
  full commercial textbook, not an open-access paper like the other two
  external-gold sources. Deliberately left untracked/uncommitted tonight;
  **needs to be moved out of the git working tree before this repo is ever
  pushed further or made public**, to avoid redistributing copyrighted
  material. Not urgent tonight since it can't get swept into a commit that
  wasn't explicitly `git add`ed, but don't forget it.
- External gold scores after tonight's Thompson-derived rule additions:
  Dasgupta & Ng 36.6% (was 37.5%), Ahmed et al. 31.6% (was 33.3%) — both
  dipped slightly. Part of this is real (a few new short prefixes catching
  coincidental false positives on unfiltered vocabulary that the curated
  94-word set doesn't expose), but part is a measurement confound:
  `evaluate_dasgupta_ng.py`'s "is this chunk a known prefix" heuristic
  reads `der_initial_dict` directly, so growing that dict also changed
  what the *evaluation* counts as a prefix chunk, not just what the
  stemmer does. Not separated out — worth doing before trusting these
  numbers for anything more than a rough sanity check.

## Plan for next session

1. **Check on the `corpus_sample_validated.csv` manual review** — ask
   whether it's done; if so, that unblocks prioritizing which `to_fix.md`
   item to tackle first.
2. **Move `Bengali (Thompson).pdf` out of the repo** before doing anything
   that could push or publicize it further.
3. **Decide whether to push tonight's local-only commit** (grammar.py +
   README.md + to_fix.md + STATUS.md + the two refreshed comparison CSVs)
   to `origin/main`.
4. Optionally: separate the real-false-positive-rate from the measurement-
   confound in the external gold score dip, if it seems worth trusting
   those numbers going forward.
5. Longer-term, still unstarted: packaging the stemmer as a real importable
   package (currently a `sys.path` hack from `bangla_corpus/stats.py`), and
   the stem-level statistics phase (stem frequency / transition
   probability) once the stemmer is validated enough to trust.
