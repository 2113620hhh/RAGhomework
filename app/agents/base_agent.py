from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langchain.schema import Document
from rag.retriever import get_relevant_documents

class BaseAgent(ABC):
    """Agent基类，定义所有Agent的通用接口"""
    api_key="sk-612777a34f24424abc5b145427f9b440"
    base_url="https://api.deepseek.com"
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def process(self, input_data: Dict[str, Any], context: List[Document] = None) -> Dict[str, Any]:
        """处理输入数据并返回结果"""
        pass

    def __str__(self):
        return f"{self.name}: {self.description}"