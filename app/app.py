from flask import Flask, request, jsonify, Response
import json
import os
import re
import logging
from coord_agent import *

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# 初始化代理
coord_agent = coord_agents()
clin_agent_instance = clin_agent()


def extract_json_from_response(response_text):
    """
    从响应文本中提取 JSON 内容
    """
    # 如果已经是字典，直接返回
    if isinstance(response_text, dict):
        return response_text

    # 尝试直接解析为 JSON
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass

    # 尝试提取 Markdown 代码块中的 JSON（支持多种格式）
    patterns = [
        r'```json\s*(\{.*\})\s*```',  # ```json {content} ```
        r'```\s*(\{.*\})\s*```',  # ``` {content} ```
        r'^(\{.*\})$'  # 纯JSON字符串
    ]

    for pattern in patterns:
        json_match = re.search(pattern, response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                continue

    # 如果以上都失败，返回原始文本作为诊断结果
    return {"diagnosis": response_text}

@app.route('/cardiomind', methods=['POST'])
def process_medical_record():
    try:
        # 获取请求中的JSON数据
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # 提取医疗记录
        medical_record = data.get("medical record", "")
        if not medical_record:
            return jsonify({"error": "No medical record found in request"}), 400

        # 使用coord_agent获取三个医生的诊断
        ans1, ans2, ans3 = coord_agent.do_job(medical_record, "../corpus")
        diagnosis_json = extract_json_from_response(ans3)
        # 尝试解析返回的JSON
        try:
            ans = json.loads(ans3)
            #return jsonify(diagnosis_json)
            # 使用 json.dumps 并设置 ensure_ascii=False 来确保中文正确显示
            response_json = json.dumps(diagnosis_json, ensure_ascii=False, indent=2)

            # 创建 Response 对象并设置正确的 MIME 类型和字符集
            response = Response(
                response=response_json,
                status=200,
                mimetype='application/json; charset=utf-8'
            )


            return response
            #return ans
            #response_json = json.dumps(diagnosis_json, ensure_ascii=False, indent=2)
            #return Response(response_json, mimetype='application/json; charset=utf-8')
        except json.JSONDecodeError:
            # 如果返回的不是JSON，直接返回文本
            return jsonify({"diagnosis": ans3})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=8080, debug=True)
    import sys
    import codecs

    if sys.stdout.encoding != 'UTF-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    if sys.stderr.encoding != 'UTF-8':
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    logger.info("启动 Flask 服务器...")
    app.run(host='0.0.0.0', port=8080, debug=True)