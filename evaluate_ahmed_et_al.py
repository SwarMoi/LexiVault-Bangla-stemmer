"""Compare LexiVault-Bangla-stemmer's stem() output against the Ahmed et al.
(2021) IEEE gold-dataset paper's rule+example corpus (see
data/external_gold/ahmed_et_al_2021_ieee/SOURCE.md).

Unlike the Dasgupta & Ng comparison, this source gives no per-word gold
segmentation -- it gives a suffix-stripping rule (always replacement=empty
string in this paper) plus one illustrative Bangla sentence per rule,
transcribed by hand from the paper's rendered PDF pages into
rule_examples.tsv (suffix<TAB>sentence). This script has to first figure out
*which word* in the sentence the rule actually targets before it can compare
anything.

Heuristic: tokenize the sentence, strip trailing punctuation, and look for
exactly one token ending with the rule's suffix. If zero or more than one
token match, the example is ambiguous and gets flagged rather than guessed
at -- same "don't silently resolve linguistic judgment calls" rule as
evaluate_dasgupta_ng.py's prefix heuristic.
"""
import csv
import re
from pathlib import Path

from stemmer import BanglaStemmer

REPO_ROOT = Path(__file__).parent
RULES_FILE = REPO_ROOT / "data/external_gold/ahmed_et_al_2021_ieee/rule_examples.tsv"
OUT_FILE = REPO_ROOT / "output/external_gold_ahmed_et_al_comparison.csv"

PUNCTUATION = "।,.?!ঃ\"'():;"


def clean_token(tok: str) -> str:
    return tok.strip(PUNCTUATION)


def find_target_word(suffix: str, sentence: str):
    tokens = [clean_token(t) for t in sentence.split()]
    candidates = [t for t in tokens if t.endswith(suffix) and len(t) > len(suffix)]
    if len(candidates) == 1:
        return candidates[0]
    return None


def main():
    stemmer = BanglaStemmer()
    rows = []
    ambiguous = 0
    with RULES_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            suffix, _, sentence = line.partition("\t")
            target = find_target_word(suffix, sentence)
            if target is None:
                ambiguous += 1
                rows.append({
                    "suffix_rule": suffix,
                    "sentence": sentence,
                    "target_word": "",
                    "gold_root_heuristic": "",
                    "stemmer_output": "",
                    "exact_match": "",
                    "status": "ambiguous_or_no_match",
                })
                continue
            gold_root = target[: -len(suffix)]
            stemmed = stemmer.stem(target)
            rows.append({
                "suffix_rule": suffix,
                "sentence": sentence,
                "target_word": target,
                "gold_root_heuristic": gold_root,
                "stemmer_output": stemmed,
                "exact_match": stemmed == gold_root,
                "status": "ok",
            })

    OUT_FILE.parent.mkdir(exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    scored = [r for r in rows if r["status"] == "ok"]
    matches = sum(1 for r in scored if r["exact_match"])

    print(f"Total rule+example lines: {len(rows)}")
    print(f"Ambiguous / no unique target word found: {ambiguous}")
    print(f"Scored: {len(scored)}")
    if scored:
        print(f"Exact root match: {matches} ({matches / len(scored):.1%})")
    print(f"Wrote comparison rows to {OUT_FILE}")


if __name__ == "__main__":
    main()
