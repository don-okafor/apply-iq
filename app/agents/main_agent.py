from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..core.registry import AGENT_REGISTRY


class BaseAgent(ABC):
    def __init__(self, context: Optional[Dict[str, Any]] = None):
        self.context = context or {}

    @abstractmethod
    def run(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Run the task and return a result."""
        pass

    def delegate_to(self, agent_name: str, task: Dict[str, Any]) -> Dict[str, Any]:
        """Pass control to another agent"""
        AgentClass = AGENT_REGISTRY.get(agent_name)
        if not AgentClass:
            raise ValueError(f"Unknown agent: {agent_name}")
        agent = AgentClass(context=self.context)
        return agent.run(task)
