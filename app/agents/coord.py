from .hyp import *
from .chall import *
from .clin import *

class coord():
    def __init__(self):
        self.agent_hyp = hyp_agent()
        self.agent_chall = chall_agent()
        self.agent_clin = clin_agent()
    def do_job(self,query):
        pass

