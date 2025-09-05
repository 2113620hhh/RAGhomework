# agents/challenger_agent.py
from .base_agent import BaseAgent
from typing import Dict, Any, List
from langchain.schema import Document
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import re


class ChallengerAgent(BaseAgent):
    """Dr.Challenger: 对诊断假设进行分析，检查诊断误差并提出替代诊断"""

    def __init__(self, rag_retriever):
        super().__init__(
            "Dr.Challenger",
            "对诊断假设列表进行分析，检查诊断误差并提出替代诊断"
        )
        self.rag_retriever = rag_retriever
        self.llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")

        # 定义提示模板
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """你是一位严谨的心内科医生Dr.Challenger。你的任务是对诊断假设进行批判性分析。

            可参考的医学知识：
            {context}

            请遵循以下步骤：
            1. 分析每个诊断假设的合理性和证据支持
            2. 识别可能的诊断误差或遗漏
            3. 提出替代诊断或补充检查建议
            4. 评估不同诊断假设的相对可能性

            输出格式要求：
            {{
                "challenges": [
                    {{
                        "hypothesis_index": 0,
                        "critique": "对假设的批评分析",
                        "alternative_suggestions": ["替代诊断1", "替代诊断2"],
                        "confidence_adjustment": "提高/降低/维持"
                    }}
                ],
                "overall_assessment": "总体评估"
            }}"""),
            ("human", "患者病历信息：{medical_record}\n\n诊断假设：{hypotheses}")
        ])

        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def process(self, input_data: Dict[str, Any], context: List[Document] = None) -> Dict[str, Any]:
        """对诊断假设进行分析和挑战"""
        medical_record = input_data.get("medical_record", "")
        hypotheses = input_data.get("hypotheses", [])

        # 使用RAG检索相关医学知识
        if context is None:
            # 从诊断假设中提取关键词进行检索
            keywords = self._extract_keywords_from_hypotheses(hypotheses)
            context = self.rag_retriever(keywords)

        # 准备上下文信息
        context_text = "\n".join([doc.page_content for doc in context[:3]])  # 只使用前3个最相关的文档

        # 调用LLM进行分析
        result = self.chain.invoke({
            "context": context_text,
            "medical_record": medical_record,
            "hypotheses": json.dumps(hypotheses, ensure_ascii=False)
        })

        # 解析结果
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            # 如果解析失败，尝试提取JSON部分
            try:
                json_match = re.search(r'\{.*\}', result, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                return {"raw_output": result}
            except:
                return {"raw_output": result}

    def _extract_keywords_from_hypotheses(self, hypotheses: List[Dict]) -> str:
        """从诊断假设中提取关键词用于检索"""
        keywords = []
        for hypothesis in hypotheses:
            condition = hypothesis.get("condition", "")
            reasoning = hypothesis.get("reasoning", "")
            keywords.append(condition)

            # 从理由中提取关键词
            medical_terms = ["鉴别诊断", "并发症", "风险因素", "治疗方案", "诊断依据"]
            for term in medical_terms:
                if term in reasoning:
                    keywords.append(term)

        return " ".join(keywords) if keywords else "心内科诊断鉴别"