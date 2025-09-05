from .base_agent import *
from openai import OpenAI
class clin_agent(BaseAgent):
    def __init__(self):
        """
        构造函数，初始化语料库路径
        :param corpus_path: 语料库路径，默认为上一级目录中的corpus文件夹
        """
        pass

    def process(self, input_data):
        """
        实现BaseAgent要求的抽象方法
        这里简单地将输入传递给do_reaserch方法
        """
        pass
    def ceshi(self):
        #base_ag=BaseAgent("ABC","12")
        print(self.api_key+self.base_url)
    def do_reaserch(self,query1,query2,ans):
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        # 构建严格的格式要求
        format_requirements = """
                【重要指令】
                你必须严格按照以下JSON格式输出诊断结果，不要添加任何额外的解释、注释或文本。
                只输出JSON对象，不要有任何其他内容。

                【输出格式】
                {
                  "患者信息": {
                    "年龄": "",
                    "性别": "",
                    "入院日期": ""
                  },
                  "临床表现": {
                    "主诉": "",
                    "现病史": ""
                  },
                  "病史信息": {
                    "既往史": "",
                    "个人史": "",
                    "婚育史": "",
                    "家族史": ""
                  },
                  "体格检查": "",
                  "辅助检查": "",
                  "诊断结果": {
                    "主要诊断": {
                      "名称": "",
                      "诊断依据": []
                    },
                    "次要诊断": [
                      {
                        "名称": "",
                        "诊断依据": []
                      }
                    ],
                    "鉴别诊断": []
                  },
                  "治疗方案": []
                }

                【特别强调】
                - 只输出JSON格式的内容，不要有任何其他文本
                - 确保所有字段都存在，即使某些字段可能为空
                - 严格按照上述结构组织数据
                - 诊断依据必须是数组格式，包含多个依据点
                - 次要诊断必须是数组，可能包含多个诊断
                - 治疗方案必须是数组，包含多个治疗建议
                """
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system",
                 "content": "你是一名资深的医学老教授，综合我给你之前两个医生的诊断信息完成诊断，生成符合要求格式的主/次要诊断和鉴别诊断。"},
                {"role": "user",
                 "content": f"以下分别是两个医生的初步诊断,这是患者的患病信息{ans}\n\n,这是第一个医生的诊断 {query1}\n\n，这是第二个医生的诊断{query2}\n\n,请您综合以上两个医生的诊断，生成符合要求格式的主/次要诊断和鉴别诊断。\n\n{format_requirements}\n\n请严格按照上述JSON格式输出，不要有任何其他文本。"},
                # {"role": "user", "content": f"请根据以下文档内容回答我的问题:\n\n{context_docs}\n\n我的问题是: {query}\n\n如果上下文的内容和提问的问题相关，你就从上下文中提取总结答案，否则你就按照自己的经验总结答案，注意你的回答不要引用文档内容，只需要参考回答即可"},
            ],
            stream=False
        )
        answer_1 = response.choices[0].message.content
        #print(answer_1)
        return answer_1