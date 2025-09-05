# main.py
from rag.retriever import get_relevant_documents
import os
from openai import OpenAI

client = OpenAI(api_key="sk-612777a34f24424abc5b145427f9b440", base_url="https://api.deepseek.com")
#
# 提取文档内容并格式化
def format_docs_for_llm(docs):
    formatted_content = ""

    for i, doc in enumerate(docs):
        # 添加文档标题或标识
        formatted_content += f"【文档 {i + 1}】\n"

        # 添加文档内容（可以根据需要截取长度）
        formatted_content += f"{doc.page_content}\n\n"

        # 如果需要，也可以添加元数据信息
        # if hasattr(doc, 'metadata') and doc.metadata:
        #     formatted_content += f"元数据: {doc.metadata}\n\n"

    return formatted_content





corpus_path = "./corpus"
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
query = "一个高龄患了冠心病，他今年很大岁数了，该怎么治疗最合理"
docs = get_relevant_documents(query)

print(docs)
# 格式化文档内容
context_docs = format_docs_for_llm(docs)
print("格式化后的文档内容:")
print(context_docs)

# 然后将这些内容与你的问题一起发送给LLM

#
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一位经验丰富的心内科医生，请根据提供的文档内容回答问题。"},
        {"role": "user", "content": f"请根据以下文档内容回答我的问题:\n\n{context_docs}\n\n我的问题是: {query}\n\n从上下文中提取总结答案，注意你的回答不要引用文档内容，只需要参考回答即可"},
        #{"role": "user", "content": f"请根据以下文档内容回答我的问题:\n\n{context_docs}\n\n我的问题是: {query}\n\n如果上下文的内容和提问的问题相关，你就从上下文中提取总结答案，否则你就按照自己的经验总结答案，注意你的回答不要引用文档内容，只需要参考回答即可"},
    ],
    stream=False
)
print(response.choices[0].message.content)