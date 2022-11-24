# 本地以图搜图
在原项目上进行了一定修改，神经网络改用 resnet50。向量检索改用 elasticsearch，图片向量数据直接存储在 elasticsearch，并用其内置向量检索算法匹配图片，不在需要 .npy 文件。图片存储在阿里云OSS

elasticsearch 索引构建请参考 elasticsearch.txt 文件

在 config.py 中修改配置