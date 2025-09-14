
from coord_agent import *
coord_agent=coord_agents()
import json
# 构建JSON文件的完整路径
json_file_path = os.path.join('..','medical_records', 'case1.json')  # 替换为你的实际文件名

# 读取JSON文件内容
with open(json_file_path, 'r', encoding='utf-8') as f:
    json_content = json.load(f)

# 提取"medical record"字段的内容作为查询字符串
query = json_content["medical record"]


#query="我这几天头有点疼"

ans1,ans2,ans3=coord_agent.do_job(query,"../corpus")
print("你好，我是第一个医生！")
print(ans1)
print("你好，我是第二个医生！")
print(ans2)
print("你好，我是第三个医生！")
print(ans3)

