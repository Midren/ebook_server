from app import app
from flask import jsonify, request
from sentence_processing.definitions import get_definitions
from sentence_processing.idiom_processing import get_idiom, get_all_idioms_dict
from time import time
import json

idiom_dict = get_all_idioms_dict()


@app.route("/", methods=["POST"])
def main():
    """Give user opportunity to get definitions using POST request."""
    st = time()
    data = request.data
    data_dict = json.loads(data)
    sentence = data_dict.get("sentence").lower().strip()
    word = data_dict.get("word").lower().strip()
    word_order = int(data_dict.get("word_order"))
    # sentence = " My name is Roman ".lower().strip()
    # word = " name ".strip()
    # word_order = 0
    idiom = True
    try:
        i_word, i_category, i_defs = get_idiom(sentence, word, word_order,
                                               idiom_dict)
    except TypeError:
        idiom = False
    print(time() - st)
    word, category, defs = get_definitions(sentence, word, word_order)
    print(time() - st)
    if(idiom):
        return jsonify(
            {"senses":
                {"word_sense": {"definitions": defs, "category": category},
                 "idiom_sense": {"definitions": i_defs, "category": i_category,
                                 "idiom_name": i_word}
                 },
             "word": word})
    else:
        return jsonify(
            {"senses":
                {"word_sense": {"definitions": defs, "category": category},
                 "idiom_sense": None},
             "word": word})
