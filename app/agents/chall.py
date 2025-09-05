from .base_agent import *
import os
from rag.retriever import get_relevant_documents
from openai import OpenAI
class chall_agent(BaseAgent):
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
    def do_reaserch(self,query):
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system",
                 "content": "你是一位经验丰富的心内科医生，请你对诊断假设列表进行分析，检查是否存在诊断误差并提出替代诊断。"},
                {"role": "user",
                 "content": f"以下是上一个医生的诊断假设列表: {query}\n\n请您对诊断假设列表进行分析，检查是否存在诊断误差并提出替代诊断。"},
                # {"role": "user", "content": f"请根据以下文档内容回答我的问题:\n\n{context_docs}\n\n我的问题是: {query}\n\n如果上下文的内容和提问的问题相关，你就从上下文中提取总结答案，否则你就按照自己的经验总结答案，注意你的回答不要引用文档内容，只需要参考回答即可"},
            ],
            stream=False
        )
        answer_1 = response.choices[0].message.content
        #print(answer_1)
        return answer_1