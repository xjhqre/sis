from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import numpy as np
import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from torch.autograd import Variable
from PIL import Image
import time

# See https://keras.io/api/applications/ for details


# 预处理操作
to_tensor = transforms.Compose([transforms.Resize((256, 256), 2),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
                                ])

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# load model
model = models.resnet50(pretrained=False)
load_checkpoint = "E:/resnet50-19c8e357.pth"
state_dict = torch.load(load_checkpoint, map_location=lambda storage, loc: storage)
model.load_state_dict(state_dict)
model.eval()


class FeatureExtractor:
    # def __init__(self):
    #     # base_model = MODEL.VGG16()
    #     base_model = VGG16(weights='imagenet')
    #     self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

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
    #     return feature / np.linalg.norm(feature)  # Normalize

    def exfeature(self, img):
        img = img.convert("RGB")
        features = list(model.children())[:-2]  # 去掉池化层及全连接层
        # print(list(model.children())[:-2])
        modelout = nn.Sequential(*features).to(device)

        img_tensor = to_tensor(img).unsqueeze(0).to(device, torch.float)
        out = modelout(img_tensor)
        out = out.reshape(-1)[::98]
        out = out.detach().numpy()
        return out
