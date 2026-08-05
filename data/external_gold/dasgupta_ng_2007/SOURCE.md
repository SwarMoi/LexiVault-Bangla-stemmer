# Dasgupta & Ng (2007) Bengali morphological segmentation gold set

**Citation**: Sajib Dasgupta and Vincent Ng, "Unsupervised morphological parsing of
Bengali," *Language Resources and Evaluation* 41 (2007), Springer.
DOI: [10.1007/s10579-007-9031-y](https://doi.org/10.1007/s10579-007-9031-y).
Companion conference paper: Dasgupta & Ng, "Unsupervised Word Segmentation for
Bangla," ICON 2007.

**Original distribution site** (dead as of 2026-08-01, redirects to a generic UT
Dallas helpdesk portal): `https://personal.utdallas.edu/~sajib/dataset.html`.
Recovered via the Wayback Machine snapshot from 2021-12-01:
`http://web.archive.org/web/20211201061226/https://www.hlt.utdallas.edu/~sajib/dataset.html`.

**License**: none stated on the distribution page or in the paper. The paper
explicitly frames the dataset as "a valuable addition to the list of resources
publicly available for Bengali language processing" (Sect. 1), but there is no
formal license grant — treat as an academic research resource, not a
redistribution-cleared one, until/unless the authors say otherwise.

## What's in this directory

- `dataset_bengali.txt` — the 4,110 word→segmentation pairs in actual Unicode
  Bangla script (converted from the source UTF-16LE encoding to UTF-8). One pair
  per line: `word<TAB>segmentation[, alt_segmentation]`, where `+` marks a
  morpheme boundary within the segmentation. Some lines carry more than one
  comma-separated segmentation (kept as-is from the source; not yet clear whether
  these are alternate valid parses or an artifact — needs a look before use).
- `dataset_transliterated.txt` — the same 4,110 pairs in the authors' own ASCII
  Roman transliteration scheme (kept for cross-checking `dataset_bengali.txt`,
  since it's a completely independent encoding of the same data).
- `transliteration_mapping.txt` — the authors' Bangla-Unicode-codepoint →
  ASCII-transliteration table (62 entries), in case `dataset_transliterated.txt`
  ever needs to be decoded independently.
- `dasgupta_ng_2007_paper.pdf` — the LRE journal paper itself, fetched from the
  author's personal page (`https://personal.utdallas.edu/~vince/papers/lre06.pdf`).

## Caveats for using this as a stemmer eval set

- This is **full morphological segmentation** (prefix + root + suffix + suffix
  ...), not a flat word→stem pair like our own `output/output_validated.csv` or
  `output/corpus_sample_validated.csv`. There is no explicit root/POS label per
  morpheme — for a simple word like `আছে → আছ+ে` the first chunk is the root, but
  for words with a real derivational prefix the root is a *later* chunk. Turning
  this into a `word,gold_root` comparison requires a heuristic (e.g. checking the
  first chunk against a known prefix list) that itself embeds a judgment call —
  don't invent one silently; check with the user first, the same way stemmer rule
  changes in `to_fix.md` are gated on their sign-off.
- Uses the *authors'* romanization/rules, not ours — words are drawn from one
  year of *Prothom Alo* news articles (2006-era), skewed toward third-person verb
  forms and sports/editorial vocabulary (see Sect. 8.1 of the paper), so don't
  expect it to be representative of our own corpus's domain mix.
- The paper's own example set overlaps directly with issues already logged in
  this repo's `to_fix.md`: their Table 3 flags `করে` (`kre`) as *more* frequent
  than its root `কর` (`kr`) — this is the same bare present-tense `-ে` verb gap
  noted in `to_fix.md`'s second item, now with independent academic confirmation
  that it's a real, expected pattern in Bengali verb morphology, not a corpus-
  sampling fluke.
