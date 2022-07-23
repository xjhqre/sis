import os

from PIL import Image
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np

trainPath = "./static/img"  # 被检索的图片路径
featurePath = "./static/feature"  # 存放被检索图片的特征

es = Elasticsearch([{'host': '1.15.88.204', 'port': 9200}], timeout=3600)
types = [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]
errorPaths = []  # 存放提取错误的图片路径

if __name__ == '__main__':
    fe = FeatureExtractor()

    cnt = 0
    actions = []

    for img_path in sorted(Path(trainPath).glob("*.*")):
        if img_path.suffix not in types:
            errorPaths.append(img_path)
            continue


        try:
            feature = fe.extract(img=Image.open(img_path))
        except Exception as e:
            print("出现异常：" + str(e))
            errorPaths.append(img_path)
        else:
            cnt += 1
            print("当前图片：" + print(img_path) + " ---> " + str(cnt))
            doc = {'imgurl': image, 'description': cap, 'name': name}
            actions.append(doc)
            feature_path = Path(featurePath) / (img_path.name + ".npy")
            np.save(feature_path, feature)


    if len(errorPaths) != 0:
        print("Error: 提取失败的图片路径：")
        for img_path in errorPaths:
            print(img_path)
