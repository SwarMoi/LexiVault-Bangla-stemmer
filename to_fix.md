# Known issues

## `der_initial_dict`'s Sanskrit prefixes over-fire on lexicalized compounds — partially resolved

The `corpus_sample_validated.csv` 400-word sample was reviewed this
session (Claude first pass — flagged `Correct`/`Remarks` on every row that
changed under `stem()`, left ~20 genuinely uncertain rows blank for you;
**this is a draft, not a substitute for your own read of it**). Of the 201
words the stemmer actually transforms, 38 were wrong, and most trace back
to one recurring cause: the same problem that made `অন` get removed
entirely also affects several of its still-present neighbors — `বি`,
`অতি`, `পরি`, `অভি`, `সম`, `নির্`. Each is a real Sanskrit prefix in the
abstract, but the specific word it's firing on here has become a fully
lexicalized, monomorphemic compound in modern Bangla, so stripping the
"prefix" produces a false merge or garbage.

**Fixed this session for the 9 confirmed cases**: `grammar.py` now has a
`protected_prefix_roots` tuple (`বিশ্বাস`, `অতিথি`, `নির্বাচন`, `সমঝোতা`,
`বিশিষ্ট`, `বিরতিস্পেস`, `পরিবর`, `বিলিরি`, `বিছট`), checked in
`apply_ffth_rule` via `word.startswith(...)` against the word as it
arrives at the prefix stage (i.e. after inflectional stripping) — matches
skip prefix-stripping entirely rather than trying to guess which specific
rule would have false-fired. `startswith` rather than exact-match so it
also covers untested inflected forms sharing the same root, not just the
9 literal words tested. Verified: 94/94 baseline, 9/400 corpus-sample
words changed (all were the intended fixes, e.g. `বিশ্বাসগুলোই` →
`বিশ্বাস` instead of `শ্বাস`), external gold ticked up slightly again
(Dasgupta & Ng 42.6%→42.7%, Ahmed et al. 33.3%→33.9%).

**Still open** — this is a 9-word seed list, not a general solution, and
several confirmed-bad words from the review were deliberately left out
because the damage happens *before* the prefix stage even runs (so
protecting the prefix stage alone doesn't fully fix them):
`অধিকারবাদের`, `বিভ্রান্তিতেও` (suffix-side now clean, but `বি-` still
merges the prefix-stripped result into `ভ্রান্তি`), `অতিতির`,
`বিশ্বাধার`, `অভিযোগকারিণীর`. Full list with remarks in
`output/corpus_sample_validated.csv` (`Correct=0` rows). Extending
`protected_prefix_roots` word-by-word as more cases turn up is fine, but
a real general fix still needs either a proper lexicon or removing each
collision-prone prefix the way `অন` was — both bigger asks than this
session took on.

## `der_final_dict`'s `কর` occupational suffix over-fires on names/compounds ending the same way

Found in the same corpus review: `কর` (der_final_dict, "assigning a
quality") strips from words that aren't root+suffix at all —
`নারভেকর` → `নারভে` (surname "Narvekar"), `পালকর` → `পাল` (surname
"Palkar"), `চর্মকার` → `চর্মকা` (should stay `চর্মকার`, "leather
worker" — `কার` here is the actual occupational-agent morpheme, not this
suffix, but the two collide). Same "no lexicon" failure class as the
prefix issue above; not fixed this session.

## Several `sp_final_dict` possessive/case rules still over-strip on multi-syllable compounds

Also found in the corpus review, distinct from the now-fixed `ার`/`া.ার`
cases: words where a trailing `র` looks like the possessive marker but is
actually the compound's own final consonant get the `র` stripped anyway,
producing a broken remainder. Three of the five originally-found examples
are now patched via `data/word_stem_overrides.csv` (see "Resolved this
session" below): `পরীক্ষাগারেও`, `শর্তানুসারে`, `ডাকচিৎকারে`. Still open,
same class, not yet individually confirmed/patched: `সত্যিকারই` →
`সত্যিকা` (likely `সত্যিকার`), `মধ্যমকুমার` → `মধ্যমকুমা`. Root cause
still not traced to one specific rule (these come from different `ার`-
family entries firing on compounds where the trailing consonant is the
compound's own, not a case marker) — the per-word override table is a
patch for confirmed cases, not a fix for the underlying pattern.

## `sp_initial_dict` stacked-suffix peeling — partially resolved, scoped narrowly on purpose

`stem()` runs a fixed chain of six stages, each of which tries its rule
table once, applies at most one match, and hands off to the next stage
without revisiting an earlier table against the newly-shortened word. This
meant a word with two stacked suffixes from the *same* dictionary only got
one of them stripped, e.g. `মালিতেও` → `মালিতে` (only the emphatic `ও` was
stripped; the locative `তে` exposed afterward belongs to `sp_initial_dict`,
the table that had already run).

**Fixed this session, but only for `sp_initial_dict` (stage 1)**:
`_stem_one` now loops stage 1 to a small fixpoint (`মালিতেও` → `মালিতে` →
`মালি`) before running the rest of the chain exactly once, unchanged.
`মিঠুকেও` → `মিঠু` and `বিভ্রান্তিতেও` → `ভ্রান্তি` (suffix-wise; the
`বি-` merge itself is the separate, still-open issue above) fixed the same
way; `অষ্ট্রেলিয়াতেও` reaches the full `অষ্ট্রেলিয়া` instead of stopping
at `অষ্ট্রেলিয়াতে`. Verified against the 94-word baseline (still 94/94)
and the full 400-word corpus sample (4 words changed, all improvements,
zero regressions); external gold scores both ticked up slightly
(Dasgupta & Ng 41.8%→42.6%, Ahmed et al. 31.6%→33.3%).

**A broader version — looping every stage, not just stage 1 — was tried
and reverted.** It fixed the same cases plus a few more (e.g.
`নেচেছি`→`নাচ`), but empirically introduced *as many new regressions* on
the same 400-word sample: previously-correct outputs got re-processed a
second time and over-fired on proper nouns/loanwords that coincidentally
match a rule's ending, e.g. `ফোটোগ্রাফারদের` (photographers) correctly
gave `ফোটোগ্রাফার` on one pass, but a second pass let `sp_final_dict`'s
`ার` rule fire again on that already-correct result, giving `ফোটোগ্রাফা`;
similarly `গ্যালাতাসারাই` (Galatasaray, a proper noun) went from the
correct `গ্যালাতাসারা` to the wrong `গ্যালাতাসা` when `sp_initial_dict`'s
`রা` (plural) key got a second try. Every rule in this stemmer is a bare
regex with no lexicon behind it, so a second pass has no way to tell "a
genuinely exposed new suffix boundary" from "a coincidental match on an
already-complete word" — the same wall this file keeps hitting elsewhere
(`ে.ে`, `অন`, `া.া.ার`). Restricting the loop to *only* stage 1, and only
letting it re-fire the bare case markers (`তো`/`কে`/`তে`) rather than the
full table (`ই`/`ও`/`রা` excluded — see `first_dict_repeat` in
`stemmer.py`), was the narrowest scope that fixed the cited bug with zero
observed regressions; extending it further needs the lexicon this session
keeps deferring to, not more manual tuning of which keys are "safe."

Stages 2–4 (`con_rep_dict`/`obv_rep_dict`/`sp_final_dict`) and the
derivational stages still run exactly once each, as originally designed.

There's a related, narrower instance of the same "leftmost re.search match
wins, no rescanning" limitation: single-character patterns like the bare
`-ে` rule (`con_rep_dict`, added to fix the gap below) only fire when their
one match happens to be the word's *last* character occurrence of that
letter. A word with an earlier, unrelated `ে` (e.g. `দেখে`, where the first
`ে` is part of the root's own spelling) never reaches the bare-`ে` rule at
all, because `re.search` finds that earlier occurrence first, fails the
end-anchor check, and there's no retry against a later occurrence of the
same pattern. `দেখে` currently falls through to `sp_final_dict`'s `ে.ে`
rule instead (now correctly left unchanged rather than false-merged, see
below, but still not reduced to its own paradigm's `দেখ` root).

## `sp_final_dict`'s `া.া.ার` rule conflates two different constructions and truncates on top of it

`া.া.ার` (two wildcards, meant for patterns like `নামাবার`/`জানালার`) has
two separate problems, found while fixing the simpler one-wildcard `া.ার`
rule (resolved this session, see below):

1. **Template-length bug**: its replacement string `া.া` only has *one*
   dot, but the pattern it's replacing has *two* wildcard positions. Since
   `dot_replace` only walks as far as the replacement string is long, the
   second consonant+vowel pair is silently dropped regardless of which
   branch fires: `জানালার` ("of the window") → `জানা` ("knowing" — a
   real but completely unrelated word), losing `ল`+`া` entirely. Should
   be `জানালা`.
2. **Conflates two real but different segmentations** that happen to
   share this surface shape, and a lexicon-free regex can't tell them
   apart: (a) causative verb root + `া` + the `-বার` gerund/infinitive
   suffix, e.g. `নাম`(root)+`া`(causative)+`বার`(gerund) = `নামাবার`,
   correct stem `নামা` — here the "second wildcard" position is actually
   *inside* the suffix being stripped, not part of the root; vs.
   (b) vowel-final noun root + bare `-র` possessive, e.g.
   `জানালা`(window)+`র` = `জানালার`, correct stem `জানালা` — here the
   second wildcard position *is* part of the root and must be kept.
   Fixing (1) naively (extending the replacement to `া.া.া` to stop
   truncating) fixes case (b) but breaks case (a) (`নামাবার` would become
   `নামাবা` instead of the correct `নামা`). Left unfixed this session
   since neither branch can be made correct for both cases without a
   lexicon check on the reconstructed root — same class of problem as the
   `ে.ে` harmony rule (now gated by `grammar.ee_harmony_roots`) and the
   removed `অন` prefix.

## Derivational affixes found in Thompson (2012) but not added to `grammar.py`

Thompson, *Bengali* (2012), ch. 4 "Word formation" (p.36-46) was read in
full to expand `der_initial_dict`/`der_final_dict` beyond the original
handful of prefixes/suffixes. Most of what's in that chapter was added
(see the `README.md` list and the comments in `grammar.py`), but several
attested affixes were tried and reverted, or skipped outright:

- **`প্র-`** (Sanskrit "forth, abundance, excess, inception") — added, then
  reverted: regressed `প্রজাপতি` ("butterfly", a single lexical item with
  no real `প্র-` prefix meaning — the initial letters are coincidental)
  from unchanged to `জাপতি` against `output/output_validated.csv`'s
  `Correct=1` baseline.
- **`-তা`** (very productive abstract-noun suffix, "-ness/-ity") — added,
  then reverted: regressed two words by firing on a coincidental `তা`-
  ending in a single lexical item rather than a real root+suffix boundary,
  and — worse — pre-stripping it *before* the প্রতি-family prefix stage
  got a chance to run its own correct one-shot strip on the same word
  (stage-ordering interaction, same root issue as this file's first
  entry): `দুর্লতা` ("creeper/vine") → `ল` instead of unchanged, and
  `দুশ্চিন্তা` → `চিন্` instead of the correct `চিন্তা`.
- **Bare `আ-`** (Sanskrit/Bangla "starting from") — not added. Single
  character, and unlike the 2-character prefixes already in the dict
  (`বি`, `উদ`), a bare vowel prefix is likely to coincide with a
  huge number of words that simply start with `আ` for unrelated reasons.
  Untested; flagging the risk rather than either adding or ruling it out.
- **Bare `নি-`** (Sanskrit/Bangla negating, alongside the already-present
  `নির্-`) — not added, same reasoning: `নি` is a very common word-initial
  sequence unrelated to this prefix (e.g. `নিজ`, `নিয়ে`).
- **`সু-`** (Sanskrit/Bangla "good") — not added, same short-prefix
  collision concern; untested.
- **`-আমি`/`-আকি`** (noun suffix for "a deliberately assumed attitude",
  e.g. `পাগলামি` "madness" from `পাগল`) — not added: `আমি` is also the
  extremely high-frequency first-person pronoun "I", and stripping it as
  a suffix risks false-positiving on any word that coincidentally ends in
  those letters.
- **`-পর`** (the `কর`/`পর` adjective-forming pair, e.g. `স্বার্থপর`
  "selfish") — only `কর` was added; `পর` was left out because it's also
  a very common independent word ("other/after"), same collision class.
- Suffixes needing a **root-vowel change** to strip correctly weren't
  added at all, since the current architecture has no general vowel-
  harmony machinery beyond the small, explicitly-whitelisted `ে.ে` case
  (see `grammar.py`'s `ee_harmony_roots`): `-ik` (আঞ্চলিক ← অঞ্চল), `-o`
  (মেজো ← মধ্য), `-i` from `-o` adjectives (নীতি ← নীত), and the
  jɔphɔla/bɔphɔla abstract nouns (Ch.4 §4.3.iii).
- **Farsi/Arabic loan prefixes** (`বে-`, `দর-`, `না-`, `বদ-`, `গর-`,
  `আম-`, listed in the same chapter) weren't added — different register/
  etymology than the rest of `der_initial_dict`, and untested against
  loanword vocabulary.

## `sp_final_dict`'s `ে.ে` rule drops চন্দ্রবিন্দু (candrabindu) on roots that need one

Found while cross-validating candidate `ee_harmony_roots` additions
(2026-08-05, see "Resolved this session" below): `dot_replace`'s
`ে.ে` → `া.` substitution doesn't preserve a candrabindu that belongs on
the reconstructed root. 5 real harmony verbs need one —
`কাঁদ` (কেঁদে "having cried"), `বাঁচ` (বেঁচে "having survived"), `ঘাঁট`
(ঘেঁটে "having rummaged"), `কাঁপ` (কেঁপে "having trembled"), `হাঁট`
(হেঁটে "having walked") — but the mechanical output comes out
candrabindu-less as `কাদ`/`বাচ`/`ঘাট`/`কাপ`/`হাট`, and every one of those
happens to collide with an unrelated real word too (`কাদা` "mud", `ঘাট`
"riverbank/dock", `কাপ` "cup" loanword, `হাট` "market" — this last one is
why the corpus-evidence check for `হাট` looked strong at all: its
frequency is dominated by the noun reading, `হাটে` "at the market", not
the verb; `বাচ` alone isn't a real word but still isn't the right root).
Deliberately held all 5 back from `ee_harmony_roots` rather than add them
with a known-wrong output. Fixing this needs `dot_replace` (or a small
special-case list) to reattach the candrabindu, not just avoid the words
— not attempted this session. (A 6th candidate, `হাজ`, was held back for
an unrelated reason — see "Resolved this session" below.)

---

**Resolved this session** (verified against the 94 `Correct=1` rows in
`output/output_validated.csv`, 0 regressions each time):

- **2026-08-05**: Expanded `grammar.py`'s `ee_harmony_roots` from
  `{হাস, নাচ}` to 30 roots. Originated from Task #14 (paused POS-tagging
  plan): built `bnlp-toolkit` into the main repo's `.venv` and tested
  POS-verb-tagging as the gate instead of a hardcoded whitelist, but
  found it doesn't work for this rule specifically — verb-tagging can't
  distinguish real harmony roots (`রাখ→রেখে`) from verbs whose root
  already ends in a bare e (`দেখ→দেখে`, `ফেল→ফেলে`); on a 40-word
  frequency-ranked real sample it would have wrongly transformed 7 of the
  highest-frequency candidates (`দেখে` 8.2M corpus occurrences, `ফেলে`
  3.6M, `দেবে` 3.1M, `নেবে`, `মেলে`, `ঠেলে`, `বেগে`) into garbage roots.
  Pivoted instead to what the data showed this actually is: a **closed**
  lexical class. Built the full 477-word candidate set (every
  `lexicon.parquet` type, freq >= 100, whose `stem()` output differs
  between the whitelist gate on vs. off — a precise superset, not a raw
  `ে.ে$` regex guess, which overcounts ~15x by also matching words other,
  earlier-priority rules intercept first). Cross-validated each candidate
  root against the lexicon itself: a genuine root should appear as both
  `root+া` (infinitive/verbal noun) and `root+তে` (purposive infinitive)
  with real, comparable frequency; coincidental matches (`তা+ার`="তার"
  the pronoun, noun `মাথা`→root-shape `মাথ`) don't. Threshold: both
  forms >=5000, neither more than 50x the other — 34 candidates cleared
  it, 6 held back (5 for a newly-found candrabindu bug, see the open
  issue above; 1, `হাজ`, for weak/inconsistent evidence), leaving 28
  confirmed new roots. No change on either external gold set (different,
  smaller vocabulary — expected), but 31 word types / **~33M token
  occurrences** in the real corpus now correctly reduce to their root
  instead of being left unstemmed. `bnlp-toolkit`/POS-tagging is proven
  to work and stays installed for other uses; just not this rule.
- Added `data/word_stem_overrides.csv` and wired it into `stemmer.py`
  (`_stem_one`, checked first, before `closed_class_words`): a small,
  individually-confirmed word → correct-stem lookup for 10 words found via
  cross-checking against Morphemo (an independent statistical
  morpheme-boundary predictor adapted for Bangla this session — see the
  main `bangla-lexical-corpus` repo's `src/morphemo_audit.py` and
  `HANDOFF.md`'s "Morphemo" section). Fixes: `চৌকীদারকে`→`চৌকীদার`,
  `সমষ্টিরও`→`সমষ্টি`, `কয়েকফোটা` (left unchanged, was wrongly stripped),
  `সম্মতে`→`সম্মত`, `সমৰ্পয়েৎ` (left unchanged — likely OCR/mixed-script
  noise, not mangled further), `পরীক্ষাগারেও`→`পরীক্ষাগার`, `নিরুক্তে`→
  `নিরুক্ত`, `বিছিয়েছে`/`শর্তানুসারে` (left unchanged, no confident better
  target found). Each is the same recurring pattern this whole file
  documents — a rule-table regex coincidentally matches the end of a word
  that isn't actually root+that-suffix — but scattered across different
  stages (`sp_initial_dict`'s `তে` rule, `sp_final_dict`'s `ার`/`টা`/`টির`
  rules) with no single common cause, so a per-word override was the
  narrow, safe fix rather than another speculative rule change. **Does
  not generalize** to other inflected forms of the same roots (e.g.
  `চৌকীদারের` isn't covered just because `চৌকীদারকে` is) — documented as
  a known limitation in the override loader's own comment.
- Wired `data/bn_closed_class_words.csv` (the draft pronoun/postposition/
  conjunction/particle list, previously unused) into `stemmer.py`:
  `BanglaStemmer` now loads it at init and `_stem_one` returns any word in
  it completely unchanged, before any rule table runs. 64 of the 145
  words in that list were getting mis-stemmed before this (none of the
  rule tables know about closed-class function words — they're written
  for content words): `উপরে`/`উপর` → `র`, `থেকে` → `থেক`, `বিনা` → `না`,
  `দ্বারা` → `দ্বা`, etc. — full before-list in this session's history.
  This list is still a **draft awaiting your review/edit** per its own
  provenance; wiring it in doesn't require it to be finished, just
  correct so far, so it's worth re-running this check if you edit it.
- Added a bare present-tense `-ে` rule to `con_rep_dict` (`করে` → `কর`).
- Gated `sp_final_dict`'s `ে.ে` vowel-harmony rule behind a small explicit
  whitelist (`grammar.ee_harmony_roots = {হাস, নাচ}`) instead of firing on
  any word with that surface shape — fixes the `ছেলে` → `ছাল` false merge
  (and the same-class `দেখে`/`খেলে`/`ঠেলে` cases) while keeping `হেসে`/
  `নেচে` working. Real verb roots outside the whitelist (if any exist with
  this exact shape) will now be left unstemmed rather than false-merged —
  a deliberate precision-over-recall tradeoff given no lexicon exists to
  do better.
- Added `sp_final_dict['ির']` for the possessive on ই-final roots
  (`মালির` → `মালি`, matching the existing `মালি`/`মালিকে` merge).
- Fixed `sp_final_dict['ার']`'s long-root branch to preserve the root's
  own vowel instead of deleting it (`ঘটনার` → `ঘটনা`, `কলিজার` → `কলিজা`).
  This changed one baseline expectation (`কলিজার`'s gold stem was
  corrected from `কলিজ` to `কলিজা`, confirmed with the user).
- Removed `der_initial_dict`'s `অন` 2-character prefix entry entirely
  (rather than patching it): every word it actually fired on in practice
  produced a nonsense fragment (`অনটন`→`টন`, `অনড়`→`ড়`, etc.), and the two
  examples its own comment cited as "genuine" cases never actually
  exercised the rule (one was blocked by `invalid_word_start`, the other
  turns out to be caught by a `sp_final_dict` bug, see next bullet).
  Fixes the confirmed `অনমনীয়` → `মনীয়` bug (Dasgupta & Ng gold set);
  words like `অনমনীয়` are now left unchanged rather than wrongly merged —
  not the ideal `অ`+`নমনীয়` split, but adding bare `অ-` was already ruled
  out elsewhere in this file as too collision-prone without a lexicon.
- Fixed `sp_final_dict['া.ার']`'s long-root branch the same way as `ার`
  above, preserving the root's vowel-consonant-vowel shape instead of
  deleting the whole match (`ঠিকানার` → `ঠিকানা`, not `ঠিক`). Its
  two-wildcard cousin `া.া.ার` has a deeper, unresolved problem — logged
  as its own item above rather than fixed, since it needs a lexicon check
  to do correctly.
