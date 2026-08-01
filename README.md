# LexiVault-Bangla-stemmer

Augmented version of the [bangla-stemmer](https://pypi.org/project/bangla-stemmer/) PyPI package (v1.0, 2020).

## What's new here vs. the PyPI package

The original package only strips **inflectional** morphology (case markers,
plurals, verb conjugation endings) through four rule stages:
`sp_initial_dict → con_rep_dict → obv_rep_dict → sp_final_dict`.

This fork adds **derivational** morphology on top of that pipeline:

- **`der_final_dict`** — derivational suffixes: `-বান`, `-মান`, `-শীল`, `-য়ি`, `-ন্ত`,
  `-ওয়ালা`, `-জনক`, `-কর`, `-গত`, `-উক`, `-সই`, `-ইত`
  (e.g. "possessing", "-ing", "prone to", "person who does").
- **`der_initial_dict`** — derivational prefixes: `দুর্-`, `বি-`, `অনু-`, `অধি-`,
  `উদ-`, `অন-`, `অত্যা-`, `প্রতি-`, `অপ-`, `অব-`, `অভি-`, `অতি-`, `উপ-`, `নির্-`,
  `পরা-`, `পরি-`, `সং-`, `সম-`, etc. (e.g. "bad/mis-", "without/dis-",
  "sub-/after-"). The full standard Sanskrit/Bangla prefix and suffix
  inventory cross-referenced against Thompson, *Bengali* (2012), ch. 4
  "Word formation" — some attested prefixes/suffixes from that chapter were
  deliberately left out after causing false positives against the validated
  test set (`প্র-`, `-তা`) or being judged too collision-prone to add without
  a lexicon (bare `আ-`, `নি-`, `সু-`, `-আমি`); see `to_fix.md`.

Both are wired into the pipeline as two extra stages run after the original
four: `sp_final_dict → der_final_dict (suffix) → der_initial_dict (prefix)`.
So a word like `দুর্ঘটনা` (prefix `দুর্-` + `ঘটনা`) or `দুরাশা` (prefix `দুরা-` +
`আশা`) now reduces past its inflectional ending down to the derivational
root, instead of stopping at the inflectional layer.

The prefix stage needed different matching logic from every other stage:
inflectional/derivational suffix rules match at the *end* of the word and
keep the head; the prefix rule matches at the *start* and keeps the tail.
It also skips the length-based "don't strip if the root would be too short"
conservatism the suffix rules use, since that check under-counts short-but-
valid roots on the prefix side (verified against
[`output/output_validated.csv`](output/output_validated.csv), a 124-word
human-validated set — the stemmer now reproduces every entry in it exactly).

Also cleaned up from the original: removed leftover debug `print()` calls
in every rule stage, a duplicate dictionary key, and dead/commented-out
experimental code.

## Known limitations

- Not currently packaged for `pip install` — `stemmer.py` and `grammar.py`
  are flat files at the repo root with a bare `import grammar`, so using
  this from another project currently means adding this directory to
  `sys.path` rather than a normal package import.
- Rule-based, no lexicon: affix patterns can false-positive on words that
  merely start/end with the same letters as an affix (e.g. `বিদ্যালয়`
  "school" isn't `বি-` + a root, but matches the `বি-` prefix rule anyway).
