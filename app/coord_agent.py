from agents.hyp import *
from agents.chall import *
from agents.clin import *
class coord_agents():
    def __init__(self):
        self.agent_hyp = hyp_agent()
        self.agent_chall = chall_agent()
        self.agent_clin = clin_agent()
    def do_job(self,query,file_path):
        result1 = self.agent_hyp.do_reaserch(query, file_path)
        query2 = result1
        result2 = self.agent_chall.do_reaserch(query2)
        result3 = self.agent_clin.do_reaserch(result1, result2,query)
        return result1,result2,result3
