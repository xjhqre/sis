# 本地以图搜图

框架使用 sentence_transformers

模型使用 clip-ViT-B-32

图片特征向量直接存储在 elasticsearch，版本7.4.2

图片存储在阿里云OSS

elasticsearch 索引构建请参考 elasticsearch.txt 文件

## 使用说明

1、在启动配置中添加以下四个参数

![1](README.assets/1.png)

![14](README.assets/14.png)

2、运行api_service.py文件即可

## 提示

不保证上传图片名称唯一，请确认上传图片名称不重复，防止覆盖