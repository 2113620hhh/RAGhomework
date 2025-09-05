# agents/reasoning_agent.py
from .base_agent import BaseAgent
from typing import Dict, Any, List
from langchain.schema import Document
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import re


class ReasoningAgent(BaseAgent):
    """Dr.Clinical-Reasoning: 综合信息完成诊断，生成主/次要诊断和鉴别诊断"""

    def __init__(self):
        super().__init__(
            "Dr.Clinical-Reasoning",
            "综合给出信息完成诊断，生成符合要求格式的主/次要诊断和鉴别诊断"
        )
        self.llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")

        # 定义提示模板
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """你是一位资深心内科医生Dr.Clinical-Reasoning。你的任务是综合所有信息生成最终诊断。

            请遵循以下步骤：
            1. 综合考虑患者病历、诊断假设和挑战分析
            2. 确定最可能的主诊断和次要诊断
            3. 列出需要鉴别的其他疾病
            4. 提供诊断依据和下一步检查建议

            输出格式必须严格按照以下JSON格式：
            {{
                "primary_diagnosis": {{
                    "condition": "主要诊断疾病名称",
                    "confidence": "高/中/低",
                    "reasoning": "诊断依据"
                }},
                "secondary_diagnoses": [
                    {{
                        "condition": "次要诊断疾病名称",
                        "confidence": "高/中/低",
                        "reasoning": "诊断依据"
                    }}
                ],
                "differential_diagnoses": [
                    {{
                        "condition": "需要鉴别的疾病名称",
                        "reasoning": "鉴别理由"
                    }}
                ],
                "next_steps": [
                    "建议的下一步检查或处理"
                ]
            }}"""),
            ("human", """患者病历信息：
            {medical_record}

            诊断假设：
            {hypotheses}

            挑战分析：
            {challenges}
            """)
        ])

        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def process(self, input_data: Dict[str, Any], context: List[Document] = None) -> Dict[str, Any]:
        """生成最终诊断结果"""
        medical_record = input_data.get("medical_record", "")
        hypotheses = input_data.get("hypotheses", [])
        challenges = input_data.get("challenges", {})

        # 调用LLM生成最终诊断
        result = self.chain.invoke({
            "medical_record": medical_record,
            "hypotheses": json.dumps(hypotheses, ensure_ascii=False),
            "challenges": json.dumps(challenges, ensure_ascii=False)
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