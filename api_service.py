# -*- coding: utf-8 -*-
import os

import numpy as np
# -*- coding: utf-8 -*-
from PIL import Image
from flask import Flask, request, render_template

import config
import es_utils
import feature_extractor
import oss_utils

'''
    以图搜图服务
'''

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# 搜索图片
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        file = request.files['query_img']

        # 临时将图片存储在本地
        img = Image.open(file.stream)
        uploaded_img_path = "static/uploaded/" + file.filename
        img.save(uploaded_img_path)

        query = feature_extractor.fe.extract(uploaded_img_path)
        query = np.array(query).flatten()
        answers = es_utils.es.feature_search(query)

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

            # 暂存图片
            img = Image.open(file.stream)
            uploaded_img_path = config.root_path + '/static/uploaded/' + file.filename
            img.save(uploaded_img_path)

            feature = feature_extractor.fe.extract(uploaded_img_path)
            feature = np.array(feature).flatten()

            # 上传到OSS，返回图片地址   test前不能加 /
            resp = oss_utils.oss_utils.upload("test/" + name, config.root_path + '/static/uploaded/' + name).resp
            img_url = resp.response.url.replace("%2F", "/")

            # 上传es
            doc = {'name': name, 'feature': feature, 'url': img_url}
            es_utils.es.index(config.elasticsearch_index, body=doc)  # 保存到elasticsearch

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
