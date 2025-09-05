# agents/coordinator.py
from typing import Dict, Any
from .hypothesis_agent import HypothesisAgent
from .challenger_agent import ChallengerAgent
from .clinical_reasoning_agent  import ReasoningAgent


class AgentCoordinator:
    """协调三个Agent的工作流程"""

    def __init__(self, rag_retriever):
        self.rag_retriever = rag_retriever
        self.hypothesis_agent = HypothesisAgent(rag_retriever)
        self.challenger_agent = ChallengerAgent(rag_retriever)
        self.reasoning_agent = ReasoningAgent()

    def process_medical_record(self, medical_record: Dict[str, Any]) -> Dict[str, Any]:
        """处理患者病历，返回最终诊断结果"""
        # 第一步：生成诊断假设
        print(f"Step 1: {self.hypothesis_agent.name} 正在工作...")
        hypotheses = self.hypothesis_agent.process(medical_record)

        # 第二步：分析和挑战诊断假设
        print(f"Step 2: {self.challenger_agent.name} 正在工作...")
        challenger_input = {
            "medical_record": medical_record.get("medical_record", ""),
            "hypotheses": hypotheses.get("hypotheses", [])
        }
        challenges = self.challenger_agent.process(challenger_input)

        # 第三步：生成最终诊断
        print(f"Step 3: {self.reasoning_agent.name} 正在工作...")
        reasoning_input = {
            "medical_record": medical_record.get("medical_record", ""),
            "hypotheses": hypotheses.get("hypotheses", []),
            "challenges": challenges
        }
        final_diagnosis = self.reasoning_agent.process(reasoning_input)

        # 返回整合结果
        return {
            "hypotheses": hypotheses,
            "challenges": challenges,
            "final_diagnosis": final_diagnosis
        }