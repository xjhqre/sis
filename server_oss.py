# -*- coding: utf-8 -*-
from PIL import Image
from elasticsearch import Elasticsearch

import config
from feature_extractor import FeatureExtractor
from flask import Flask, request, render_template

'''
    以图搜图服务
'''

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Read image features
fe = FeatureExtractor()

es = Elasticsearch([{'host': config.elasticsearch_url, 'port': config.elasticsearch_port}], timeout=3600)


def feature_search(query):
    global es
    # print(query)
    results = es.search(
        index=config.elasticsearch_index,
        body={
            "size": 30,
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.queryVector, doc['feature'])+1.0",
                        "params": {
                            "queryVector": query
                        }
                    }
                }
            }
        })
    hitCount = results['hits']['total']['value']

    if hitCount > 0:
        # if hitCount is 1:
            # print(str(hitCount), ' result')
        # else:
            # print(str(hitCount), 'results')
        answers = []
        max_score = results['hits']['max_score']

        if max_score >= 0.35:
            for hit in results['hits']['hits']:
                if hit['_score'] > 0.5 * max_score:
                    imgurl = hit['_source']['url']
                    name = hit['_source']['name']
                    imgurl = imgurl.replace("#", "%23")
                    answers.append([imgurl, name])
    else:
        answers = []
    return answers


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        # print(file.filename)
        uploaded_img_path = "static/uploaded/" + file.filename
        # print(uploaded_img_path)
        img.save(uploaded_img_path)

        # Run search
        query = fe.execute(uploaded_img_path)
        answers = feature_search(query)

        return render_template('index.html',
                               query_path=uploaded_img_path.replace("#", "%23"),
                               scores=answers)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run("0.0.0.0")
