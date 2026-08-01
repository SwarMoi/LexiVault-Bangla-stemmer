"""Compare LexiVault-Bangla-stemmer's stem() output against the Dasgupta & Ng
(2007) gold morphological segmentation set (see data/external_gold/dasgupta_ng_2007/SOURCE.md).

The gold data marks full prefix+root+suffix segmentation, not a single "root"
label, so this uses a first-pass heuristic to pick out the root chunk:
first segment is the root, unless it exactly matches one of our own known
derivational prefixes (grammar.der_initial_dict), in which case the second
segment is taken as the root instead. Multi-root / multi-suffix words beyond
that are not handled specially -- flagged for manual review via the CSV.
"""
import csv
from pathlib import Path

from grammar import der_initial_dict
from stemmer import BanglaStemmer

REPO_ROOT = Path(__file__).parent
GOLD_FILE = REPO_ROOT / "data/external_gold/dasgupta_ng_2007/dataset_bengali.txt"
OUT_FILE = REPO_ROOT / "output/external_gold_dasgupta_ng_comparison.csv"

KNOWN_PREFIXES = set(der_initial_dict.keys())


def gold_root(segmentation: str) -> str:
    first_variant = segmentation.split(",")[0].strip()
    chunks = first_variant.split("+")
    if len(chunks) > 1 and chunks[0] in KNOWN_PREFIXES:
        return chunks[1]
    return chunks[0]


def main():
    stemmer = BanglaStemmer()
    rows = []
    with GOLD_FILE.open(encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            word, _, segmentation = line.partition(" ")
            root = gold_root(segmentation)
            stemmed = stemmer.stem(word)
            rows.append({
                "word": word,
                "gold_segmentation": segmentation,
                "gold_root_heuristic": root,
                "stemmer_output": stemmed,
                "exact_match": stemmed == root,
            })

    OUT_FILE.parent.mkdir(exist_ok=True)
    with OUT_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    matches = sum(r["exact_match"] for r in rows)
    prefixed = sum(1 for r in rows if r["gold_segmentation"].split(",")[0].strip().split("+")[0] in KNOWN_PREFIXES)

    print(f"Total gold words: {total}")
    print(f"Exact root match: {matches} ({matches / total:.1%})")
    print(f"Words where a known prefix chunk was detected (heuristic engaged): {prefixed}")
    print(f"Wrote comparison rows to {OUT_FILE}")


if __name__ == "__main__":
    main()
