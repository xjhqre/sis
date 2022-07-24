import glob
import os

from PIL import Image
from elasticsearch import Elasticsearch

from feature_extractor import FeatureExtractor

es = Elasticsearch([{'host': '', 'port': 9200}], timeout=3600)  # 修改这里
types = [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]
errorPaths = []  # 存放提取错误的图片路径

if __name__ == '__main__':
    fe = FeatureExtractor()
    trainPath = glob.glob('./static/img/*')  # 被检索的图片路径
    cnt = 0

    for i, image in enumerate(trainPath):
        (filename, extension) = os.path.splitext(image)
        if extension not in types:
            print("格式出错：" + image)
            errorPaths.append(image)
            continue

        try:
            feature = fe.extract(img=Image.open(image))
            feature = feature[::4]
            # print(feature.tolist().__str__())
        except Exception as e:
            print("出现异常：" + str(e))
            errorPaths.append(image)
        else:
            name = image.rsplit("\\")[1]
            imgUrl = "./static/img/" + image.rsplit("\\")[1]
            doc = {'url': imgUrl, 'feature': feature,
                   'name': name}

            es.index("imgsearch", body=doc)  # 保存到elasticsearch

            cnt += 1
            print("当前图片：" + imgUrl + " ---> " + str(cnt))

    if len(errorPaths) != 0:
        print("Error: 提取失败的图片路径：")
        for image in errorPaths:
            print(image)
