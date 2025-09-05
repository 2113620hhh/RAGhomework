from .base_agent import BaseAgent
import os
from rag.retriever import get_relevant_documents
from openai import OpenAI

#client = OpenAI(api_key="sk-612777a34f24424abc5b145427f9b440", base_url="https://api.deepseek.com")
#client = OpenAI(api_key="sk-612777a34f24424abc5b145427f9b440", base_url="https://api.deepseek.com")

def format_docs_for_llm(docs):
    formatted_content = ""

    for i, doc in enumerate(docs):
        # 添加文档标题或标识
        formatted_content += f"【文档 {i + 1}】\n"
        formatted_content += f"{doc.page_content}\n\n"

    return formatted_content

class hyp_agent(BaseAgent):
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
        return self.do_reaserch(input_data)
    def do_reaserch(self,query,corpus_path):
        #corpus_path = "../corpus"
        if os.path.exists(corpus_path):
            files = os.listdir(corpus_path)
            print(f"语料库中的文件: {files}")

            # 读取并显示文件内容（前200字符）
            for file in files:
                if file.endswith('.txt'):
                    with open(os.path.join(corpus_path, file), 'r', encoding='utf-8') as f:
                        content = f.read(200)  # 只读取前200个字符
                        print(f"{file} 内容预览: {content}...")
        else:
            print("语料库目录不存在")

        print("查询结果")
        #query = "一个高龄患了冠心病，他今年很大岁数了，该怎么治疗最合理"
        docs = get_relevant_documents(query)

        print(docs)
        # 格式化文档内容
        context_docs = format_docs_for_llm(docs)
        print("格式化后的文档内容:")
        print(context_docs)

        # 然后将这些内容与你的问题一起发送给LLM

        #
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位经验丰富的心内科医生，请根据提供的文档内容回答问题,根据患者病历信息生成生成诊断假设列表。"},
                {"role": "user",
                 "content": f"请根据以下文档内容回答我的问题:\n\n{context_docs}\n\n我的问题是: {query}\n\n从上下文中提取总结答案，注意你的回答不要引用文档内容，只需要参考回答即可"},
                # {"role": "user", "content": f"请根据以下文档内容回答我的问题:\n\n{context_docs}\n\n我的问题是: {query}\n\n如果上下文的内容和提问的问题相关，你就从上下文中提取总结答案，否则你就按照自己的经验总结答案，注意你的回答不要引用文档内容，只需要参考回答即可"},
            ],
            stream=False
        )
        answer_1=response.choices[0].message.content
        #print(answer_1)
        return answer_1