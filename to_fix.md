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

## No rule table covers the bare present-tense `-ে` verb ending

`করে` ("does/do", 3rd person present habitual) is left completely
unchanged by `stem()` — none of the six rule tables have an entry that
matches a bare `-ে` ending on its own (`con_rep_dict` only covers `-ে`
combined with progressive/perfect markers like `িয়ে`/`েয়ে`/`ায়ে`/`য়ে`, not
the plain present-tense form). This isn't a rule-ordering bug like the one
above; the rule simply doesn't exist.

This matters more than most gaps because `করে` is one of the highest-
frequency single tokens in the whole corpus (~153M occurrences,
2nd-ranked by raw frequency). It stays split off from the rest of its own
paradigm — `করা`/`করলাম`/`করব`/`করেছে`/`করছি` all correctly reduce to `কর`,
but `করে` doesn't join them.

Same gap likely affects the same present-tense form of every other verb
(e.g. `যায়`, `বলে`, `দেয়`), not just `কর`. Needs a new `con_rep_dict`
entry for bare `-ে` (with the usual short-root conservatism), which is a
grammar-table content change rather than a code fix — flagging for
review rather than adding unilaterally, since a bad regex here would
touch a very large number of words at once.

## `sp_final_dict`'s `ে.ে` vowel-harmony rule fires on unrelated nouns

`ছেলে` ("boy" — a very high-frequency, basic-vocabulary noun) reduces to
`ছাল`, which is a real but completely unrelated Bangla word ("bark/skin/
husk"), not a variant spelling or typo. Root cause: the `ে.ে` → `া.` rule
(`sp_final_dict`, comment references `হেসে নেচে গেয়ে`) exists to reverse a
vowel-harmony alternation specific to `-য়ে` conjunctive-participle verb
forms (root হাস + য়ে → হেসে). But the rule table stores it as a bare
literal/regex pattern with no way to require "this is actually a `-য়ে`
participle" — it matches *any* word with a consonant-ে-anything-ে shape,
which `ছেলে` satisfies purely by coincidence.

This is a false-merge risk, not just a wrong-looking output: if any
inflected form of the real word `ছাল` also appears in the corpus, it
would land on the same stem as `ছেলে` and its whole family, silently
merging two unrelated lemmas in `stem_freq`.

Likely fix: tighten the pattern to require the vowel harmony's actual
trigger (a preceding `য়`, i.e. something like `য়ে$` combined with the
vowel-flip logic) instead of matching the bare `ে.ে` shape — needs
linguistic review before changing, since getting the replacement logic
wrong here would touch every word fitting the shape, including the
correct verb-form cases it currently handles fine (e.g. `হেসে`, `নেচে`).

## `sp_final_dict`'s `ার` rule can eat a vowel-final root's own final vowel

`ঘটনার` ("of the event") reduces to `ঘটন`, not `ঘটনা`. The root `ঘটনা`
already ends in the vowel sign `া`; the possessive marker attached to it
is just `র`, but the `ার` rule (meant for consonant-final roots like
`কার`/`মার`/`যার`, per its comment) matches the literal 2-character
sequence `ার` regardless of whether the `া` belongs to the suffix or the
root, so it strips both `া` and `র` here — over-stripping the root's own
final letter.

Same "no lexicon, literal pattern only" failure class as the other items
here. Likely needs a lexicon/heuristic check for vowel-final roots before
applying `ার`, or a separate, narrower rule for bare `র` after a vowel.

## No rule covers the possessive `-ির` ending on ই-final roots

`মালির` ("gardener's", from `মালি` + `র`) is left unchanged — `sp_final_dict`
has `ার` (for আ-final roots) but nothing analogous for ই-final roots, so
`মালি`/`মালিকে` correctly merge with each other but `মালির` doesn't join
them. Same category as the `করে` gap above: missing rule, not a bug.

## `der_initial_dict`'s `অন` prefix rule over-fires on words taking the bare `অ-` negation prefix

`অনমনীয়` ("inflexible/unyielding") reduces to `মনীয়`, which is not a real
Bengali word — the correct segmentation, confirmed independently by the
Dasgupta & Ng (2007) academic gold set (see
`data/external_gold/dasgupta_ng_2007/`, found via `অ+নমনীয়` in that data),
is `অ` (negation prefix, "un-/in-") + `নমনীয়` ("flexible/malleable", a real
standalone root).

Root cause, traced through `apply_ffth_rule`: `der_initial_dict` has an
entry for the 2-character prefix `অন` (README: "without/dis-"), and
`re.match('অন', 'অনমনীয়')` succeeds because the word's first two
characters literally are `অ` + `ন`. The rule strips both characters and
returns the remainder (`মনীয়`) unconditionally, with no way to tell that
here the true morpheme boundary falls after just the first character —
this word actually takes the plain `অ-` prefix, and its root just happens
to start with `ন`. Compounding this, `অ-` alone isn't in `der_initial_dict`
at all, so there's no shorter/competing match that could win instead.

Same "no lexicon, literal pattern only" failure class as the `ে.ে` and
`ার` entries above: the rule can't distinguish a coincidental character
match from a real prefix boundary. Likely needs either (a) adding a bare
`অ-` rule and some way to prefer the correct one of `অ`/`অন` per-word
(a lexicon check, most plausibly — regex alone can't disambiguate this),
or (b) tightening `অন` to only fire in cases it's actually attested,
if that set turns out to be small and enumerable. Flagging for review
rather than changing unilaterally, per the usual rule for this file —
getting the fix wrong here would silently break the genuine `অন-` cases
(e.g. `অনিয়ম`, `অনাচার`) the rule was originally added for.

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
  (`বি`, `অন`, `উদ`), a bare vowel prefix is likely to coincide with a
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
  added at all, since the current architecture has no vowel-harmony
  machinery beyond the one hand-tuned `ে.ে` rule already flagged as buggy
  above: `-ik` (আঞ্চলিক ← অঞ্চল), `-o` (মেজো ← মধ্য), `-i` from `-o`
  adjectives (নীতি ← নীত), and the jɔphɔla/bɔphɔla abstract nouns
  (Ch.4 §4.3.iii).
- **Farsi/Arabic loan prefixes** (`বে-`, `দর-`, `না-`, `বদ-`, `গর-`,
  `আম-`, listed in the same chapter) weren't added — different register/
  etymology than the rest of `der_initial_dict`, and untested against
  loanword vocabulary.
