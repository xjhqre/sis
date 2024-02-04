# Stage 1: Build environment
FROM python:3.7.16 as builder

WORKDIR /app

# Copy only the requirements file to install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Stage 2: Final environment
FROM python:3.7.16

WORKDIR /app

# Copy the built dependencies from the previous stage
COPY --from=builder /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy the rest of the application files
COPY . .

# Set environment variables
ENV AccessKeyId 你的AccessKeyId
ENV AccessKeySecret 你的AccessKeySecret
ENV elasticsearch_url 你的elasticsearch_url
ENV elasticsearch_port 9200
ENV model_path test

# Expose the port
EXPOSE 5000

CMD ["python", "api_service.py"]
