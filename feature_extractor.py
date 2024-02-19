import glob
import os
import time

import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing import image

import config
import es_utils
from oss_utils import ou


def imageProcess(img_path):
    """
    图片处理
    :param str img_path: 图片路径
    :return: <class 'PIL.Image.Image'>
    """
    img = image.load_img(img_path, target_size=(224, 224))
    img = img.resize((224, 224))
    img = img.convert('RGB')
    return img


def get_file_paths(img_folder_path, batch_size):
    """
    获取图片路径
    :param str img_folder_path: 图片文件夹路径
    :param int batch_size: 每次获取数量
    :return: list 图片路径列表
    """
    img_path_list = glob.glob(img_folder_path + "/*")
    for i in range(0, len(img_path_list), batch_size):
        yield img_path_list[i:i + batch_size]


class FeatureExtractor:
    def __init__(self):
        self.model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

    def extract(self, img_path):
        img = imageProcess(img_path)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        feature = self.model.predict(x)
        return feature.flatten()[::2]  # 维度 2048 -> 1024

    def extract_batch(self, img_folder_path, batch_size=32):
        batch_size_copy = batch_size
        cnt = 0  # 图片计数
        time_start = time.time()
        # 获取图片路径生成器
        img_path_list_generator = get_file_paths(img_folder_path, batch_size)
        for img_path_list in img_path_list_generator:
            # 过滤掉非图片类型的文件
            img_path_list = [name for name in img_path_list if
                             os.path.splitext(name)[1] in config.types]

            # 如果剩余图片数量小于batch_size，batch_size的值设置为剩余的图片数量
            if len(img_path_list) < batch_size:
                batch_size = len(img_path_list)
            else:
                batch_size = batch_size_copy

            # 创建一个空的数组用于存储图像数据
            batch_images = np.zeros(
                (batch_size, 224, 224, 3))

            cnt += len(img_path_list)

            for i, img_path in enumerate(img_path_list):
                img = imageProcess(img_path)
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                x = preprocess_input(x)
                batch_images[i % batch_size] = x  # 将图像添加到批次数组中

            # 当达到批量处理大小时或者是最后一张图像时进行处理
            embeddings = self.model.predict(batch_images)  # 执行特征提取
            for j in range(embeddings.shape[0]):
                feature = embeddings[j][::2]  # 维度 2048 -> 1024
                # 上传到OSS，返回图片地址   test是文件夹 前面不能加 /
                # TODO 上传 oss 耗时较高
                resp = ou.upload("test/" + os.path.basename(img_path_list[j]), img_path_list[j])
                img_url = resp.response.url.replace("%2F", "/")

                # 上传es
                doc = {'name': os.path.basename(img_path_list[j]), 'feature': feature, 'url': img_url}
                es_utils.es.index(config.elasticsearch_index, body=doc)  # 保存到elasticsearch

        time_end = time.time()
        time_sum = time_end - time_start
        print("提取结束，提取成功图片: {} 张 总耗时: {} 秒\n".format(
            cnt, time_sum))


fe = FeatureExtractor()

if __name__ == '__main__':
    fe.extract_batch(r"F:\ACG\壁纸")
