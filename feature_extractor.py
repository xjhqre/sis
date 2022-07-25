from keras_applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

from tensorflow.python import keras
from tensorflow.python.keras.backend import set_session

import tensorflow as tf
from numpy import linalg as LA

# See https://keras.io/api/applications/ for details


class FeatureExtractor:
    def __init__(self):
        # base_model = MODEL.VGG16()
        # base_model = VGG16(weights='imagenet')
        # self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

        # Milvus
        self.session = tf.compat.v1.Session()
        set_session(self.session)
        self.graph = tf.compat.v1.get_default_graph()
        self.model = ResNet50(
            weights='imagenet',
            include_top=False,
            pooling='avg',
            backend=keras.backend,
            layers=keras.layers,
            models=keras.models,
            utils=keras.utils
        )

    # def extract(self, img):
    #     """
    #     Extract a deep feature from an input image
    #     Args:
    #         img: from PIL.Image.open(path) or tensorflow.keras.preprocessing.image.load_img(path)
    #
    #     Returns:
    #         feature (np.ndarray): deep feature with the shape=(4096, )
    #     """
    #     img = img.resize((224, 224))  # VGG must take a 224x224 img as an input
    #     img = img.convert('RGB')  # Make sure img is color
    #     x = image.img_to_array(img)  # To np.array. Height x Width x Channel. dtype=float32
    #     x = np.expand_dims(x, axis=0)  # (H, W, C)->(1, H, W, C), where the first elem is the number of img
    #     x = preprocess_input(x)  # Subtracting avg values for each pixel
    #     feature = self.model.predict(x)[0]  # (1, 4096) -> (4096, )
    #     feature = feature / np.linalg.norm(feature)
    #     return feature[::4]  # Normalize

    def execute(self, img_path):
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        with self.graph.as_default():
            with self.session.as_default():
                features = self.model.predict(x)
                norm_feature = features[0] / LA.norm(features[0])
                norm_feature = [i.item() for i in norm_feature]
                return norm_feature[::2]
