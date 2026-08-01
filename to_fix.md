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
