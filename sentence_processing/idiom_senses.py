import graph_word_wsd
import auxiliar_functions as af
import idiom_processing as ip
from nltk.corpus import wordnet as wn
from pprint import pprint

def get_idiom_definitions(sentence, word, word_order):
    idiom_name, _, def_examples = ip.get_idiom(sentence, word, word_order)
    lemmas_set = af.get_sen_lemmas_set(sentence)
    graph = graph_word_wsd.build_word_graph(lemmas_set, word)

    graph.add_vertex("start")
    for num, sense in enumerate(def_examples):
        new_sense = num
        graph.add_vertex(new_sense)
        graph.add_edge("start", new_sense)

        lemmas_set = af.get_sen_lemmas_set(sense["definition"].lower())
        gr = graph_word_wsd.build_word_graph(lemmas_set, new_sense, True, 1)
        graph.merge(gr)

        lemmas_set = af.get_sen_lemmas_set(sense["example"].lower())
        gr = graph_word_wsd.build_word_graph(lemmas_set, new_sense, True)
        graph.merge(gr)

    definitions = graph_word_wsd.get_top_synsets(graph, "start", True)
    print(list(map(lambda x: def_examples[x], definitions)))
    print(definitions)

if __name__ == "__main__":
    sentence = """as soon as, I got off, I bumped into an old shoolmate, Mark""".lower()
    pprint(get_idiom_definitions(sentence, "got", 0))
