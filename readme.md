Cardiomind API 项目
简介
该项目提供了一个心血管疾病预测分析的API服务，支持通过RESTful接口进行疾病预测。

安装与运行
方式一：直接运行（Python环境）
安装依赖包：

bash
pip install -r requirements.txt
启动服务：

bash
python app/app.py
方式二：Docker运行
加载Docker镜像：

bash
docker load -i cardiomind-api.tar
运行容器：

bash
docker run -d --name cardiomind-container -p 8080:8080 -e HF_ENDPOINT=https://hf-mirror.com cardiomind-api
API使用示例
使用curl测试API接口：

bash
curl -X POST "http://localhost:8080/cardiomind" -H "Content-Type: application/json" --data-binary "@case1.json"
注意事项
确保端口8080未被其他程序占用

case1.json文件应放在当前工作目录中

如需使用其他HF endpoint，可通过修改HF_ENDPOINT环境变量实现
