import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from flask import Flask, request, render_template
from pathlib import Path
from offline import featurePath
from offline import trainPath

app = Flask(__name__)

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
img_names = []
for feature_path in Path(featurePath).glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path(trainPath) / feature_path.stem.replace("#", "%23"))
    img_names.append(feature_path.stem)
features = np.array(features)


def description_search(query):
    global es
    results = es.search(
        index="desearch",
        body={
            "size": 30,
            "query": {
                "match": {"description": query}
            }
        })
    hitCount = results['hits']['total']
    print(results)

    if hitCount > 0:
        if hitCount is 1:
            print(str(hitCount), ' result')
        else:
            print(str(hitCount), 'results')
        answers = []
        max_score = results['hits']['max_score']

        if max_score >= 0.35:
            for hit in results['hits']['hits']:
                if hit['_score'] > 0.5 * max_score:
                    desc = hit['_source']['description']
                    imgurl = hit['_source']['imgurl']
                    name = hit['_source']['name']
                    answers.append([imgurl, desc, name])
    else:
        answers = []
    return answers


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        print(file.filename)
        uploaded_img_path = "static/uploaded/" + file.filename
        print(uploaded_img_path)
        img.save(uploaded_img_path)

        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features - query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:30]  # Top 30 results
        # scores返回结果，依次包含：图片相似度（越接近0就越相似）、图片路径（含名称）、图片名称
        scores = [(dists[id], img_paths[id], img_names[id]) for id in ids]

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run("0.0.0.0")
