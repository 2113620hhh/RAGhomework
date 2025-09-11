pip install -r requirements.txt
python app/app.py
命令行：curl -X POST "http://localhost:8080/cardiomind" -H "Content-Type: application/json" --data-binary "@case1.json"
docker使用
1.加载docker镜像cardiomind-api
2.生成容器cardiomind-container
3.docker run -d --name cardiomind-container  -p 8080:8080 -e HF_ENDPOINT=https://hf-mirror.com cardiomind-api
4.curl -X POST "http://localhost:8080/cardiomind" -H "Content-Type: application/json" --data-binary "@case1.json"

