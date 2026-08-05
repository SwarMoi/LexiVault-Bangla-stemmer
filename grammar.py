
#-------------- Rules for obvious replecement of inflection --------------#
obv_rep_dict = {
    'েরগুলির':['ের', ''],
    'েরগুলিকে':['ের', ''],
    'েরগুলি':['ের', ''],
    'গুলিকে':['ই', ''],
    'গুলির':['ই', ''],
    'গুলি':['ই', ''],
    #---------------#
    'েরগুলীর':['ের', ''],
    'েরগুলীকে':['ের', ''],
    'েরগুলী':['ের', ''],
    'গুলীকে':['ই', ''],
    'গুলীর':['ই', ''],
    'গুলী':['ই', ''],
    #--------------#
    'েরটার':['ের', ''],
    'েরটা':['ের', ''],
    'েরগুলোকে':['ের', ''],
    'েরগুলোর':['ের', ''],
    'েরগুলো':['ের', ''],
    'গুলোকে':['ই', ''],
    'গুলোর':['ই', ''],
    'গুলো':['ই', '']
}

#-------------- Rules for contradictory replacement of inflection -------------#

con_rep_dict = {
    #---------------#
    'াচ্ছেন':['ায়', ''],
    'াচ্ছে':['ায়', ''],
    'াচ্ছ':['ায়', ''],
    'াচ্ছিলাম':['ায়', ''],
    'াচ্ছিলা':['ায়', ''],
    'াচ্ছিলেন':['ায়', ''],
    'াচ্ছিলে':['ায়', ''],
    'াচ্ছিল':['ায়', ''],
    'াচ্ছিস':['ায়', ''],
    'াচ্ছি':['ায়', ''],
    #---------------#
    'িচ্ছেন':['েয়', ''],
    'িচ্ছে':['েয়', ''],
    'িচ্ছ':['েয়', ''],
    'িচ্ছিলাম':['েয়', ''],
    'িচ্ছিলা':['েয়', ''],
    'িচ্ছিলেন':['েয়', ''],
    'িচ্ছিলে':['েয়', ''],
    'িচ্ছিল':['েয়', ''],
    'িচ্ছিস':['েয়', ''],
    'িচ্ছি':['েয়', ''],
    #---------------#
    'েয়েছে':['ায়', ''],
    'িয়েছে':['িয়', ''],
    'য়েছে':['য়', ''],
    'ে.েছে':['া.', ''],
    'েছে':['েছ', ''],
    'ছে':['ছ', ''],
    #---------------#
    'েয়েছ':['ায়', ''],
    'িয়েছ':['িয়', ''],
    'য়েছ':['য়', ''],
    'ে.েছ':['া.', ''],
    'েছ':['েছ', ''],
    'ছ':['ছ', ''],
    #----------------#
    'েয়েছেন':['ায়', ''],
    'িয়েছেন':['িয়', ''],
    'য়েছেন':['য়', ''],
    'ে.েছেন':['া.', ''],
    'েছেন':['েছ', ''],
    'ছেন':['ছ', ''],
    #-----------------#
    'েয়েছিল':['ায়', ''],
    'িয়েছিল':['িয়', ''],
    'য়েছিল':['য়', ''],
    'ে.েছিল':['া.', ''],
    'েছিল':['েছ', ''],
    'ছিল':['ছ', ''],
    #----------------#
    'েয়েছিলা':['ায়', ''],
    'িয়েছিলা':['িয়', ''],
    'য়েছিলা':['য়', ''],
    'ে.েছিলা':['া.', ''],
    'েছিলা':['েছ', ''],
    'ছিলা':['ছ', ''],
    #------------------#
    'েয়েছিলাম':['ায়', ''],
    'িয়েছিলাম':['িয়', ''],
    'য়েছিলাম':['য়', ''],
    'ে.েছিলাম':['া.', ''],
    'েছিলাম':['েছ', ''],
    'ছিলাম':['ছ', ''],
    #------------------#
    'েয়েছিলেন':['ায়', ''],
    'িয়েছিলেন':['িয়', ''],
    'য়েছিলেন':['য়', ''],
    'ে.েছিলেন':['া.', ''],
    'েছিলেন':['েছ', ''],
    'ছিলেন':['ছ', ''],
    #------------------#
    'েয়েছিলে':['ায়', ''],
    'িয়েছিলে':['িয়', ''],
    'য়েছিলে':['য়', ''],
    'ে.েছিলে':['া.', ''],
    'েছিলে':['েছ', ''],
    'ছিলে':['ছ', ''],
    #-----------------#
    'েয়েছিলি':['ায়', ''],
    'িয়েছিলি':['িয়', ''],
    'য়েছিলি':['য়', ''],
    'ে.েছিলি':['া.', ''],
    'েছিলি':['েছ', ''],
    'ছিলি':['ছ', ''],
    #--------------#
    'েয়েছিস':['ায়', ''],
    'িয়েছিস':['িয়', ''],
    'য়েছিস':['য়', ''],
    'ইছিস':['য়', ''],
    'ে.েছিস':['া.', ''],
    'ছিস':['ছ', ''],
    'িস':['িস', ''],
    #-----------------#
    'িয়ে':['িয়ে', 'া'],        # পালিয়ে দমিয়ে
    'েয়ে':['ায়', ''],         # গেয়ে পেয়ে
    'ইয়ে':['য়', ''],          # পাইয়ে, যাইয়ে
    'ায়ে':['া', ''],          # নায়ে পায়ে গায়ে
    'য়ে':['য়', 'য়'],          # হয়ে, লয়ে
    #---------------#
    # Bare present-tense habitual ending (word+e with no semivowel
    # marker, e.g. করে -> কর). Must come last in this dict: every pattern
    # above this point is a longer, more specific final shape and has to
    # get first refusal, since bare e would otherwise match the tail of
    # all of them too (end-anchored, first-match-wins loop in stemmer.py).
    # Short-root branch (checklen==1, e.g. closed-class pronouns) is left
    # unchanged, same conservatism used elsewhere in this table -- to_fix.md.
    'ে':['ে', '']
}

#------------- Rules for special inflection ---------------#
sp_initial_dict = {
    'ই':['ই', ''],
    'ও':['ও', ''],
    'তো':['ত', ''],
    'কে':['ক', ''],
    'তে':['ত', ''],
    'রা':['র', '']
}

sp_final_dict = {
    'টির':['টি', ''],
    'টার':['টা', ''],
    #--------------#
    'লেন':['ল', ''],
    'লাম':['ল', ''],
    'দের':['দের', ''],
    'বেন':['ব', ''],
    #---------------#
    # 'েল':''
    # 'েলো':'েল', #খেলো  মেলো
    # 'ওয়া':
    #---------------#
    'েশে':['েশ', 'েশ'],        # দেশে কেশে
    'ে.ে':['া.', 'ে.'],         # হেসে নেচে -- gated by ee_harmony_roots, see below
    'েঁ.ে':['াঁ.', 'েঁ.'],       # কেঁদে, বেঁচে -- candrabindu-bearing cousin of
                                 # the rule above. A literal চন্দ্রবিন্দু sits
                                 # between the vowel sign and the medial
                                 # consonant (কেঁদে is 5 codepoints: ক,ে,ঁ,দ,ে),
                                 # so the plain 'ে.ে' pattern's single-char
                                 # wildcard structurally can't match these
                                 # words at all -- they were being left
                                 # completely unstemmed, not mis-stemmed.
                                 # Needs its own gated key; see
                                 # ee_harmony_rule_keys below and to_fix.md.
    'া.া.ার':['া.া', ''],   # নামাবার, জানালার
    'া.ার':['া.া', 'া.া'],   # কামার, জানার
    'ের':['ের', ''],        # শের
    'ার':['ার', 'া'],        #কার মার যার
    'ির':['ির', 'ি'],       # মালির -> মালি (possessive on i-final roots,
                                     #  e.g. বাড়ির -> বাড়ি); short-root branch
                                     # left unchanged, same conservatism as elsewhere
                                     # -- to_fix.md
    'েন':['েন', ''],
    #---------------#
    'লি':['লি', ''],
    'টি':['টি', ''],
    'টা':['টা', ''],
    'ছি':['ছি', ''],
    #---------------#
    'রছ':['র', 'র'],
    'ড়ছ':['ড়', 'ড়'],
    'রব':['র', 'র'],
    'ড়ব':['ড়', 'ড়']
}

# Roots that undergo the আ<->ে vowel-harmony alternation before the bare
# -e present/participle marker (হাস+e -> হেসে, নাচ+e -> নেচে).
# sp_final_dict's 'e.e' rule matches this Cons-e-Cons-e surface shape,
# but that shape also occurs coincidentally in words whose root already
# contains an internal e (ছেলে "boy", দেখে "sees") or in
# other unrelated nouns -- without a lexicon there's no way to tell a
# real harmony alternation from a coincidental match, so the rule is
# restricted to only fire for this small, explicitly attested set of
# roots. See to_fix.md.
#
# Expanded 2026-08-05 (Task #14 Phase B): this turned out to be a closed
# lexical class, not something POS-tagging can gate (verb-tagging alone
# can't distinguish real harmony roots from verbs whose root already ends
# in e, e.g. দেখ/ফেল -- see to_fix.md). Instead cross-validated candidates
# from every gate-relevant word type in lexicon.parquet (freq >= 100)
# against the lexicon itself: a genuine root R should appear as both
# R+'া' (infinitive/verbal noun, e.g. কাটা) and R+'তে' (purposive
# infinitive, e.g. কাটতে) with real, comparable frequency; coincidental
# matches (তা+ার="তার", noun মাথা->"মাথ") don't. Threshold: both forms
# >=5000 and neither more than 50x the other. 6 candidates that cleared
# the threshold were held back anyway: 5 (কাদ/বাচ/ঘাট/কাপ/হাট) each
# collide with an unrelated, higher-frequency reading of the exact same
# spelling once double-checked -- কাদা "mud", ঘাট "riverbank/dock" noun,
# কাপ "cup" loanword, হাটে "at the market" (noun locative), and বাচ
# is dominated by বেচে "sells" (from বেচা, an unrelated verb spelled
# identically); the 6th, হাজ, had weak/inconsistent evidence either way.
# (An earlier version of this comment blamed a candrabindu-loss bug for
# these 5 -- wrong; they're plain 4-codepoint words with nothing to
# lose. The candrabindu-bearing cousins of these same roots, e.g. কাঁদ
# for কেঁদে, are a genuinely separate set of lexicon entries the old
# pattern never matched at all -- see 'েঁ.ে' above and its own roots
# below.)
ee_harmony_roots = {
    'হাস', 'নাচ',
    # 28 below added from the Phase B corpus cross-validation:
    'জান', 'রাখ', 'মার', 'টান', 'কাট', 'ভাব', 'মান', 'নাম', 'চাপ', 'ভাঙ',
    'সাজ', 'পার', 'লাগ', 'হান', 'ভাজ', 'ছাপ', 'হার', 'ভাস', 'মাখ', 'ঢাল',
    'ফাট', 'বাজ', 'থাম', 'মাপ', 'জাগ', 'চাট', 'খাট', 'মাজ',
    # candrabindu-bearing roots (েঁ.ে pattern), added the same session
    # after cross-validating the 134-candidate েঁ.ে$ set the same way.
    # Several real verbs (ঘাঁট, ভাঁজ, ছাঁট, ফাঁপ, ফাঁস...) didn't clear
    # the frequency threshold and were left out rather than added on
    # weaker evidence -- see to_fix.md if revisiting with a lower bar:
    'বাঁধ', 'হাঁট', 'বাঁচ', 'কাঁদ', 'কাঁপ', 'গাঁথ', 'রাঁধ',
}
ee_harmony_rule_keys = {'ে.ে', 'েঁ.ে'}

# Words confirmed (corpus_sample_validated.csv review) to be fully
# lexicalized/monomorphemic in modern Bangla despite starting with what
# looks like a der_initial_dict prefix -- stripping that "prefix"
# false-merges them into an unrelated real word or garbage (e.g.
# বিশ্বাস "belief" -> শ্বাস "breath" if বি- fires; নির্বাচন "election"
# -> বাচন "diction" if নির্- fires). Checked with str.startswith in
# apply_ffth_rule against the word as it arrives at the prefix stage
# (i.e. after inflectional suffixes are already stripped), so this also
# protects untested inflected forms of the same roots, not just the
# exact words below. Same "no lexicon" failure class noted throughout
# to_fix.md -- this is a seed list from confirmed cases, not a general
# solution; see to_fix.md's der_initial_dict item for the many other
# known-affected words not yet added here.
protected_prefix_roots = (
    'বিশ্বাস',
    'অতিথি',
    'নির্বাচন',
    'সমঝোতা',
    'বিশিষ্ট',
    'বিরতিস্পেস',
    'পরিবর',
    'বিলিরি',
    'বিছট',
)

der_initial_dict = {
    'প্রতি':['প্রতি', ''],
    'দুশ্চি':['দুশ্চি', 'চি'],
    'দুর্':['দুর্', ''],
    'দুঃ':['দুঃ', ''],
    'দুরা':['দুরা', 'আ'],
    'বি':['বি', ''],
    'অত্যা':['অত্যা', 'আ'],
    'অধি':['অধি', ''],
    'অনু':['অনু', ''],
    'উদ':['উদ', ''],
    # 'অন' (2-char prefix, was here for "without/dis-") removed: every
    # word it actually fired on empirically (অনটন, অনল, etc.) produced a
    # nonsense fragment, not a real root, and the two "genuine" examples
    # this comment used to cite never actually exercised this rule in
    # practice (one is blocked by invalid_word_start, the other is caught
    # by an unrelated earlier rule first). Confirmed bug it caused:
    # অনমনীয় -> অ + নমনীয় (Dasgupta & Ng gold set), see to_fix.md.
    # No lexicon-free way found to keep 'অন' for real cases without this
    # kind of over-stripping, so it's dropped rather than patched.
    # Added from Thompson, "Bengali" (2012), ch. 4 "Word formation", p.36-39 --
    # the standard Sanskrit/Bangla prefix inventory. Prefixes shorter than
    # these (bare আ-, নি-, সু-) or belonging to a different register (Farsi/
    # Arabic loan prefixes be-, dɔr-, na-, bɔd-, gɔr-, am-, listed on the same
    # pages) were left out as too collision-prone or out of scope -- see
    # to_fix.md.
    'অপ':['অপ', ''],     # mis-, off, away (ɔpô-)
    'অব':['অব', ''],     # down, inferior (ɔbô-)
    'অভি':['অভি', ''],   # excess, towards (ôbhi-)
    'অতি':['অতি', ''],   # too, excessive (ôti-)
    'উপ':['উপ', ''],     # over, under, sub- (upô-)
    'নির্':['নির্', ''],  # negating, without (nir-)
    'পরা':['পরা', ''],   # other, reverse (pɔra-)
    'পরি':['পরি', ''],   # thoroughness, around, opposition (pôri-)
    # 'প্র' (forth, abundance, excess -- prô-) tried and reverted: regressed
    # প্রজাপতি ("butterfly", a single lexical item with no real প্র- prefix
    # meaning) to জাপতি against the output_validated.csv baseline. See
    # to_fix.md.
    'সং':['সং', ''],     # together, with (sɔṁ-)
    'সম':['সম', '']      # together, with (sɔm-)
}

der_final_dict = {
    'বান':['বান', ''],
    'মান':['মান', ''],
    'শীল':['শীল', ''],
    'য়ি':['য়ি', ''],
    'ন্ত':['ন্ত', ''],
    # Added from Thompson, "Bengali" (2012), ch. 4 "Word formation", p.40-43.
    # Suffixes needing a root-vowel change to strip correctly (e.g. -ik
    # আঞ্চলিক<-অঞ্চল, -o মেজো<-মধ্য, -i নীতি<-নীত), or that collide with a
    # common independent word (-ami আমি = the pronoun "I"; kɔr/pɔr's পর =
    # the common word "other/after"), were left out -- see to_fix.md.
    'ওয়ালা':['ওয়ালা', ''],  # person doing a job/task (-oỵala)
    'জনক':['জনক', ''],      # generating, causing (-jɔnôk)
    'কর':['কর', ''],        # assigning a quality (-kɔr)
    # 'তা' (abstract noun, -ness/-ity -- very productive) tried and reverted:
    # regressed দুর্লতা ("creeper/vine", a single lexical item, not root+তা)
    # to ল, and দুশ্চিন্তা to চিন্ (pre-stripping তা before the প্রতি-family
    # prefix stage got a chance to run its own, correct one-shot strip) --
    # against the output_validated.csv baseline. See to_fix.md.
    'গত':['গত', ''],        # pertaining to, obtained/held (-gɔtô)
    'উক':['উক', ''],        # desiring/prone to (-uk)
    'সই':['সই', ''],        # attributes a characteristic (-sôi)
    'ইত':['ইত', '']         # past-participle-like adjective (-itô)
}
