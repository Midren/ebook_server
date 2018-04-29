from nltk.corpus import wordnet as wn
from pprint import pprint
from . import auxiliar_functions
from . import graph_word_wsd
import json
import requests

def get_wn_definitions(sentence, word, word_order):
    lemmas_set, start_word = auxiliar_functions.get_sen_lemmas_set(sentence, word, word_order)
    graph = graph_word_wsd.build_word_graph(lemmas_set, start_word)
    synsets = graph_word_wsd.get_top_synsets(graph, start_word)
    word_definitions = []
    for synset in synsets:
        word_definitions.append({
            "definition": synset.definition()
        })
        try:
            word_definitions[-1].update({"example": synset.examples()[0]})
        except IndexError:
            continue
    return start_word[0], auxiliar_functions.simple_wn_2_oxf(start_word[1]), word_definitions


def get_oxf_definitions(word, word_pos):
    """
    Get definitions of word from Oxford API
    """
    app_id = '0dd8f390'
    app_key = '1671423a9398f671e334350676749918'
    url = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/" + word
    ret = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    word_definitions = list()
    for lexical_category in json.loads(ret.text)["results"][0]["lexicalEntries"]:
        for definition in lexical_category["entries"][0]["senses"]:
            try:
                wn_lexical_cat = auxiliar_functions.oxf_2_wn(lexical_category["lexicalCategory"])
                if wn_lexical_cat == word_pos:
                    word_definitions.append({
                        "definition": definition["definitions"][0],
                        "example": definition["examples"][0]["text"]
                    })
            except KeyError:
                pass
    return word, auxiliar_functions.wn_2_oxf(word_pos), word_definitions


def get_definitions(sentence, word, word_order):
    senses = []
    tokens_dict = auxiliar_functions.get_pos_tokens_dict(sentence)
    start_word = auxiliar_functions.get_pos_wn(word, tokens_dict, word_order)
    if(start_word):
        senses.extend(get_wn_definitions(sentence, word, word_order))
    else:
        senses.extend(get_oxf_definitions(word, tokens_dict[word][word_order]))
    return senses

if __name__ == "__main__":
    # sentence = input("Write sentence: ")
    # word = input("Write unknown word in this sentence: ")
    # order = 1
    # if sentence.count(word) > 1:
    #     order = int(input("Write order of word in this sentence: "))
    # pprint(get_definitions(word, sentence, order - 1))
    sentence = "Maybe it's vice versa".lower()
    word = "vice"
    word_order = 0
    pprint(get_definitions(sentence, word, word_order))
