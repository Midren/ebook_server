from nltk.corpus import wordnet as wn


class Graph:
    """Represents graph as data structure."""

    def __init__(self):
        """Initialize empty graph."""
        self.edges = {}
        self.leng = {}
        self.num = {}

    def add_vertex(self, word):
        """
        (self, str) -> None.

        Add vertex to graph with word as data.
        """
        if word not in self.edges:
            self.edges[word] = set()

    def add_edge(self, word1, word2):
        """
        (self, str, str) -> None.

        Make edge between two vertexes.
        """
        self.edges[word1].add(word2)
        self.edges[word2].add(word1)

    def count_len(self):
        """
        (self) -> None.

        Count number of edges in all vertexesself.
        """
        for vertex in self.edges.keys():
            self.leng[vertex] = len(self.edges[vertex])

    def merge(self, another_graph):
        """
        (Graph, Graph) -> None.

        Merge two graphes.
        """
        for edge in another_graph.edges:
            try:
                self.edges[edge].update(another_graph.edges[edge])
            except KeyError:
                self.edges[edge] = another_graph.edges[edge]

    def count_num(self, lst):
        """
        (self, list) -> None.

        Place all vertexes in some order.
        """
        for number, vertex in enumerate(lst):
            self.num[vertex] = number


def get_similar(synset):
    """
    (synset) -> set.

    Return set with all synsets that are similar to this synset.
    """
    if isinstance(synset, int):
        return None
    similar_words = set()
    similar_words.update(synset.member_holonyms())
    similar_words.update(synset.member_meronyms())
    similar_words.update(synset.hypernyms())
    similar_words.update(synset.hyponyms())
    similar_words.update(synset.part_holonyms())
    similar_words.update(synset.part_meronyms())
    return similar_words


def add_similar(graph, synset, depth=0):
    """
    (Graph, synset, int) -> None.

    Add similar synsets to graph.
    """
    for word in get_similar(synset):
        graph.add_vertex(word)
        graph.add_edge(synset, word)
        if depth < 3:
            add_similar(graph, word, depth + 1)


def build_word_graph(lemmas_set, start_word, root=False, depth=0):
    """
    (set, str, bool, int) -> Graph.

    Return graph with words from lemmas_set where start_word will be root.
    """
    graph = Graph()
    if root:
        graph.add_vertex(start_word)
    for word_lemma, word_pos in lemmas_set:
        start_words = wn.synsets(word_lemma, pos=word_pos)
        if not start_words:
            continue
        graph.add_vertex(start_words[0])
        if root:
            graph.add_edge(start_word, start_words[0])
        for word in start_words:
            graph.add_vertex(word)
            graph.add_edge(start_words[0], word)
            add_similar(graph, word, depth)
    return graph


def get_top_synsets(graph, start_word, root=False, number=3):
    """
    (Graph, tuple, bool, int) -> list.

    Return top synsets in graph which are sorted by PageRank algorithm,
    where start_word is root
    """
    graph.count_len()
    graph_vertexes = list(graph.edges.keys())
    graph.count_num(graph_vertexes)
    N = len(graph.edges)
    pagerank = [1 / N for i in range(N)]

    for _ in range(20):
        for i, vertex in enumerate(graph_vertexes):
            pagerank[i] = 0.85 / N + 0.15 * sum([pagerank[graph.num[j]] /
                    graph.leng[j] for j in graph.edges[vertex]])
    possible_explanation = []
    if root:
        senses = graph.edges[start_word]
    else:
        senses = wn.synsets(start_word[0], start_word[1])
    print(senses)

    for i in range(N):
        if graph_vertexes[i] in senses:
            print(graph_vertexes[i], pagerank[i])
            possible_explanation.append((pagerank[i], graph_vertexes[i]))

    return list(map(lambda x: x[1], sorted(possible_explanation)[:number]))
