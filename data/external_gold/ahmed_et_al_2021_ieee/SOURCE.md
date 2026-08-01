# Ahmed, Hossain, Salim, Anjum & Hasan (2021), "Gold Dataset for the Evaluation of Bangla Stemmer"

**Citation**: T. Ahmed, S. Hossain, Md. S. Salim, A. Anjum, K. M. Azharul Hasan,
"Gold Dataset for the Evaluation of Bangla Stemmer," 2021 5th International
Conference on Electrical Information and Communication Technology (EICT),
Khulna, Bangladesh. DOI: [10.1109/EICT54103.2021.9733662](https://doi.org/10.1109/EICT54103.2021.9733662).
Authors: Khulna University of Engineering & Technology (KUET), Bangladesh.

**Obtained**: full text via IEEE Xplore institutional access (Queen Mary
University of London), 2026-08-01 — not otherwise freely available (no open
PDF found on Semantic Scholar, Google Scholar, ResearchGate, or the authors'
publication list page).

**License**: none stated; standard IEEE copyright applies to the paper PDF
itself. The paper's reference [11] points to a public GitHub repo
(`github.com/Tanim-Ahmed/performance_evaluation_dataset`) which **no longer
exists** (404). The nearest surviving repo on the same author's account,
`github.com/Tanim-Ahmed/Bangla_Stemming_Rules`, has no license file either —
same "treat as research reference, not redistribution-cleared" caveat as the
Dasgupta & Ng data in the sibling directory.

## What's actually here — and why this is a weaker resource than Dasgupta & Ng

Unlike Dasgupta & Ng (2007), **this is not a clean word→root list**. What the
paper actually contains/references:

- `ahmed_et_al_2021_paper.pdf` — the full paper. Section IV ("Rule Based
  Corpus Generation") lists roughly 150 suffix-stripping rules, each
  illustrated with one Bangla example *sentence* rather than an isolated
  word — e.g. rule `িট- → ϵ, ে◌ → ϵ` illustrated by input sentence
  `েস কাজিট কের` → output `েস কাজ কর`. Turning this into `word,gold_root`
  pairs comparable to our own CSVs would require manually identifying which
  word in each example sentence the rule targets and what it reduces to —
  doable, but real per-example parsing work, not a mechanical conversion
  like the Dasgupta & Ng `+`-delimited segmentation was.
- `github_suffix_list.txt` — 287 bare suffix strings (no roots, no examples,
  no rule→replacement mapping) fetched from `Bangla_Stemming_Rules`, the
  closest surviving repo to the paper's dead reference [11] link. Useful only
  as a checklist to cross-reference against our own `grammar.py` suffix
  tables for coverage gaps, not as evaluable gold data.
- The paper's actual evaluation corpus used for its Table I results (316
  sentences, 1086 words, 308 candidate inflected words) is **not published
  anywhere** — the paper only reports aggregate right/wrong-stemmed counts
  for three stemmers (their own, plus two GitHub baselines: `rafi-kamal/
  Bangla-Stemmer`, `sazid1462/py-bangla-stemmer`), not the underlying data.

**Bottom line**: this paper is real and the corpus it describes is real, but
what's actually publicly retrievable is a suffix rule list plus prose
examples, not a ready-to-run gold set.

## Update: transcribed and compared anyway (2026-08-01)

Confirmed the PDF's text layer uses a non-Unicode-compliant embedded font —
naive text extraction (and this would equally affect scraping IEEE's
abstract page, which has no full-text HTML for conference papers anyway;
checked, only a PDF download exists) produces corrupted, reordered Bangla
glyphs (e.g. "িবিধ" instead of "বিধি"). Visually reading the rendered PDF
pages (zoomed screenshots) gives correct text. All 215 rule+example lines
from Section IV were hand-transcribed this way into `rule_examples.tsv`
(`suffix<TAB>example_sentence`, one row per rule; many sentences repeat
across rows since one sentence can illustrate several rules at once).

`evaluate_ahmed_et_al.py` (repo root) turns this into a comparison: for each
row, it looks for exactly one word in the sentence ending with the rule's
suffix; if found, gold stem = that word minus the suffix (every rule in this
paper replaces with the empty string, no vowel-harmony or other
replacement logic). Ambiguous rows (zero or multiple matching words) are
flagged rather than guessed — 41 of 215. Result on the other 174:
**33.3% exact match (58/174)**, in the same range as the Dasgupta & Ng
result.

**Caveat when reading these mismatches**: this paper's own "gold" standard
is shallower than either Dasgupta & Ng's or our stemmer's — it's a single
flat suffix strip with no iteration, so e.g. rule `ছে` on `উঠেছে` ("has
risen/stood up") gives their gold `উঠে`, not the true root `উঠ` our
stemmer reaches (via its own multi-stage chain). A mismatch here sometimes
means our stemmer is doing *more* correctly than this dataset expects, not
less — read disagreements in `output/external_gold_ahmed_et_al_comparison.csv`
with that in mind, unlike the Dasgupta & Ng comparison where mismatches are
more consistently gaps.
