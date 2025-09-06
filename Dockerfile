# 使用指定版本的 Python 基础镜像
FROM python:3.10.18-slim

# 设置工作目录为 /code（避免与项目中的 app 文件夹冲突）
WORKDIR /code

# 复制整个项目到容器中
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8080

# 设置启动命令
CMD ["python", "app/app.py"]
