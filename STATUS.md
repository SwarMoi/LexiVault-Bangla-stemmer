# Session status — 2026-08-05

Read this first when picking the stemmer work back up.

## What we did this session

1. **Housekeeping, overdue since Aug 1**: pushed the 2 local-only commits
   to `origin/main` (`3f78233..b86e04e`). Moved `Bengali (Thompson).pdf`
   (full commercial textbook, was sitting untracked in the repo root)
   out of the git working tree entirely, onto the external drive at
   `/Volumes/G-DRIVE-PRO/bangla-lexical-corpus-data/docs/LexiVault-Bangla-stemmer/`
   — it was never committed, so no history to scrub, and nothing in code
   referenced its path (only page-number citations in `grammar.py`
   comments), so no symlink needed back in the repo.

   Also: all of this repo's own `.md` docs (`README.md`, `STATUS.md`,
   `to_fix.md`, both `external_gold/*/SOURCE.md`) were moved the same
   way this session, replaced with symlinks in-repo — see the parent
   `bangla-lexical-corpus` repo's `HANDOFF.md`/`corpus.md` for why
   (getting project docs out of the Dropbox sync path). Doesn't change
   how anything reads — `open('STATUS.md')` etc. still works.

2. **Started Task #14 (POS-tagging for the vowel-harmony gate), Phase A
   proof-of-concept.** Goal: replace the hardcoded
   `grammar.ee_harmony_roots = {হাস, নাচ}` whitelist with a real POS-tag
   gate on `sp_final_dict`'s `ে.ে` rule (only fire on verbs).

   - Installed `bnlp-toolkit` (4.4.1) into the main repo's `.venv`
     (Python 3.12) — confirmed CPU-only, no `torch` pulled in, matches
     what was expected when this tool was chosen.
   - API note for next time: `bnlp.create_pos_pipeline()` is currently
     broken in this version (`'BengaliPOS' object is not callable` —
     looks like a real bug in bnlp-toolkit's own `Pipeline` wiring, not
     something on our end). Bypassed it — use `bnlp.BengaliPOS` directly:
     ```python
     from bnlp import BengaliPOS
     tagger = BengaliPOS(model_path='/Users/lab/bnlp/models/bn_pos.pkl')
     tagger.tag('সে জোরে হেসে উঠল।')  # -> [('সে','PPR'), ('জোরে','NC'), ('হেসে','VM'), ('উঠল','VAUX'), ('।','PU')]
     ```
     The `bn_pos.pkl` CRF model (3.7MB) auto-downloads on first use to
     `~/bnlp/models/`. Verb tags to treat as "VERB" for the gate: `VM`,
     `VAUX`.
   - **Tested on the actual target words**, both in a full sentence and
     as a bare isolated word (the real input shape — the stemmer runs on
     `lexicon.parquet` word *types*, not sentences, so sentence-context
     wasn't guaranteed to transfer):
     | word | in context | bare word | expected |
     |---|---|---|---|
     | হেসে (whitelisted) | VM ✓ | VM ✓ | VERB |
     | নেচে (whitelisted) | VM ✓ | VM ✓ | VERB |
     | ছেলে (the actual false-merge target, noun "boy") | NC ✓ | NC ✓ | NOT_VERB |
     | দেখে (not whitelisted, currently left unstemmed) | VM ✓ | VM ✓ | VERB |
     | খেলে (not whitelisted) | NC ✗ | NC ✗ | VERB (missed both times) |
     | ঠেলে (not whitelisted) | VM ✓ | VM ✓ | VERB |

     **11/13 (85%)**, clears the plan's ≥70% go/no-go bar, and — the
     important part — accuracy barely dropped with zero sentence context
     (6/7 → 5/6), so the CRF's per-token/suffix features carry most of
     the signal, not context. The one consistent miss, `খেলে`, is
     genuinely ambiguous even to a human reading it with no context (verb
     "plays" vs. a citation-form noun reading).

   **This is a real signal, not a rigorous go/no-go** — n=13 is 6
   hand-picked words tested twice, not a proper sample. Not yet decided
   whether/how to scale this to Phase B.

## Current repo state (as of this session's end)

- `to_fix.md` still has its prior 5 open issues (Sanskrit-prefix
  over-firing beyond the 9-word seed, `কর`/`কার` surname collision, the
  `া.া.ার` two-wildcard conflation, remaining `sp_final_dict`
  over-stripping cases, Thompson affixes not added) — none touched this
  session.
- `output/corpus_sample_validated.csv`: **380/400 rows reviewed**, 20
  genuinely-ambiguous rows still blank, awaiting your own linguistic call
  — unchanged this session, still the same 20 as of Aug 4.
- Nothing in `grammar.py`/`stemmer.py` changed this session — Phase A was
  pure feasibility-testing in a scratch script, not committed anywhere
  (no repo file to point to; the table above is the full record).
- `bnlp-toolkit` is installed in the **main repo's** `.venv`, not this
  repo's — this repo still has no `pyproject.toml`/`requirements.txt` of
  its own (same unresolved packaging gap as ever, see "Not yet resolved"
  in the parent repo's stemmer-state notes).

## Plan for next session

1. **Decide Phase B scope** for the POS-tagging gate: build a real
   validation sample (e.g., pull every `ে.ে`-shaped word type above the
   frequency floor from `lexicon.parquet`, tag them all, hand-review a
   random subset) rather than trusting 13 hand-picked words. This is the
   next concrete step for Task #14.
2. Still pending from before: finish the 20-row `corpus_sample_validated.csv`
   review (your own judgment).
3. Still open, untouched: the 5 `to_fix.md` items, in particular the
   narrowly-scoped `কর`/`কার` surname collision (smallest, most
   self-contained of the remaining items if you want a quick win instead).
