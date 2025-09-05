from .vector_store import get_vector_store
import  os
# 初始化向量数据库
# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取项目根目录（rag目录的上一级）
project_root = os.path.dirname(current_dir)
# 构建正确的 corpus 路径
corpus_path = os.path.join(project_root, "corpus")
vector_store = get_vector_store(corpus_path)

#vector_store = get_vector_store("./corpus")

def get_relevant_documents(query, k=4):
    """获取相关文档"""
    return vector_store.similarity_search(query, k=k)