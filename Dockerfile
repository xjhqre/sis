# Dockerfile 指令
# 基于 基础镜像
FROM python:3.7.16

# 将构建环境下的文件OR目录, 复制到镜像中的/code目录下,
ADD . /app

# 设置/切换 当前工作目录 为 /code
WORKDIR /app

# 根据需要, 定义 环境变量
ENV AccessKeyId 你的AccessKeyId
ENV AccessKeySecret 你的AccessKeySecret
ENV elasticsearch_url 你的elasticsearch_url
ENV elasticsearch_port 9200

# 安装python环境支持(针对python项目)
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露出外界访问容器的端口
EXPOSE 5000

CMD ["python", "api_service.py"]
