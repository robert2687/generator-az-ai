"""
Agent Builder - Dynamic agent creation and management system
"""
import os
import yaml
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Predefined agent roles"""
    PLANNER = "planner"
    EXECUTOR = "executor"
    CRITIC = "critic"
    RESEARCHER = "researcher"
    WRITER = "writer"
    ANALYZER = "analyzer"
    COORDINATOR = "coordinator"
    CUSTOM = "custom"


class OrchestrationPattern(Enum):
    """Available orchestration patterns"""
    DEBATE = "debate"
    PLANNER_EXECUTOR = "planner_executor"
    REASONER = "reasoner"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"


@dataclass
class AgentConfig:
    """Configuration for a single agent"""
    name: str
    role: AgentRole
    description: str
    instructions: str
    model_id: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    tools: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.tools is None:
            self.tools = []
        if self.metadata is None:
            self.metadata = {}
        if isinstance(self.role, str):
            self.role = AgentRole(self.role)

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['role'] = self.role.value
        return data

    def to_yaml(self) -> str:
        """Convert to YAML format"""
        return yaml.dump(self.to_dict(), default_flow_style=False)

    @classmethod
    def from_dict(cls, data: Dict) -> 'AgentConfig':
        """Create from dictionary"""
        return cls(**data)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'AgentConfig':
        """Load from YAML file"""
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)


@dataclass
class WorkflowConfig:
    """Configuration for an agent workflow"""
    name: str
    description: str
    pattern: OrchestrationPattern
    agents: List[str]
    termination_condition: Optional[str] = None
    max_iterations: int = 10
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if isinstance(self.pattern, str):
            self.pattern = OrchestrationPattern(self.pattern)

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        data = asdict(self)
        data['pattern'] = self.pattern.value
        return data


class AgentRegistry:
    """Registry for managing agents and workflows"""
    
    def __init__(self, base_path: str = "agents"):
        self.base_path = Path(base_path)
        self.agents: Dict[str, AgentConfig] = {}
        self.workflows: Dict[str, WorkflowConfig] = {}
        self._load_agents()
        self._load_workflows()

    def _load_agents(self):
        """Load all agents from the agents directory"""
        if not self.base_path.exists():
            logger.warning(f"Agent directory {self.base_path} does not exist")
            return

        for yaml_file in self.base_path.glob("*.yaml"):
            try:
                agent = AgentConfig.from_yaml(yaml_file)
                self.agents[agent.name] = agent
                logger.info(f"Loaded agent: {agent.name}")
            except Exception as e:
                logger.error(f"Failed to load agent from {yaml_file}: {e}")

    def _load_workflows(self):
        """Load all workflows from the workflows directory"""
        workflows_path = self.base_path / "workflows"
        if not workflows_path.exists():
            return

        for yaml_file in workflows_path.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    data = yaml.safe_load(f)
                workflow = WorkflowConfig(**data)
                self.workflows[workflow.name] = workflow
                logger.info(f"Loaded workflow: {workflow.name}")
            except Exception as e:
                logger.error(f"Failed to load workflow from {yaml_file}: {e}")

    def register_agent(self, agent: AgentConfig, save: bool = True) -> None:
        """Register a new agent"""
        self.agents[agent.name] = agent
        if save:
            self.save_agent(agent)
        logger.info(f"Registered agent: {agent.name}")

    def save_agent(self, agent: AgentConfig) -> None:
        """Save agent configuration to file"""
        self.base_path.mkdir(parents=True, exist_ok=True)
        filepath = self.base_path / f"{agent.name}.yaml"
        with open(filepath, 'w') as f:
            f.write(agent.to_yaml())
        logger.info(f"Saved agent to {filepath}")

    def get_agent(self, name: str) -> Optional[AgentConfig]:
        """Get agent by name"""
        return self.agents.get(name)

    def list_agents(self) -> List[AgentConfig]:
        """List all registered agents"""
        return list(self.agents.values())

    def delete_agent(self, name: str) -> bool:
        """Delete an agent"""
        if name in self.agents:
            del self.agents[name]
            filepath = self.base_path / f"{name}.yaml"
            if filepath.exists():
                filepath.unlink()
            logger.info(f"Deleted agent: {name}")
            return True
        return False

    def register_workflow(self, workflow: WorkflowConfig, save: bool = True) -> None:
        """Register a new workflow"""
        self.workflows[workflow.name] = workflow
        if save:
            self.save_workflow(workflow)
        logger.info(f"Registered workflow: {workflow.name}")

    def save_workflow(self, workflow: WorkflowConfig) -> None:
        """Save workflow configuration to file"""
        workflows_path = self.base_path / "workflows"
        workflows_path.mkdir(parents=True, exist_ok=True)
        filepath = workflows_path / f"{workflow.name}.yaml"
        with open(filepath, 'w') as f:
            yaml.dump(workflow.to_dict(), f, default_flow_style=False)
        logger.info(f"Saved workflow to {filepath}")

    def get_workflow(self, name: str) -> Optional[WorkflowConfig]:
        """Get workflow by name"""
        return self.workflows.get(name)

    def list_workflows(self) -> List[WorkflowConfig]:
        """List all registered workflows"""
        return list(self.workflows.values())


class AgentBuilder:
    """Builder for creating and configuring agents"""
    
    def __init__(self, registry: Optional[AgentRegistry] = None):
        self.registry = registry or AgentRegistry()
        self._current_agent: Optional[AgentConfig] = None

    def create(self, name: str, role: AgentRole = AgentRole.CUSTOM) -> 'AgentBuilder':
        """Start creating a new agent"""
        self._current_agent = AgentConfig(
            name=name,
            role=role,
            description="",
            instructions=""
        )
        return self

    def with_description(self, description: str) -> 'AgentBuilder':
        """Set agent description"""
        if self._current_agent:
            self._current_agent.description = description
        return self

    def with_instructions(self, instructions: str) -> 'AgentBuilder':
        """Set agent instructions"""
        if self._current_agent:
            self._current_agent.instructions = instructions
        return self

    def with_model(self, model_id: str, temperature: float = 0.7) -> 'AgentBuilder':
        """Set model configuration"""
        if self._current_agent:
            self._current_agent.model_id = model_id
            self._current_agent.temperature = temperature
        return self

    def with_tools(self, *tools: str) -> 'AgentBuilder':
        """Add tools to the agent"""
        if self._current_agent:
            self._current_agent.tools.extend(tools)
        return self

    def with_metadata(self, **metadata) -> 'AgentBuilder':
        """Add metadata to the agent"""
        if self._current_agent:
            self._current_agent.metadata.update(metadata)
        return self

    def build(self, register: bool = True) -> AgentConfig:
        """Build and optionally register the agent"""
        if not self._current_agent:
            raise ValueError("No agent being built. Call create() first.")
        
        agent = self._current_agent
        self._current_agent = None
        
        if register:
            self.registry.register_agent(agent)
        
        return agent


class WorkflowBuilder:
    """Builder for creating agent workflows"""
    
    def __init__(self, registry: Optional[AgentRegistry] = None):
        self.registry = registry or AgentRegistry()
        self._current_workflow: Optional[WorkflowConfig] = None

    def create(self, name: str, pattern: OrchestrationPattern) -> 'WorkflowBuilder':
        """Start creating a new workflow"""
        self._current_workflow = WorkflowConfig(
            name=name,
            description="",
            pattern=pattern,
            agents=[]
        )
        return self

    def with_description(self, description: str) -> 'WorkflowBuilder':
        """Set workflow description"""
        if self._current_workflow:
            self._current_workflow.description = description
        return self

    def add_agent(self, agent_name: str) -> 'WorkflowBuilder':
        """Add an agent to the workflow"""
        if self._current_workflow:
            self._current_workflow.agents.append(agent_name)
        return self

    def add_agents(self, *agent_names: str) -> 'WorkflowBuilder':
        """Add multiple agents to the workflow"""
        if self._current_workflow:
            self._current_workflow.agents.extend(agent_names)
        return self

    def with_termination(self, condition: str) -> 'WorkflowBuilder':
        """Set termination condition"""
        if self._current_workflow:
            self._current_workflow.termination_condition = condition
        return self

    def with_max_iterations(self, max_iterations: int) -> 'WorkflowBuilder':
        """Set maximum iterations"""
        if self._current_workflow:
            self._current_workflow.max_iterations = max_iterations
        return self

    def build(self, register: bool = True) -> WorkflowConfig:
        """Build and optionally register the workflow"""
        if not self._current_workflow:
            raise ValueError("No workflow being built. Call create() first.")
        
        workflow = self._current_workflow
        self._current_workflow = None
        
        if register:
            self.registry.register_workflow(workflow)
        
        return workflow


# Predefined agent templates
AGENT_TEMPLATES = {
    "critic": AgentConfig(
        name="critic",
        role=AgentRole.CRITIC,
        description="Analyzes and provides constructive feedback",
        instructions="""You are a Critic Agent. You carefully analyze content and provide constructive feedback.
        
Your Task:
- Analyze the content objectively
- Identify strengths and weaknesses
- Provide actionable suggestions for improvement
- Rate the quality on a scale of 1-10
        """
    ),
    "writer": AgentConfig(
        name="writer",
        role=AgentRole.WRITER,
        description="Creates high-quality written content",
        instructions="""You are a Writer Agent. You create engaging, well-structured content.
        
Your Task:
- Understand the topic and audience
- Create clear, compelling content
- Follow best practices for the content type
- Incorporate feedback when provided
        """
    ),
    "researcher": AgentConfig(
        name="researcher",
        role=AgentRole.RESEARCHER,
        description="Gathers and synthesizes information",
        instructions="""You are a Researcher Agent. You gather accurate, relevant information.
        
Your Task:
- Identify key information sources
- Collect relevant facts and data
- Synthesize findings clearly
- Cite sources when applicable
        """
    ),
    "planner": AgentConfig(
        name="planner",
        role=AgentRole.PLANNER,
        description="Creates strategic plans and task breakdowns",
        instructions="""You are a Planner Agent. You create comprehensive plans to achieve goals.
        
Your Task:
- Understand the overall objective
- Break down into actionable steps
- Identify dependencies and priorities
- Create realistic timelines
        """
    ),
    "executor": AgentConfig(
        name="executor",
        role=AgentRole.EXECUTOR,
        description="Executes plans and completes tasks",
        instructions="""You are an Executor Agent. You complete tasks efficiently and effectively.
        
Your Task:
- Follow the provided plan
- Execute each step carefully
- Report progress and results
- Handle errors gracefully
        """
    )
}


def get_agent_template(template_name: str) -> Optional[AgentConfig]:
    """Get a predefined agent template"""
    return AGENT_TEMPLATES.get(template_name)


def list_agent_templates() -> List[str]:
    """List available agent templates"""
    return list(AGENT_TEMPLATES.keys())
