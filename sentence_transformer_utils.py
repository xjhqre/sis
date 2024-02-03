import glob
import os
import pickle
import time

import torch
from PIL import Image
from sentence_transformers import SentenceTransformer, util
from src.config import config
from src.config.config import config_instance
from src.exception.no_feature_file_exception import NoFeatureFileException
from src.exception.no_feature_path_exception import NoFeaturePathException

torch.set_num_threads(4)

model_name_or_path = ""
if os.path.exists(config.model_path):
    model_name_or_path = config.model_path
else:
    model_name_or_path = "clip-ViT-B-32"
model = SentenceTransformer(model_name_or_path)


# 存储张量
def dump(img_names, img_emb):
    if not os.path.exists(config_instance.get_feature_path()):
        os.makedirs(config_instance.get_feature_path())
    with open(config_instance.get_feature_path() + str(int(time.time())) + ".pickle", 'wb') as fOut:
        pickle.dump((img_names, img_emb), fOut)


# 提取特征方法
def extract(img_path):
    img = Image.open(img_path)
    emb = model.encode([img], batch_size=1, convert_to_tensor=True, show_progress_bar=False)
    img.close()
    return emb


# 搜索图片
def search(query, k=None):
    # 默认参数值是在函数定义时计算的，而不是在运行时计算的
    if k is None:
        k = int(config_instance.get_result_count())
    if not os.path.exists(config_instance.get_feature_path()):
        raise NoFeaturePathException

    img_names = []
    img_emb = None
    feature_list = list(glob.glob(config_instance.get_feature_path() + "*"))
    if len(feature_list) == 0:
        raise NoFeatureFileException

    for feature_path in feature_list:
        with open(feature_path, 'rb') as fIn:
            names, emb = pickle.load(fIn)
            img_names.extend(names)
            if img_emb is None:
                img_emb = emb
            else:
                img_emb = torch.concat((img_emb, emb), dim=0)

    img = Image.open(query)
    query_emb = model.encode([img], batch_size=1, convert_to_tensor=True, show_progress_bar=False)
    img.close()

    hits = util.semantic_search(query_emb, img_emb, top_k=k)[0]

    return [img_names[hit['corpus_id']] for hit in hits]
