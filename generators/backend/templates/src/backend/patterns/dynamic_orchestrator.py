"""
Advanced orchestration patterns for agent workflows
"""
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator
from abc import ABC, abstractmethod

from semantic_kernel.kernel import Kernel
from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from agent_builder import AgentConfig, WorkflowConfig, OrchestrationPattern

logger = logging.getLogger(__name__)


class BaseOrchestrator(ABC):
    """Base class for all orchestrators"""

    def __init__(self, kernel: Kernel, workflow: WorkflowConfig):
        self.kernel = kernel
        self.workflow = workflow
        self.agents = {}

    @abstractmethod
    async def process_conversation(
        self,
        user_id: str,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Process a conversation through the orchestrator"""
        pass


class SequentialOrchestrator(BaseOrchestrator):
    """
    Sequential orchestrator - agents execute one after another
    Each agent's output becomes the next agent's input
    """

    async def process_conversation(
        self,
        user_id: str,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Process messages sequentially through agents"""
        logger.info(f"Sequential orchestration for user {user_id}")

        current_content = messages[-1]['content']

        for agent_name in self.workflow.agents:
            yield f"Agent {agent_name} processing..."

            # Simulate agent processing
            # In real implementation, this would invoke the actual agent
            agent = self.agents.get(agent_name)
            if agent:
                # Process with agent
                current_content = f"[{agent_name} output]: Processed - {current_content}"
                yield current_content
            else:
                yield f"Warning: Agent {agent_name} not found"

        yield f"Sequential processing complete"


class ParallelOrchestrator(BaseOrchestrator):
    """
    Parallel orchestrator - all agents execute simultaneously
    Results are aggregated at the end
    """

    async def process_conversation(
        self,
        user_id: str,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Process messages in parallel through agents"""
        logger.info(f"Parallel orchestration for user {user_id}")

        content = messages[-1]['content']
        results = []

        # Execute all agents in parallel
        for agent_name in self.workflow.agents:
            yield f"Agent {agent_name} starting..."

            agent = self.agents.get(agent_name)
            if agent:
                result = f"[{agent_name}]: Processed - {content}"
                results.append(result)
                yield result

        # Aggregate results
        yield "Aggregating results..."
        final_result = "\n\n".join(results)
        yield f"Final aggregated result:\n{final_result}"


class HierarchicalOrchestrator(BaseOrchestrator):
    """
    Hierarchical orchestrator - coordinator agent manages other agents
    Coordinator decides which agents to call and how to combine results
    """

    async def process_conversation(
        self,
        user_id: str,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Process messages through hierarchical structure"""
        logger.info(f"Hierarchical orchestration for user {user_id}")

        content = messages[-1]['content']

        # First agent should be the coordinator
        if not self.workflow.agents:
            yield "Error: No agents in workflow"
            return

        coordinator_name = self.workflow.agents[0]
        worker_agents = self.workflow.agents[1:]

        yield f"Coordinator {coordinator_name} analyzing task..."

        # Coordinator creates plan
        yield f"Plan: Will delegate to {len(worker_agents)} worker agents"

        # Execute workers
        results = []
        for agent_name in worker_agents:
            yield f"Worker {agent_name} executing..."
            result = f"[{agent_name}]: Completed subtask"
            results.append(result)
            yield result

        # Coordinator synthesizes
        yield f"Coordinator synthesizing results..."
        final = f"Coordinator {coordinator_name} final output:\n" + "\n".join(results)
        yield final


class DynamicOrchestrator:
    """
    Dynamic orchestrator that can switch between patterns at runtime
    """

    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        self.orchestrators = {
            OrchestrationPattern.SEQUENTIAL: SequentialOrchestrator,
            OrchestrationPattern.PARALLEL: ParallelOrchestrator,
            OrchestrationPattern.HIERARCHICAL: HierarchicalOrchestrator,
        }

    async def process_with_workflow(
        self,
        workflow: WorkflowConfig,
        user_id: str,
        messages: List[Dict[str, str]]
    ) -> AsyncGenerator[str, None]:
        """Process conversation with specified workflow"""

        orchestrator_class = self.orchestrators.get(workflow.pattern)
        if not orchestrator_class:
            yield f"Error: Orchestration pattern '{workflow.pattern}' not supported"
            return

        orchestrator = orchestrator_class(self.kernel, workflow)

        async for message in orchestrator.process_conversation(user_id, messages):
            yield message


def create_orchestrator(
    pattern: OrchestrationPattern,
    kernel: Kernel,
    workflow: WorkflowConfig
) -> BaseOrchestrator:
    """Factory function to create appropriate orchestrator"""

    orchestrators = {
        OrchestrationPattern.SEQUENTIAL: SequentialOrchestrator,
        OrchestrationPattern.PARALLEL: ParallelOrchestrator,
        OrchestrationPattern.HIERARCHICAL: HierarchicalOrchestrator,
    }

    orchestrator_class = orchestrators.get(pattern)
    if not orchestrator_class:
        raise ValueError(f"Unknown orchestration pattern: {pattern}")

    return orchestrator_class(kernel, workflow)
