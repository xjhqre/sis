import glob

import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image


class FeatureExtractor:
    def __init__(self):
        base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')
        x = base_model.output
        x = Dense(1024, activation='relu')(x)  # 添加一个全连接层，将图片维度映射为1024
        self.model = Model(inputs=base_model.input, outputs=x)

    def extract(self, img):
        img = img.resize((224, 224))
        img = img.convert('RGB')
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        feature = self.model.predict(x)
        return feature.flatten()

    def extract_batch(self, img_folder_path, batch_size=32):
        result = []
        # 获取图片路径生成器
        img_path_list_generator = get_file_paths(img_folder_path, batch_size)
        for img_path_list in img_path_list_generator:
            for i, img_path in enumerate(img_path_list):
                # 如果剩余图片数量小于batch_size，batch_size的值设置为剩余的图片数量
                batch_size = batch_size if len(img_path_list) > batch_size else len(img_path_list)
                # 创建一个空的数组用于存储图像数据
                batch_images = np.zeros(
                    (batch_size, 224, 224, 3))

                img = image.load_img(img_path, target_size=(224, 224))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                x = preprocess_input(x)
                batch_images[i % batch_size] = x  # 将图像添加到批次数组中
                if (i + 1) % batch_size == 0:
                    # 当达到批量处理大小时或者是最后一张图像时进行处理
                    embeddings = self.model.predict(batch_images)  # 执行特征提取
                    print(embeddings.shape)
                    for j in range(embeddings.shape[0]):
                        img_features = embeddings[j]
                        result.append(img_features)
        return len(result)


def get_file_paths(img_folder_path, batch_size):
    img_path_list = glob.glob(img_folder_path + "/*")
    for i in range(0, len(img_path_list), batch_size):
        yield img_path_list[i:i + batch_size]


fe = FeatureExtractor()
