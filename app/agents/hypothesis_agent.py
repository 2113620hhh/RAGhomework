# agents/hypothesis_agent.py
from .base_agent import BaseAgent
from typing import Dict, Any, List
from langchain.schema import Document
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import re



class HypothesisAgent(BaseAgent):
    """Dr.Hypothesis: 根据患者病历生成诊断假设列表"""

    def __init__(self, rag_retriever):
        super().__init__(
            "Dr.Hypothesis",
            "根据患者病历信息生成诊断假设列表"
        )
        self.rag_retriever = rag_retriever
        self.llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo")

        # 定义提示模板
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """你是一位经验丰富的心内科医生Dr.Hypothesis。你的任务是根据患者病历信息生成可能的诊断假设列表。

            可参考的医学知识：
            {context}

            请遵循以下步骤：
            1. 分析患者病历中的关键信息
            2. 基于心内科知识生成可能的诊断假设
            3. 按可能性从高到低排序
            4. 为每个假设提供简要理由

            输出格式要求：
            {{
                "hypotheses": [
                    {{
                        "condition": "疾病名称",
                        "confidence": "高/中/低",
                        "reasoning": "诊断理由"
                    }}
                ]
            }}"""),
            ("human", "患者病历信息：{medical_record}")
        ])

        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def process(self, input_data: Dict[str, Any], context: List[Document] = None) -> Dict[str, Any]:
        """处理患者病历，生成诊断假设"""
        medical_record = input_data.get("medical_record", "")

        # 使用RAG检索相关医学知识
        if context is None:
            # 从病历中提取关键词进行检索
            keywords = self._extract_keywords(medical_record)
            context = self.rag_retriever(keywords)

        # 准备上下文信息
        context_text = "\n".join([doc.page_content for doc in context[:3]])  # 只使用前3个最相关的文档

        # 调用LLM生成诊断假设
        result = self.chain.invoke({
            "context": context_text,
            "medical_record": medical_record
        })

        # 解析结果
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            # 如果解析失败，尝试提取JSON部分或返回原始结果
            try:
                # 尝试从文本中提取JSON
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                return {"raw_output": result}
            except:
                return {"raw_output": result}

    def _extract_keywords(self, medical_record: str) -> str:
        """从病历中提取关键词用于检索"""
        # 简单实现：提取医学术语和症状描述
        keywords = []

        # 添加一些常见心内科关键词
        cardiac_terms = ["胸痛", "心悸", "气短", "心电图", "心肌酶", "高血压", "冠心病", "心衰", "心律", "心绞痛"]
        for term in cardiac_terms:
            if term in medical_record:
                keywords.append(term)

        # 添加病历中的数字信息（如年龄、血压值等）
        numbers = re.findall(r'\d+', medical_record)
        keywords.extend(numbers)

        return " ".join(keywords) if keywords else "心内科常见疾病"
