from collections import defaultdict
from pprint import pprint
import json
from . import auxiliar_functions as af


class IdiomExpression:
    """This class represents idiom expression."""

    def __init__(self, name, definition, example, kind):
        """Initialize idiom expression with name, definition and example."""
        self.name = name
        self.lemmatized = af.get_lemmatized_sen(name)
        self.definition = definition
        self.example = example
        self.kind = kind.strip()

    def __repr__(self):
        """Represent idiom in repr form."""
        return "<Idiom: " + self.name + ": " + self.definition + ": " +\
            self.kind + ">"

    def check_sentence(self, lemmatized_sen):
        """
        (self, list) -> tuple.

        Check sentence if it has idiom expression.
        """
        answer = None
        if self.kind == "inseparable" or self.kind == "intransitive":
            answer = self._check_inseparable(lemmatized_sen)
        elif self.kind == "separable [optional]":
            answer = self._check_inseparable(lemmatized_sen) or \
                self._check_separable(lemmatized_sen)
        elif self.kind == "separable [obligatory]":
            answer = self._check_separable(lemmatized_sen)
        if answer and answer[0] == answer[1]:
            return tuple([answer[0]] + [answer[1] + i + 1
                for i in range(len(self.lemmatized) - 1)])
        elif answer:
            return tuple([answer[0]] + [answer[1] + i
                for i in range(len(self.lemmatized) - 1)])

    def _check_inseparable(self, lemmatized_sen):
        """
        (self, list) -> int, int.

        Check sentence if it has an inseparable idiom expression.
        """
        st = -1
        while(True):
            try:
                st = st + 1 + lemmatized_sen[st + 1:].index(self.lemmatized[0])
            except ValueError:
                return False
            try:
                replacing_words = set(["you", "your", "someone", "something",
                                       "somebody"])
                for word in range(st, st + len(self.lemmatized)):
                    if self.lemmatized[word - st] in replacing_words:
                        continue
                    if lemmatized_sen[word] != self.lemmatized[word - st]:
                        break
                else:
                    return st, st
            except IndexError:
                break

    def _check_separable(self, lemmatized_sen):
        """
        (self, list) -> int, int.

        Check sentence if it has an separable idiom expression.
        """
        fst = -1
        while(True):
            try:
                fst = fst + 1 + \
                    lemmatized_sen[fst + 1:].index(self.lemmatized[0])
                snd = fst + 1 + \
                    lemmatized_sen[fst + 1:].index(self.lemmatized[1])
            except ValueError:
                return False
            if snd - fst > 7 or snd - fst < 2:
                continue
            else:
                for i in range(2, len(self.lemmatized)):
                    if lemmatized_sen[snd + i - 1] != self.lemmatized[i]:
                        break
                else:
                    for token in af.get_pos_tokens_list(lemmatized_sen[
                            fst + 1: snd]):
                        if token[1][:2] == "VB" or token[1][0] == "R":
                            return False
                    return fst, snd


class IdiomDict:
    """Represents dictionary of idioms."""

    def __init__(self):
        """Initialize class with empty dict."""
        self.idioms = defaultdict(list)

    def add_idiom(self, idiom):
        """
        (self, IdiomExpression) -> None.

        Add idiom to dictionary.
        """
        self.idioms[idiom.name].append(idiom)

    def __getitem__(self, key):
        """
        (self, IdiomExpression) -> None.

        Return idiom by idiom's name.
        """
        return self.idioms[key]

    def __len__(self):
        """
        (self) -> int.

        Return count of elements in dictionary.
        """
        return len(self.idioms)

    def __iter__(self):
        """
        (self) -> iter.

        Return iterator for the elements of dictionary.
        """
        return self.idioms.__iter__()

    def find_idioms(self, lemmatized_sen):
        """
        (self, list) -> defaultdict.

        Return idioms that are in lemmatized sentence.
        """
        idioms = defaultdict(list)
        for idiom in self:
            for exp in self[idiom]:
                index_list = exp.check_sentence(lemmatized_sen)
                if index_list:
                    idioms[index_list].append(exp)
        return idioms


def get_all_idioms_dict():
    """
    (None) -> IdiomDict.

    Return dictionary with all idioms.
    """
    idioms = json.loads(open("expressions.json").read().strip())
    idiom_dict = IdiomDict()
    for idiom in idioms:
        idiom_dict.add_idiom(IdiomExpression(idiom["name"],
                                             idiom["definition"],
                                             idiom["example"],
                                             idiom["kind"]))
    return idiom_dict


def get_idiom(sentence, word, word_order, idiom_dict=None):
    """
    (str, str, int, IdiomDict) -> str, str, list.

    Return idiom if word is part of it or None either.
    """
    if not idiom_dict:
        idiom_dict = get_all_idioms_dict()
    lemmatized_sen = af.get_lemmatized_sen(sentence)
    lemma = af.lemmatize_word(sentence, word, word_order)
    current_ord = 0
    for num, word in enumerate(lemmatized_sen):
        if word == lemma:
            if current_ord == word_order:
                break
            current_ord += 1
    possible_idioms = idiom_dict.find_idioms(lemmatized_sen)
    idioms_num = list(filter(lambda x: num in x, possible_idioms))
    if(not idioms_num):
        return None
    if len(idioms_num) > 1:
        idioms_num.sort(key=lambda x: len(x), reverse=True)
    idioms = possible_idioms[idioms_num[0]]
    idioms_def_example = [{"definition": idiom.definition,
                           "example": idiom.example} for idiom in idioms]
    return idioms[0].name, "Idiomatic phrase", idioms_def_example


if __name__ == "__main__":
    sentence = """Maybe it's vice versa""".lower()
    pprint(get_idiom(sentence, "versa", 0))
