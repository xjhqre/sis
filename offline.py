import os

from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np

trainPath = "./static/img"  # 被检索的图片路径
featurePath = "./static/feature"  # 存放被检索图片的特征

types = [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]

errorPaths = []  # 存放提取错误的图片路径

if __name__ == '__main__':
    fe = FeatureExtractor()

    for img_path in sorted(Path(trainPath).glob("*.*")):
        if img_path.suffix not in types:
            continue
        print(img_path)

        try:
            feature = fe.extract(img=Image.open(img_path))
        except Exception:
            errorPaths.append(img_path)
        else:
            feature_path = Path(featurePath) / (img_path.name + ".npy")
            np.save(feature_path, feature)

    print("Error: 提取失败的图片路径：")
    for img_path in errorPaths:
        print(img_path)
