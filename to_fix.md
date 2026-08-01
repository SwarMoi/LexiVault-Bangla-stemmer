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
