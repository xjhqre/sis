# 本地以图搜图

框架使用 sentence_transformers

模型使用 clip-ViT-B-32

图片特征向量直接存储在 elasticsearch，版本7.4.2

图片存储在阿里云OSS

elasticsearch 索引构建请参考 elasticsearch.txt 文件

运行内存大约1.8G

## 使用说明

1、在启动配置中添加以下五个参数

* AccessKeyId：必填
* AccessKeySecret：必填
* elasticsearch_url：elasticsearch地址（必填）
* elasticsearch_port：elasticsearch端口（必填）
* model_path：模型地址（可选）

![1](README.assets/1.png)

![14](README.assets/14.png)

2、运行api_service.py文件即可

## 提示

不保证上传图片名称唯一，请确认上传图片名称不重复，防止覆盖

## docker

### 运行步骤

1、拉取镜像或者自己打包

```shell
docker pull xjhqre/sis:v1.0
```

```shell
docker build . -t xjhqre/sis:v1.0
```

2、运行容器

```shell
docker run -d -p 5000:5000 \
-e AccessKeyId=你的AccessKeyId \
-e AccessKeySecret=你的AccessKeySecret \
-e elasticsearch_url=你的elasticsearch_url \
-e elasticsearch_port=9200 \
-e model_path=你的模型地址(可选) \
--name sis xjhqre/sis:v1.0
```

3、访问 [127.0.0.1:5000](127.0.0.1:5000)

如果运行后报错模型下载不了，则在run指令中加上model_path参数，手动到
https://huggingface.co/sentence-transformers/clip-ViT-B-32/tree/main
下载所有文件，将文件夹复制到docker容器中，地址与model_path对应，例如-e model_path=/opt/model