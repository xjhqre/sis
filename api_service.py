# -*- coding: utf-8 -*-
import os
import sys

import numpy as np
# -*- coding: utf-8 -*-
import oss2
from PIL import Image
from elasticsearch import Elasticsearch
from flask import Flask, request, render_template

import config
import sentence_transformer_utils

'''
    以图搜图服务
'''

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# es连接
es = Elasticsearch([{'host': config.elasticsearch_url, 'port': config.elasticsearch_port}], timeout=10000)

# 检查是否成功连接
if es.ping():
    print("elasticsearch连接成功")
else:
    print("elasticsearch连接失败")
    sys.exit()

# 阿里云OSS
# 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
auth = oss2.Auth(config.AccessKeyId, config.AccessKeySecret)
# yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
# 填写Bucket名称。
bucket = oss2.Bucket(auth, config.EndPoint, config.bucket)


def feature_search(query):
    global es
    print(query.size)
    results = es.search(
        index=config.elasticsearch_index,
        body={
            "size": config.result_count,
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
    return render_template('index.html')


# 搜索图片
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        file = request.files['query_img']

        # Save query image
        img = Image.open(file.stream)  # PIL image
        # print(file.filename)
        uploaded_img_path = "static/uploaded/" + file.filename
        # print(uploaded_img_path)
        img.save(uploaded_img_path)

        # Run search
        query = sentence_transformer_utils.extract(uploaded_img_path)
        query = np.array(query).flatten()
        answers = feature_search(query)

        # 删除本地图片
        if os.path.exists(uploaded_img_path):
            os.remove(uploaded_img_path)
        else:
            print('删除图片失败:', uploaded_img_path)

        return render_template('index.html',
                               query_path=uploaded_img_path.replace("#", "%23"),
                               scores=answers)
    else:
        return render_template('index.html')


# 上传图片
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for file in request.files.getlist('upload_img'):
            name = file.filename

            # Save query image
            img = Image.open(file.stream)  # PIL image
            # print(file.filename)
            uploaded_img_path = config.root_path + '/static/uploaded/' + file.filename
            # print(uploaded_img_path)
            img.save(uploaded_img_path)

            feature = sentence_transformer_utils.extract(uploaded_img_path)
            feature = np.array(feature).flatten()

            # 上传到OSS，返回图片地址   test前不能加 /
            resp = bucket.put_object_from_file("test/" + name, config.root_path + '/static/uploaded/' + name).resp

            imgUrl = resp.response.url.replace("%2F", "/")

            # 上传es
            doc = {'name': name, 'feature': feature, 'url': imgUrl}
            es.index(config.elasticsearch_index, body=doc)  # 保存到elasticsearch

            # 删除本地图片
            if os.path.exists(uploaded_img_path):
                os.remove(uploaded_img_path)
            else:
                print('删除图片失败:', uploaded_img_path)

        return render_template('index.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
