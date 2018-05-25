from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
import nltk


def get_pos_tokens_dict(sentence):
    """
    (str) -> dict.

    Return dictionary, where key is word and value
    is list with Part-Of-Speech tags, index of tag in list
    is order of occurrence
    """
    tokenized_sen = nltk.word_tokenize(sentence)
    tokens_lst = get_pos_tokens_list(tokenized_sen)
    tokens_dict = defaultdict(list)
    for word, word_class in tokens_lst:
        tokens_dict[word].append(word_class)
    return tokens_dict


def get_pos_tokens_list(tokenized_sen):
    """
    (list) -> list.

    Return list of part-of-speech tags for tokenized sentence.
    """
    return nltk.pos_tag(tokenized_sen)


def get_lemmatized_sen(sentence):
    """
    (str) -> list.

    Return list of lemmatized words of this sentence.
    """
    tokenized_sen = nltk.word_tokenize(sentence)
    tokens_dict = get_pos_tokens_dict(sentence)
    lemmatized_sen = []
    for word in tokenized_sen:
        lemmatized_sen.append(lemmatize(word, tokens_dict).strip("-–"))
        del tokens_dict[word][0]
    return lemmatized_sen


def lemmatize_word(sentence, word, order):
    """
    (str, str, int) -> str.

    Return lemmatized word.
    """
    tokens_dict = get_pos_tokens_dict(sentence)
    return lemmatize(word, tokens_dict, order)


def get_pos_wn(word, tokens_dict, order=0):
    """
    (str, dict, int) -> str.

    Return part-of-speech of word in WordNet's representation.
    """
    word_class = tokens_dict[word][order]
    if word_class in ['NN', 'NNS', 'NNP', 'NNPS']:
        return wn.NOUN
    elif word_class in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return wn.VERB
    elif word_class in ['RB', 'RBR', 'RBS']:
        return wn.ADV
    elif word_class in ['JJ', 'JJR', 'JJS']:
        return wn.ADJ


def simple_wn_2_oxf(wn_class):
    """
    (str) -> str.

    Return part-of-speech in Oxford's representation from WordNet's that is
    two charachters long.
    """
    wn_2_oxf = {wn.ADJ: "Adjective", wn.ADV: "Adverb", wn.NOUN: "Noun",
                wn.VERB: "Verb", wn.ADJ_SAT: "Adjective"}
    return wn_2_oxf[wn_class]


def wn_2_oxf(wn_class):
    """
    (str) -> str.

    Return WordNet's representation of part-of-speech from Oxford's.
    """
    wn_2_oxf = {"JJ": "Adjective", "RB": "Adverb", "CC": "Conjuction",
                "DT": "Determiner", "UH": "Interjection", "NN": "Noun",
                "CD": "Numeral", "IN": "Preposition", "PRP": "Pronoun",
                "VB": "Verb"}
    return wn_2_oxf[wn_class]


def oxf_2_wn(oxf_class):
    """
    (str) -> str.

    Return lexical category in WordNet form from
    lexical category from Oxford API.
    """
    oxf_2_wn = {"Adjective": "JJ", "Adverb": "RB", "Conjuction": "CC",
                "Determiner": "DT", "Idiomatic": "Idiomatic",
                "Interjection": "UH", "Noun": "NN", "Numeral": "CD",
                "Other": "Other", "Prefix": "Prefix", "Preposition": "IN",
                "Pronoun": "PRP", "Suffix": "Suffix", "Verb": "VB"}
    return oxf_2_wn[oxf_class]


def lemmatize(word, tokens_dict, order=0):
    """
    (str, dict, int) -> str.

    Return lemmatized word using dict of tokens and order of word in
    sentence.
    """
    pos_tag = get_pos_wn(word, tokens_dict)
    if pos_tag:
        poss_lemm = wn._morphy(word, pos_tag)
    else:
        poss_lemm = ""
    if len(poss_lemm) == 1:
        return poss_lemm[0]
    else:
        if tokens_dict[word][order] in "VBD VBN":
            for w in poss_lemm:
                if w != word:
                    return w
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized = wordnet_lemmatizer.lemmatize(word)
    return lemmatized


def get_sen_lemmas_set(sentence, word=None, word_order=0):
    """
    (str, str, int) -> set.

    Return set of lemmas of words in this sentence.
    """
    tokens_dict = get_pos_tokens_dict(sentence)
    lemmas_set = set()

    for token in tokens_dict.keys():
        for order, pos in enumerate(tokens_dict[token]):
            if not (token in punctuation or (
                    token in stopwords.words("english"))) or token == word:
                lemma = lemmatize(token, tokens_dict, order)
                lemmas_set.add((lemma, get_pos_wn(token, tokens_dict, order)))

    if word:
        word_lemma = lemmatize(word, tokens_dict, word_order)
        word_pos = get_pos_wn(word, tokens_dict, word_order)
        return lemmas_set, (word_lemma, word_pos)
    return lemmas_set
