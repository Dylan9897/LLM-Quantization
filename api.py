from flask import Flask, request, Response, jsonify
from stanfordcorenlp import StanfordCoreNLP

app = Flask(__name__)

nlp = StanfordCoreNLP(r'ckpt/stanford-corenlp-full-2018-10-05/', lang='en', quiet=False)

class StandfordParser():
    namespace="/stanford"

    @app.route(namespace+'/postag', methods=["POST"])
    def postag():
        return jsonify(nlp.pos_tag(request.json['text']))
    
    @app.route(namespace+'/ner', methods=["POST"])
    def ner():
        return jsonify(nlp.ner(request.json['text']))
    
    @app.route(namespace+'/dependency_parser', methods=["POST"])
    def dependency_parser():
        return jsonify(nlp.dependency_parse(request.json['text']))


    @app.route(namespace+'/parse', methods=["POST"])
    def parse():
        return jsonify(nlp.parse(request.json['text']))


    @app.route(namespace+'/tokenize', methods=["POST"])
    def tokenizer():
        return jsonify(nlp.word_tokenize(request.json['text']))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=20010)

