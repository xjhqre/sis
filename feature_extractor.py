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
