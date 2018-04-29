from app import app
from flask import jsonify, request
from sentence_processing.definitions import get_definitions
from sentence_processing.idiom_processing import get_idiom, get_all_idioms_dict
from time import time
import json

idiom_dict = get_all_idioms_dict()


@app.route("/", methods=["POST", "GET"])
def hello_world():
    st = time()
    data = request.data
    data_dict = json.loads(data)
    sentence = data_dict.get("sentence").lower().strip()
    word = data_dict.get("word").lower().strip()
    word_order = int(data_dict.get("word_order"))
    # sentence = "I worked all day on the farm or all day on factory and find out about her".lower()
    # word = "worked"
    # word_order = 0
    idiom = True
    try:
        i_word, i_category, i_defs = get_idiom(sentence, word, word_order, idiom_dict)
    except TypeError:
        idiom = False
    print(time() - st)
    word, category, defs = get_definitions(sentence, word, word_order)
    print(time() - st)
    if(idiom):
        return jsonify(
            {"senses":
                {"word_sense": {"definitions": defs, "category": category},
                "idiom_sense": {"definitions": i_defs, "category": i_category}
                },
            "word": word})
    else:
        return jsonify(
            {"senses":
                {"word_sense": {"definitions": defs, "category": category},
                "idiom_sense": None},
            "word": word})
