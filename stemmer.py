from os.path import dirname, abspath
from typing import Dict, List
import re

import grammar

# d = dirname(dirname(abspath(__file__)))

class BanglaStemmer:

    first_dict: Dict[str,List[str]]
    second_dict: Dict[str,List[str]]
    third_dict: Dict[str,List[str]]
    fourth_dict: Dict[str,List[str]]
    fifth_dict: Dict[str,List[str]] # Swarnendu added
    sixth_dict: Dict[str,List[str]] # Swarnendu added

    def __init__(self):
        self.grammarParser()

    def grammarParser(self):
        self.first_dict = grammar.sp_initial_dict
        self.second_dict = grammar.con_rep_dict
        self.third_dict = grammar.obv_rep_dict
        self.fourth_dict = grammar.sp_final_dict
        self.fifth_dict = grammar.der_initial_dict # Swarnendu added
        self.sixth_dict = grammar.der_final_dict # Swarnendu added

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
            if result:
                initial_index = result.span()[0]
                final_index = result.span()[1]
                wordlen = len(word)
                if final_index == wordlen:
                    rigid_wordlen = self.checklen(grep[0:initial_index])
                    if rigid_wordlen > 1:
                        rplc = self.sixth_dict[rules][1]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    elif rigid_wordlen == 1:
                        rplc = self.sixth_dict[rules][0]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    else:
                        pass
                else:
                    pass
                break
            else:
                pass
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
        for rules in self.fifth_dict:
            result = re.match(rules, word)
            if result:
                final_index = result.span()[1]
                remainder = word[final_index:]
                if remainder and remainder[0] in self.invalid_word_start:
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
            if result:
                initial_index = result.span()[0]
                final_index = result.span()[1]
                wordlen = len(word)
                if final_index == wordlen:
                    rigid_wordlen = self.checklen(grep[0:initial_index])
                    if rigid_wordlen > 1:
                        rplc = self.fourth_dict[rules][1]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    elif rigid_wordlen == 1:
                        rplc = self.fourth_dict[rules][0]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    else:
                        pass
                else:
                    pass
                break
            else:
                pass
        grep = self.apply_sixth_rule(grep)
        return grep

    def apply_thrd_rule(self, word):
        grep = word
        for rules in self.third_dict:
            result = re.search(rules, word)
            if result:
                initial_index = result.span()[0]
                final_index = result.span()[1]
                
                wordlen = len(word)
                #print(wordlen)
                #print(final_index)
                if final_index == wordlen:
                    rigid_wordlen = self.checklen(grep[0:initial_index])
                    if rigid_wordlen > 1:
                        rplc = self.third_dict[rules][1]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    elif rigid_wordlen == 1:
                        rplc = self.third_dict[rules][0]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    else:
                        pass
                else:
                    pass
                break
            else:
                pass
        grep = self.apply_frth_rule(grep)
        return grep

    def apply_scnd_rule(self, word):
        grep = word
        for rules in self.second_dict:
            result = re.search(rules, word)
            if result:
                initial_index = result.span()[0]
                final_index = result.span()[1]
                wordlen = len(word)
                if final_index == wordlen:
                    rigid_wordlen = self.checklen(grep[0:initial_index])
                    if rigid_wordlen > 1:
                        rplc = self.second_dict[rules][1]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    elif rigid_wordlen == 1:
                        rplc = self.second_dict[rules][0]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    else:
                        pass
                else:
                    pass
                break
            else:
                pass
        grep = self.apply_thrd_rule(grep)
        return grep

    def apply_frst_rule(self, word):
        grep = word
        for rules in self.first_dict:
            result = re.search(rules, word)
            if result:
                initial_index = result.span()[0]
                final_index = result.span()[1]
                wordlen = len(word)
                if final_index == wordlen:
                    rigid_wordlen = self.checklen(grep[0:initial_index])
                    if rigid_wordlen > 1:
                        rplc = self.first_dict[rules][1]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    elif rigid_wordlen == 1:
                        rplc = self.first_dict[rules][0]
                        if '.' in rplc:
                            grep = self.dot_replace(word, initial_index, rplc)
                        else:
                            grep = self.dirrect_replace(word, initial_index, rplc)
                    else:
                        pass
                else:
                    pass
                break
            else:
                pass
        grep = self.apply_scnd_rule(grep)
        return grep

    def stem(self, wordarg):
        stemlist = []
        stemword = ''
        if isinstance(wordarg, list):
            for word in wordarg:
                stemlist.append(self.apply_frst_rule(word))
            return stemlist
        elif isinstance(wordarg, str):
            stemword = self.apply_frst_rule(wordarg)
            return stemword
        
