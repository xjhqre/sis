"""
以图搜图配置文件，批量处理
"""
import os

root_path = os.path.dirname(os.path.abspath(__file__))

# 批量提取图片路径
train_pic_path = 'F:/ACG/出处归档/*'

pic_url = "https://chuchu-xjhqre.oss-cn-hangzhou.aliyuncs.com/img/"

# 可搜索的图片类型
types = [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]

# 搜素相似图片返回数量
result_count = 30

# elasticsearch
elasticsearch_index = os.getenv("elasticsearch_index")
elasticsearch_url = os.getenv("elasticsearch_url")
elasticsearch_port = os.getenv("elasticsearch_port")

# OSS
AccessKeyId = os.getenv("AccessKeyId")
AccessKeySecret = os.getenv("AccessKeySecret")
EndPoint = os.getenv("EndPoint")
bucket = os.getenv("bucket")

# 模型地址
model_path = os.getenv("model_path")

if __name__ == '__main__':
    pass
