# Known issues

## Each rule stage fires at most once per word (no stacked-suffix peeling)

`stem()` runs a fixed chain of six stages
(`apply_frst_rule → apply_scnd_rule → apply_thrd_rule → apply_frth_rule →
apply_sixth_rule → apply_ffth_rule`, see `stemmer.py`), and each stage
tries its rule table once, applies at most one match, and hands off to the
next stage. It never loops back to re-check an earlier table against the
new, shorter word.

This means a word with two stacked suffixes from the *same* dictionary
only gets one of them stripped. Example from the corpus sample
(`output/corpus_sample_validated.csv`):

- `মালিতেও` → `মালিতে` (only the emphatic `ও` is stripped; the locative
  `তে` that becomes exposed afterward belongs to `sp_initial_dict`, the
  same table that already fired earlier in the chain for this word, so it
  never gets a second look). Ideal stem: `মালি`.

Fix would mean either looping each stage to a fixpoint (repeat until no
rule matches) or restructuring the chain to revisit earlier tables after a
later one strips something — needs some care to avoid infinite loops or
over-stripping on repeated application.

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

## `sp_final_dict`'s `া.ার` rule can over-strip too, same failure class as the now-fixed `ার` rule

Found while testing the `অন` prefix fix below: `অনাচার` ("misconduct")
reduces to `অন`, not left unchanged or correctly split. Root cause: before
reaching the prefix stage at all, `sp_final_dict`'s `া.ার` rule (meant for
patterns like `কামার`/`জানার`) matches the word's trailing `াচার` and,
since `checklen('অন') > 1`, strips it entirely rather than preserving the
root's own vowel — the exact same class of bug the plain `ার` rule had
(now fixed, see the session that resolved items below) but not yet applied
to this related pattern (`া.ার`, and its cousin `া.া.ার`). Needs the same
treatment: change the `rigid_wordlen > 1` branch's replacement to preserve
the vowel sign instead of deleting it, then re-verify against the 94-word
baseline and external gold sets, since these patterns are rarer and less
tested than plain `ার` was.

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

---

**Resolved this session** (verified against the 94 `Correct=1` rows in
`output/output_validated.csv`, 0 regressions each time):

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
  turns out to be caught by the `া.ার` bug logged above). Fixes the
  confirmed `অনমনীয়` → `মনীয়` bug (Dasgupta & Ng gold set); words like
  `অনমনীয়` are now left unchanged rather than wrongly merged — not the
  ideal `অ`+`নমনীয়` split, but adding bare `অ-` was already ruled out
  elsewhere in this file as too collision-prone without a lexicon.
