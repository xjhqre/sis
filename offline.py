import glob
import os
import shutil

from elasticsearch import Elasticsearch

from feature_extractor import FeatureExtractor

es = Elasticsearch([{'host': '1.15.88.204', 'port': 9200}], timeout=3600)
types = [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]
errorImg = []  # 存放提取错误的图片路径
errorPath = "static/error/"


def moveFile(srcfile, dstPath):  # 移动函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstPath):
            os.makedirs(dstPath)  # 创建路径
        shutil.move(srcfile, dstPath + fname)  # 移动文件
        print("move %s -> %s" % (srcfile, dstPath + fname))


if __name__ == '__main__':
    fe = FeatureExtractor()
    # trainPath = glob.glob('./static/img/*')  # 被检索的图片路径
    trainPath = glob.glob('F:/ACG/出处归档/*')  # 被检索的图片路径
    cnt = 0

    for i, image in enumerate(trainPath):
        (filename, extension) = os.path.splitext(image)
        if extension not in types:
            print("格式出错：" + image)
            errorImg.append(image)
            moveFile(image, errorPath)
            continue

        try:
            feature = fe.execute(image)
            # feature = fe.execute(img=Image.open(image))
            # feature = feature[::4]
        except Exception as e:
            print("出现异常：" + str(e))
            errorImg.append(image)
            moveFile(image, errorPath)
        else:
            name = image.rsplit("\\")[1]
            # imgUrl = "./static/img/" + image.rsplit("\\")[1]  # OSS
            imgUrl = "https://chuchu-xjhqre.oss-cn-hangzhou.aliyuncs.com/img/" + image.rsplit("\\")[1]  # OSS

            doc = {'url': imgUrl, 'feature': feature,
                   'name': name}

            es.index("imgsearch", body=doc)  # 保存到elasticsearch

            cnt += 1
            print("当前图片：" + imgUrl + " ---> " + str(cnt))

    if len(errorImg) != 0:
        print("Error: 提取失败的图片路径：")
        for image in errorImg:
            print(image)
