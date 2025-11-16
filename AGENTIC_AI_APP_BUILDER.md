# Agentic AI App Builder

## Overview
The Agentic AI App Builder is a comprehensive enhancement to the generator-az-ai Yeoman generator that enables users to build, manage, and orchestrate AI agents for Azure deployments.

## Features

### 1. Agent Management System (`agent_builder.py`)
- **AgentConfig**: Define agents with name, role, instructions, model configuration, and tools
- **AgentRegistry**: Central registry for managing agents and workflows with YAML persistence
- **AgentBuilder**: Fluent API for creating agents programmatically
- **WorkflowConfig**: Define multi-agent workflows with orchestration patterns
- **WorkflowBuilder**: Fluent API for building complex agent workflows
- **Agent Templates**: Pre-configured templates for common agent types (critic, writer, researcher, planner, executor)

### 2. REST API Backend (`app_builder.py`)
Full-featured FastAPI backend with endpoints for:
- **Agents**: GET, POST, PUT, DELETE operations
- **Workflows**: GET, POST, PUT, DELETE operations
- **Templates**: GET available templates, POST to instantiate
- **Conversations**: POST to execute agents/workflows
- **Health Check**: Monitor service status

### 3. Interactive UI (`frontend/app_builder.py`)
Streamlit-based web interface with:
- **Home Page**: Overview and getting started guide
- **Agents Page**: Create, view, edit, and delete agents
- **Workflows Page**: Build multi-agent workflows with pattern selection
- **Templates Page**: Browse and instantiate agent templates
- **Chat Page**: Test agents and workflows interactively

### 4. Dynamic Orchestration (`dynamic_orchestrator.py`)
Multiple orchestration patterns:
- **Sequential**: Agents execute one after another
- **Parallel**: All agents execute simultaneously
- **Hierarchical**: Coordinator agent manages worker agents
- **Dynamic**: Switch patterns at runtime based on context

### 5. Testing Framework (`agent_testing.py`)
Comprehensive testing utilities:
- **TestCase**: Define test inputs and expected outputs
- **TestResult**: Track test execution results with timing
- **AgentTester**: Run tests against agents with validation
- **WorkflowValidator**: Validate agent and workflow configurations
- **Sample Test Cases**: Pre-defined tests for common scenarios

## Usage

### Generate a New Project
```bash
yo az-ai
```

### Create an Agent
```python
from agent_builder import AgentBuilder

agent = (AgentBuilder("critic")
    .with_role("Code Reviewer")
    .with_instructions("Review code for quality and best practices")
    .with_model("gpt-4", temperature=0.3)
    .build())
```

### Build a Workflow
```python
from agent_builder import WorkflowBuilder

workflow = (WorkflowBuilder("blog_pipeline")
    .add_agent("researcher", researcher_agent)
    .add_agent("writer", writer_agent)
    .add_agent("critic", critic_agent)
    .with_pattern("sequential")
    .build())
```

### Use Templates
```python
from agent_builder import AgentRegistry, AGENT_TEMPLATES

registry = AgentRegistry()
critic_config = AGENT_TEMPLATES["critic"]
critic = registry.create_agent_from_config(critic_config)
```

### Run Tests
```python
from agent_testing import AgentTester, load_sample_tests

tester = AgentTester("test_suite")
load_sample_tests(tester)
results = await tester.run_all_tests(my_agent)
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
│         (Agent & Workflow Management UI)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST
┌─────────────────────▼───────────────────────────────────────┐
│                    FastAPI Backend                          │
│         (REST API + Agent Orchestration)                    │
├─────────────────────────────────────────────────────────────┤
│  Agent Builder  │  Agent Registry  │  Dynamic Orchestrator  │
├─────────────────────────────────────────────────────────────┤
│                    Semantic Kernel                          │
│              (Agent Runtime & Plugins)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  Azure OpenAI                               │
│              (GPT-4, GPT-3.5, etc.)                         │
└─────────────────────────────────────────────────────────────┘
```

## Integration with Existing Patterns

The Agentic AI App Builder extends the existing orchestration patterns:
- **DebateOrchestrator** (from `patterns/debate.py`)
- **ReasonerOrchestrator** (from `patterns/reasoner.py`)
- **PlannerOrchestrator** (from `patterns/planner_executor.py`)

You can use these patterns through the dynamic orchestrator or directly through the API.

## Configuration

Agents are configured via YAML files (e.g., `agents/critic.yaml`):
```yaml
name: critic
role: Code Reviewer
description: Reviews code for quality and best practices
instructions: |
  You are an expert code reviewer...
model_id: gpt-4
temperature: 0.3
tools: []
```

## Deployment

The generated applications include:
- **Bicep templates** for Azure infrastructure
- **Container support** with Dockerfiles
- **Azure Container Apps** hosting configuration
- **Azure AI Foundry** integration
- **Authentication** with Azure identity

## Testing

Run the test suite to validate agent behavior:
```bash
# Backend tests
cd src/backend
pytest test_agents.py

# Generator tests
npm test
```

## Next Steps

1. **Extend Templates**: Add more agent templates for specific use cases
2. **Enhanced Orchestration**: Add conditional logic and branching workflows
3. **Monitoring**: Add telemetry and logging for agent execution
4. **Multi-Modal**: Support for vision, speech, and other modalities
5. **Tool Integration**: Connect agents to external APIs and services

## License
MIT License - See LICENSE file for details

## Contributing
See CONTRIBUTING.md for contribution guidelines
