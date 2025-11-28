FROM python:3.9-slim

WORKDIR /dop-tools

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口（Flask默认端口5000）
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 启动应用
CMD ["flask", "run", "--host=0.0.0.0"]