# 本地以图搜图
在原项目上进行了一定修改，神经网络改用 resnet50。向量检索改用 elasticsearch，图片向量数据直接存储在 elasticsearch，并用其内置向量检索算法匹配图片，不在需要 .npy 文件。图片存储在阿里云OSS

elasticsearch 索引构建请参考 elasticsearch.txt 文件

在 config.py 中修改配置

## 使用说明
安装 elasticsearch7.2 版本或以上

开通阿里云OSS

配置 config.py

offline.py：训练本地文件夹里的图片，上传到阿里云OSS和elasticsearch

searchService.py：flask服务，支持以图搜搜和图片上传功能