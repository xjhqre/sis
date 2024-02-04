FROM python:3.7.16 as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

FROM python:3.7.16

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY . .

# 设置环境变量
ENV AccessKeyId 你的AccessKeyId
ENV AccessKeySecret 你的AccessKeySecret
ENV elasticsearch_url 你的elasticsearch_url
ENV elasticsearch_port 9200
ENV model_path test

EXPOSE 5000

CMD ["python", "api_service.py"]
