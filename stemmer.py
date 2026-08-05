from os.path import dirname, abspath, join
from typing import Dict, List
import csv
import re

import grammar

_REPO_ROOT = dirname(abspath(__file__))

class BanglaStemmer:

    first_dict: Dict[str,List[str]]
    second_dict: Dict[str,List[str]]
    third_dict: Dict[str,List[str]]
    fourth_dict: Dict[str,List[str]]
    fifth_dict: Dict[str,List[str]] # Swarnendu added
    sixth_dict: Dict[str,List[str]] # Swarnendu added

    def __init__(self):
        self.grammarParser()
        self.closed_class_words = self._load_closed_class_words()
        self.word_stem_overrides = self._load_word_stem_overrides()

    def _load_word_stem_overrides(self):
        # Individually-confirmed word -> correct-stem exceptions
        # (data/word_stem_overrides.csv), found via cross-checking against
        # Morphemo (an independent statistical segmenter, see
        # src/morphemo_audit.py in the main bangla-lexical-corpus repo) and
        # manually verified. Each is a case where a rule-table pattern
        # coincidentally matches the end of a word that isn't actually
        # root+that-suffix (e.g. চৌকীদারকে: the 'ার' rule strips the
        # Persian agentive suffix -দার as if '-ার' were case marker + the
        # root's own vowel). Checked against the word's ORIGINAL surface
        # form only, same as closed_class_words -- this does NOT generalize
        # to other inflected forms of the same root (e.g. চৌকীদারের isn't
        # covered just because চৌকীদারকে is); it's a narrow, evidence-based
        # patch for these specific confirmed cases, not a new rule.
        path = join(_REPO_ROOT, 'data', 'word_stem_overrides.csv')
        with open(path, encoding='utf-8') as f:
            return {row['Word']: row['Stem'] for row in csv.DictReader(f)}

    def _load_closed_class_words(self):
        # Pronouns/postpositions/conjunctions/particles (draft list,
        # data/bn_closed_class_words.csv) that stem() must leave untouched
        # entirely: 64 of the 145 words in this list currently get
        # mis-stemmed by the rule tables below if not special-cased (e.g.
        # উপরে/উপর -> র, থেকে -> থেক, বিনা -> না), since none of those
        # tables know about closed-class function words -- they're written
        # for content words. Checked against the word's ORIGINAL surface
        # form only (see stem()); this list is a draft awaiting the
        # project owner's review, per the data file's own provenance notes.
        path = join(_REPO_ROOT, 'data', 'bn_closed_class_words.csv')
        with open(path, encoding='utf-8') as f:
            return frozenset(row['Word'] for row in csv.DictReader(f))

    def grammarParser(self):
        self.first_dict = grammar.sp_initial_dict
        self.second_dict = grammar.con_rep_dict
        self.third_dict = grammar.obv_rep_dict
        self.fourth_dict = grammar.sp_final_dict
        self.fifth_dict = grammar.der_initial_dict # Swarnendu added
        self.sixth_dict = grammar.der_final_dict # Swarnendu added
        # sp_initial_dict entries that are safe to try a SECOND time, after
        # an emphatic particle (ই/ও) has already been stripped from the
        # same word -- see _stem_one. Restricted to bare case/classifier
        # markers (তো/কে/তে) that genuinely stack after an emphatic in
        # normal Bangla morphology (মালিতে+ও, মিঠু+কে+ও). ই and ও
        # themselves are excluded (a word can't take the same emphatic
        # twice); রা (plural) is also excluded even though it's a real
        # sp_initial_dict key -- empirically, re-trying it on an
        # already-once-reduced word over-fires on proper nouns/loanwords
        # that coincidentally end in রা (গ্যালাতাসারা "Galatasaray" ->
        # wrongly to গ্যালাতাসা), since প্লুরাল-রা is normally the
        # FIRST suffix layer after the root, not something exposed by
        # stripping a later emphatic.
        self.first_dict_repeat = {k: v for k, v in self.first_dict.items() if k in ('তো', 'কে', 'তে')}

    def checklen(self, word):
        skip_wrd = ['া', 'ি', 'ী', 'ু', 'ূ', 'ৃ', 'ে', 'ৈ', 'ো', 'ৌ']
        len = 0
        for ltr in word:
            if ltr in skip_wrd:
                pass
            else:
                len += 1
        return len

    def dot_replace(self, word, initial_index, rplc):
        wrd = word[0:initial_index]
        for i in range(len(rplc)):
            if rplc[i] == '.':
                wrd += word[initial_index + i]
            else:
                wrd += rplc[i]
        return wrd

    def dirrect_replace(self, word, initial_index, rplc):
        wrd = word[0:initial_index]
        wrd += rplc
        return wrd
    
    ## Swarnendu Added --------------------------------
    def apply_sixth_rule(self, word):
        # der_final_dict: derivational suffixes (বান, মান, শীল, ...) -- same
        # end-anchored matching as the inflectional-suffix rules above.
        grep = word
        for rules in self.sixth_dict:
            result = re.search(rules, word)
            if not result:
                continue
            initial_index = result.span()[0]
            final_index = result.span()[1]
            wordlen = len(word)
            if final_index != wordlen:
                # matched somewhere mid-word, not as a real suffix here --
                # keep scanning instead of giving up on this whole stage.
                continue
            rigid_wordlen = self.checklen(grep[0:initial_index])
            if rigid_wordlen > 1:
                rplc = self.sixth_dict[rules][1]
                if '.' in rplc:
                    grep = self.dot_replace(word, initial_index, rplc)
                else:
                    grep = self.dirrect_replace(word, initial_index, rplc)
                break
            elif rigid_wordlen == 1:
                rplc = self.sixth_dict[rules][0]
                if '.' in rplc:
                    grep = self.dot_replace(word, initial_index, rplc)
                else:
                    grep = self.dirrect_replace(word, initial_index, rplc)
                break
        grep = self.apply_ffth_rule(grep)
        return grep

    # Dependent vowel signs, virama/hasant, and the other combining marks
    # can only ever attach after a consonant -- a Bangla word can never
    # start with one of these. Used to reject prefix matches that would
    # split a conjunct consonant cluster in two (e.g. matching the literal
    # prefix 'অন' inside 'অন্তর্লোক' at the অ-ন-্ conjunct boundary would
    # leave '্তর্লোক', starting with a bare hasant).
    invalid_word_start = set('ািীুূৃেৈোৌ্ঁংঃ')

    def apply_ffth_rule(self, word):
        # der_initial_dict: derivational prefixes (দুর্, বি, অনু, ...). These
        # attach to the front of the word, so -- unlike every other rule
        # table here -- a match has to be anchored at index 0, and what
        # survives stripping is the *tail* (word[final_index:]), not the
        # head. checklen()-based conservatism (used by every suffix rule to
        # avoid over-stripping short roots) doesn't transfer here: prefixed
        # roots are often short by checklen's count while still being
        # complete words (e.g. দুরা+আশা -> দুরাশা, remainder আশা has
        # checklen 1 but is a valid root), so this rule always applies the
        # index[1] replacement. None of the current replacement strings
        # contain '.', so no dot_replace-style vowel preservation is needed.
        grep = word
        if word.startswith(grammar.protected_prefix_roots):
            # Confirmed monomorphemic/lexicalized word (see
            # grammar.protected_prefix_roots) -- don't let any prefix rule
            # touch it at all, rather than trying to guess which specific
            # rule would have false-fired.
            return grep
        for rules in self.fifth_dict:
            result = re.match(rules, word)
            if result:
                final_index = result.span()[1]
                remainder = word[final_index:]
                if not remainder:
                    # the whole word is the affix itself (e.g. word == 'বি')
                    # -- stripping it would leave an empty stem.
                    continue
                if remainder[0] in self.invalid_word_start:
                    continue
                rplc = self.fifth_dict[rules][1]
                grep = rplc + remainder
                break
            else:
                pass
        return grep
    ## Swarnendu Added --------------------------------|
    def apply_frth_rule(self, word):
        grep = word
        for rules in self.fourth_dict:
            result = re.search(rules, word)
            if not result:
                continue
            initial_index = result.span()[0]
            final_index = result.span()[1]
            wordlen = len(word)
            if final_index != wordlen:
                continue
            rigid_wordlen = self.checklen(grep[0:initial_index])
            if rigid_wordlen > 1:
                rplc = self.fourth_dict[rules][1]
                if '.' in rplc:
                    grep = self.dot_replace(word, initial_index, rplc)
                else:
                    grep = self.dirrect_replace(word, initial_index, rplc)
                break
            elif rigid_wordlen == 1:
                rplc = self.fourth_dict[rules][0]
                if '.' in rplc:
                    candidate = self.dot_replace(word, initial_index, rplc)
                else:
                    candidate = self.dirrect_replace(word, initial_index, rplc)
                if rules in grammar.ee_harmony_rule_keys and candidate not in grammar.ee_harmony_roots:
                    # Cons-e-Cons-e shape matched, but not one of the
                    # attested vowel-harmony roots -- likely a coincidental
                    # match (ছেলে, দেখে), not a real alternation. Skip this
                    # key rather than risk a false merge; see grammar.py's
                    # ee_harmony_roots comment and to_fix.md.
                    continue
                grep = candidate
                break
        grep = self.apply_sixth_rule(grep)
        return grep

    def apply_thrd_rule(self, word):
        grep = word
        for rules in self.third_dict:
            result = re.search(rules, word)
            if not result:
                continue
            initial_index = result.span()[0]
            final_index = result.span()[1]
            wordlen = len(word)
            if final_index != wordlen:
                continue
            rigid_wordlen = self.checklen(grep[0:initial_index])
            if rigid_wordlen > 1:
                rplc = self.third_dict[rules][1]
                if '.' in rplc:
                    grep = self.dot_replace(word, initial_index, rplc)
                else:
                    grep = self.dirrect_replace(word, initial_index, rplc)
                break
            elif rigid_wordlen == 1:
                rplc = self.third_dict[rules][0]
                if '.' in rplc:
                    grep = self.dot_replace(word, initial_index, rplc)
                else:
                    grep = self.dirrect_replace(word, initial_index, rplc)
                break
        grep = self.apply_frth_rule(grep)
        return grep

    def apply_scnd_rule(self, word):
        grep = word
        for rules in self.second_dict:
            result = re.search(rules, word)
            if not result:
                continue
            initial_index = result.span()[0]
            final_index = result.span()[1]
            wordlen = len(word)
            if final_index != wordlen:
                continue
            rigid_wordlen = self.checklen(grep[0:initial_index])
            if rigid_wordlen > 1:
                rplc = self.second_dict[rules][1]
                if '.' in rplc:
                    grep = self.dot_replace(word, initial_index, rplc)
                else:
                    grep = self.dirrect_replace(word, initial_index, rplc)
                break
            elif rigid_wordlen == 1:
                rplc = self.second_dict[rules][0]
                if '.' in rplc:
                    grep = self.dot_replace(word, initial_index, rplc)
                else:
                    grep = self.dirrect_replace(word, initial_index, rplc)
                break
        grep = self.apply_thrd_rule(grep)
        return grep

    def apply_frst_rule(self, word, repeat=False):
        grep = word
        fired = False
        first_dict = self.first_dict_repeat if repeat else self.first_dict
        for rules in first_dict:
            result = re.search(rules, word)
            if not result:
                continue
            initial_index = result.span()[0]
            final_index = result.span()[1]
            wordlen = len(word)
            if final_index != wordlen:
                continue
            rigid_wordlen = self.checklen(grep[0:initial_index])
            if rigid_wordlen > 1:
                rplc = first_dict[rules][1]
                if '.' in rplc:
                    grep = self.dot_replace(word, initial_index, rplc)
                else:
                    grep = self.dirrect_replace(word, initial_index, rplc)
                fired = True
                break
            elif rigid_wordlen == 1:
                rplc = first_dict[rules][0]
                if '.' in rplc:
                    grep = self.dot_replace(word, initial_index, rplc)
                else:
                    grep = self.dirrect_replace(word, initial_index, rplc)
                fired = True
                break
        return grep, fired

    # sp_initial_dict strips at most one case/emphatic marker, then hands
    # off to the rest of the (otherwise unchanged, single-pass) chain --
    # it never gets a second look at a word it's already touched. So a
    # word with two stacked sp_initial_dict markers only gets one peeled:
    # মালিতেও -> মালিতে, where the locative তে exposed by stripping the
    # emphatic ও belongs to the same table that just ran and doesn't run
    # again. Loop *only* this one stage to a fixpoint (see
    # first_dict_repeat above for why it's narrowed on repeat passes),
    # then run the rest of the chain -- con_rep/obv_rep/sp_final/
    # der_final/der_initial -- exactly once, unchanged from the original,
    # 94-word-baseline-validated architecture. A broader loop (every stage
    # re-tried, tried and reverted) empirically over-fired on proper nouns
    # and loanwords that coincidentally match a rule's ending on their
    # SECOND pass nearly as often as it fixed genuine stacking.
    MAX_FIRST_STAGE_PASSES = 5

    def _stem_one(self, word):
        if word in self.word_stem_overrides:
            return self.word_stem_overrides[word]
        if word in self.closed_class_words:
            return word
        current, fired = self.apply_frst_rule(word, repeat=False)
        for _ in range(self.MAX_FIRST_STAGE_PASSES - 1):
            if not fired:
                break
            current, fired = self.apply_frst_rule(current, repeat=True)
        return self.apply_scnd_rule(current)

    def stem(self, wordarg):
        if isinstance(wordarg, list):
            return [self._stem_one(word) for word in wordarg]
        elif isinstance(wordarg, str):
            return self._stem_one(wordarg)
        
