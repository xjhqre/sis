import glob
import os
import shutil

import torch
from PIL import Image
from elasticsearch import Elasticsearch
from transformers import CLIPModel, CLIPProcessor

import config

model_name_or_path = ""
if os.path.exists(config.model_path if config.model_path is not None else ""):
    model_name_or_path = config.model_path
else:
    model_name_or_path = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name_or_path)
processor = CLIPProcessor.from_pretrained(model_name_or_path)

es = Elasticsearch([{'host': config.elasticsearch_url, 'port': config.elasticsearch_port}], timeout=3600)


# 提取特征方法
def extract(img_path):
    inputs = processor(text=None, images=Image.open(img_path), return_tensors="pt", padding=True)
    # 嵌入图像
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
    return image_features


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


# 扫描本地文件夹图片，提取特征上传es
if __name__ == '__main__':
    trainPath = glob.glob(config.train_pic_path)  # 被检索的图片路径
    cnt = 0

    for i, image in enumerate(trainPath):
        (filename, extension) = os.path.splitext(image)
        if extension == 'ini':
            continue
        elif extension not in config.types:
            print("格式出错：" + image)
            errorImg.append(image)
            moveFile(image, errorPath)
            continue

        try:
            feature = extract(image)
        except Exception as e:

            print("出现异常：" + str(e))
            errorImg.append(image)
            moveFile(image, errorPath)
        else:
            name = image.rsplit("\\")[1]
            imgUrl = config.pic_url + image.rsplit("\\")[1]  # OSS

            doc = {'url': imgUrl, 'feature': feature,
                   'name': name}

            es.index(config.elasticsearch_index, body=doc)  # 保存到elasticsearch

            cnt += 1
            print("当前图片：" + imgUrl + " ---> " + str(cnt))

    if len(errorImg) != 0:
        print("Error: 提取失败的图片路径：")
        for image in errorImg:
            print(image)
