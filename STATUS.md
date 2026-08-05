# Session status — 2026-08-05

Read this first when picking the stemmer work back up.

## What we did this session

1. **Housekeeping, overdue since Aug 1**: pushed the 2 local-only commits
   to `origin/main`. Moved `Bengali (Thompson).pdf` (full commercial
   textbook, was sitting untracked in the repo root) out of the git
   working tree entirely, onto the external drive at
   `/Volumes/G-DRIVE-PRO/bangla-lexical-corpus-data/docs/LexiVault-Bangla-stemmer/`
   — never committed, so no history to scrub, and nothing in code
   referenced its path (only page-number citations in `grammar.py`
   comments). **Note**: an earlier attempt this session to also move the
   repo's own `.md` docs onto the drive (symlinks in-repo) was tried and
   then reverted the same session — it silently broke git tracking of
   doc edits, and the copyrighted PDF briefly, confusingly reappeared in
   the repo mid-session (Dropbox restoring it faster than expected after
   the first move). Docs are back to being regular tracked files;
   PDF-off-repo is the only thing that stuck from that detour.

2. **Task #14 (POS-tagging for the vowel-harmony gate) — ran the
   proof-of-concept, then pivoted based on what it found.**
   `bnlp-toolkit` (4.4.1) installed into the main repo's `.venv`,
   confirmed CPU-only. API note: `bnlp.create_pos_pipeline()` is broken
   in this version (`'BengaliPOS' object is not callable`); use
   `bnlp.BengaliPOS(model_path=...).tag(text)` directly — model
   auto-downloads to `~/bnlp/models/bn_pos.pkl` on first use. Verb tags:
   `VM`, `VAUX`.

   Small hand-picked test (13 words) looked promising (85%), but a
   properly-built sample said otherwise: constructed the real 477-word
   candidate set (every `ে.ে`-shaped `lexicon.parquet` type, freq>=100,
   whose `stem()` output actually depends on the `ee_harmony_roots`
   gate — not a raw regex guess, which overcounts ~15x by also catching
   words other rules intercept first). On the top 40 by frequency,
   POS-verb-tagging hit 73.7% — clears the plan's ≥70% bar on paper, but
   would have wrongly transformed 7 of the highest-frequency words
   (`দেখে` 8.2M corpus occurrences, `ফেলে`, `দেবে`, `নেবে`, `মেলে`,
   `ঠেলে`, `বেগে`) into garbage roots. Root cause: verb-tagging can't
   distinguish real harmony roots (`রাখ→রেখে`) from verbs whose root
   already ends in a bare e (`দেখ→দেখে`) — both are just "VERB" to a POS
   tagger. That's a different, finer-grained distinction than POS
   category.

   **Pivoted**: this is actually a closed lexical class (a fixed,
   learnable list of Bengali verb roots), not an open-class disambiguation
   problem — so directly expanding the whitelist from data beats gating
   with POS tags. Cross-validated all 477 candidates against the lexicon
   itself (does `root+া` and `root+তে` both exist with real, comparable
   frequency?) and expanded `ee_harmony_roots` from 2 roots to 30. Full
   detail, evidence, and the 6 held-back candidates are in `to_fix.md`'s
   "Resolved this session" entry — don't re-derive here.

   Verified: **94/94 baseline**, external gold flat (Dasgupta & Ng
   42.7%, Ahmed et al. 33.9% — unchanged, different vocabulary than what
   this fix targets), but **31 word types / ~33M token occurrences** in
   the real corpus now correctly reduce to their root instead of being
   left unstemmed.

   `bnlp-toolkit` stays installed — it works, just wasn't the right tool
   for *this specific rule*. Worth remembering for anything that's a
   genuine open-class distinction (e.g. the `কর`/`কার` occupational-
   suffix-vs-surname problem might be a better fit, since surnames vs.
   common nouns is closer to what a tagger's actually good at than a
   closed morphological class was).

3. **Same session, picked back up after "go ahead"**: what looked like a
   `dot_replace`-preserves-candrabindu bug turned out, on inspection, to
   be a different and separate gap — the plain `ে.ে` pattern structurally
   can't match candrabindu-bearing words at all (they're 5 codepoints,
   not 4), so those words were being left completely unstemmed, not
   mis-stemmed. The original 5 held-back roots (`কাদ`/`বাচ`/`ঘাট`/`কাপ`/
   `হাট`) were never a candrabindu issue in the first place — each
   collides with an unrelated, higher-frequency word using the exact
   same 4-codepoint spelling instead (`কাদা` "mud", `ঘাট` "riverbank"
   noun, `কাপ` "cup" loanword, `হাটে` "at the market", `বাচ` swamped by
   `বেচে` "sells", an unrelated verb). Corrected `to_fix.md`'s record
   rather than leave the wrong diagnosis standing.

   Added a real fix for the actual gap: a second `sp_final_dict` key,
   `'েঁ.ে'`, alongside the plain `'ে.ে'` one, gated by the same
   `ee_harmony_roots` whitelist (`ee_harmony_rule_key` → plural
   `ee_harmony_rule_keys`, a set of both). Ran the identical
   candidate-discovery + corpus cross-validation methodology on the
   134-word candrabindu-shaped candidate set: **7 roots** cleared the
   threshold (`বাঁধ`/`হাঁট`/`বাঁচ`/`কাঁদ`/`কাঁপ`/`গাঁথ`/`রাঁধ` — tie,
   walk, survive, cry, tremble, string/thread, cook), covering **~4.2M**
   more token occurrences. Correctly left alone: `পেঁপে` "papaya" (noun),
   `বেঁটে` "short" (adjective) — same surface shape, not verbs. Full
   detail in `to_fix.md`'s "Resolved this session" entry.

   94/94 baseline holds; external gold flat again (same reasoning as the
   first fix — different, smaller vocabulary than either fix targets).

## Current repo state (as of this session's end)

- `to_fix.md` now has **5 open issues** (net: added the candrabindu gap,
  then fully resolved it the same session, so it nets out to one fewer
  than this session started with).
- `output/corpus_sample_validated.csv`: still **380/400** reviewed, same
  20 blank rows as before — untouched this session.
- Committed and pushed to `origin/main`: the housekeeping revert, the
  `ee_harmony_roots` expansion, and the candrabindu-pattern fix. Check
  `git log` for exact hashes if picking this up later; not re-stating
  them here since STATUS.md itself isn't the source of truth for that,
  git is.

## Plan for next session

1. Still pending: finish the 20-row `corpus_sample_validated.csv` review
   (your own linguistic judgment).
2. Pick a `to_fix.md` item. Candidates, roughly by effort:
   - **`কর`/`কার` surname collision** — smallest untouched item; possibly
     a genuine fit for `bnlp-toolkit`'s POS/NER tagging now that it's
     installed and proven to work (surname vs. common-noun is a more
     POS-taggable distinction than the closed harmony-verb class was).
   - Sanskrit-prefix over-firing beyond the 9-word seed, or the
     `া.া.ার` two-wildcard conflation — both still need a lexicon-style
     check, no new idea for either this session.
   - Lower-confidence harmony roots left out this session (`ঘাঁটা`
     "rummage", `ভাঁজ` "fold", `ছাঁটা` "trim", `ফাঁপা` "swell", `ফাঁসা`
     "get trapped") could be revisited with a relaxed threshold or a
     manual per-word confirmation instead of pure corpus evidence.
3. Longer-term, still unstarted: packaging as a real importable package,
   and the stem-level statistics phase once a "good enough" call is made.
