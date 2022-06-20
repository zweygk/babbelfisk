from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin
from copy import deepcopy
from numerizer import numerize
from g2p_en import G2p

import nltk
import string
import spacy 



app = Flask(__name__)
CORS(app)

nlp = spacy.load("en_core_web_sm")
nlp.tokenizer.rules = {key: value for key, value in nlp.tokenizer.rules.items() if "'" not in key and "’" not in key and "‘" not in key}

nltk.download('brown')
nltk.download('names')

arpabet = nltk.corpus.cmudict.dict()

g2p = G2p()

from normalise import normalise


@app.route('/', methods=['GET'])
def health():
    # Response with 200 to GET request (health check). Separated so as to not require auth.
    return Response('{"ok":"ok"}', status=200, mimetype='application/json')


@app.route('/', methods=['POST'])
def main():

    user_abbrevs = {"what's": "what's"}

    def _normalize(text):
        # some issues in normalise package
        try:
            return ' '.join(normalise(text, variety="AmE", user_abbrevs=user_abbrevs, verbose=False))
        except:
            return text
    
    def _remove_punct(doc):
        l =  [t for t in doc if t.text not in string.punctuation.replace("'", "").replace("’", "").replace("‘", "")]
        l2 = []
        for i, token in enumerate(l):
            indices_left = len(l)-1-i
            if token.text in ["'s", "’s", "‘s"]:
                continue
            if indices_left > 0:
                next_token = l[i+1]
                if next_token.text in ["'s", "’s", "‘s"]:
                    l2.append("".join([token.text, next_token.text]))
                else:
                    l2.append(token.text)
        return l2

    def _get_cmudict_pronunciations(wordlist):
        lex = {}
        for word in wordlist:
            try:
                pronunciation = arpabet[word.lower()][0]
                for i, p in enumerate(pronunciation):
                    if len(p) > 2: pronunciation[i] = p[:2]
                lex[word.upper()] = pronunciation
            except Exception as e:
                lex[word.upper()] = None
        return lex

    def _get_g2p_pronunciations(cmu_lex):
        lex = deepcopy(cmu_lex)
        for word, pronunciation in lex.items():
            if not pronunciation:
                p = g2p(word)
                p_nopos = [ ''.join([i for i in s if not i.isdigit()]) for s in p ]
                lex[word] = p_nopos
        return lex

    def process_and_generate(text):
        normalized_text = _normalize(text)
        renumerized_text = numerize(normalized_text)
        doc = nlp(renumerized_text)
        removed_punct = _remove_punct(doc)
        cmu_lex = _get_cmudict_pronunciations(removed_punct)
        cmu_g2p_lex = _get_g2p_pronunciations(cmu_lex)
        return cmu_g2p_lex

    
    sentence = request.json['sentence']
    lex = process_and_generate(sentence)

    json_output = jsonify(
        lex = lex
    )

    print(lex)

    return json_output


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5002)