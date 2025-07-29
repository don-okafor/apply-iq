import asyncio
from typing import List, Dict, Any, Type
from ..agents.main_agent import BaseAgent
from ..agents.kv_store_agent import KeyValueStorageAgent
from ..agents.file_read_agent import FileReadAgent
from ..agents.job_search_agent import JobSearchAgent
from ..agents.resume_tailoring_agent import ResumeTailoringAgent
from ..agents.job_application_agent import JobApplicationAgent

AGENT_REGISTRY: Dict[str, Type[BaseAgent]] = {
    "file_read": FileReadAgent,
    "job_search": JobSearchAgent,
    "resume_tailoring": ResumeTailoringAgent,
    "job_application" : JobApplicationAgent
    #"kv_store": KeyValueStorageAgent,
}

class MCPOrchestrator:
    async def run(self, sequence: List[str], task: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        try:
            for agent_name in sequence:
                AgentCls = AGENT_REGISTRY.get(agent_name)
                if not AgentCls:
                    return {"status": "error", "message": f"Unknown agent {agent_name}"}
                agent = AgentCls()
                

                if asyncio.iscoroutinefunction(agent.run):
                    result = await agent.run(task)
                else:
                    result = agent.run(task)
                
                if not result.get("status") == "success":
                    return {
                        "status": "error",
                        "message": f"Agent '{agent_name}' failed: {result.get('message', 'Unknown error')}"
                    }

                if isinstance(result, dict):
                    task.update(result)
                elif isinstance(result, (list, tuple)):
                    task.update(dict(result))  
                else:
                    task.update({"value": result})
        except Exception as e:
             return {
                    "status": "error",
                    "message": f"Agent '{agent_name}' crashed with exception: {str(e)}"
                }
        
        return result
