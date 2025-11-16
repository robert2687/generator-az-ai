"""
Enhanced FastAPI backend with agent builder capabilities
"""
import json
import logging
import os
from typing import Dict, List, Optional
from fastapi import FastAPI, Body, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from patterns.debate import DebateOrchestrator
from patterns.reasoner import ReasonerOrchestrator
from agent_builder import (
    AgentRegistry, AgentBuilder, WorkflowBuilder,
    AgentConfig, WorkflowConfig, AgentRole, OrchestrationPattern,
    get_agent_template, list_agent_templates
)
from utils.util import load_dotenv_from_azd, set_up_tracing, set_up_metrics, set_up_logging

load_dotenv_from_azd()
set_up_tracing()
set_up_metrics()
set_up_logging()

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:   %(name)s   %(message)s',
)
logger = logging.getLogger(__name__)
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)
logging.getLogger('azure.monitor.opentelemetry.exporter.export').setLevel(logging.WARNING)

# Initialize agent registry
agent_registry = AgentRegistry("agents")

# Default orchestrator
orchestrator = ReasonerOrchestrator()

app = FastAPI(
    title="Agentic AI App Builder",
    description="Backend API for building and managing AI agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Diagnostics: %s", os.getenv('SEMANTICKERNEL_EXPERIMENTAL_GENAI_ENABLE_OTEL_DIAGNOSTICS'))


# Pydantic models for API
class AgentCreateRequest(BaseModel):
    name: str
    role: str
    description: str
    instructions: str
    model_id: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    tools: List[str] = []
    metadata: Dict = {}


class WorkflowCreateRequest(BaseModel):
    name: str
    description: str
    pattern: str
    agents: List[str]
    termination_condition: Optional[str] = None
    max_iterations: int = 10
    metadata: Dict = {}


class ConversationRequest(BaseModel):
    topic: str
    user_id: str = "default_user"
    workflow: Optional[str] = None


# ============================================================================
# Agent Management Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Agentic AI App Builder API",
        "version": "1.0.0",
        "endpoints": {
            "agents": "/agents",
            "workflows": "/workflows",
            "templates": "/templates",
            "blog": "/blog"
        }
    }


@app.get("/agents")
async def list_agents():
    """List all registered agents"""
    agents = agent_registry.list_agents()
    return {
        "agents": [agent.to_dict() for agent in agents],
        "count": len(agents)
    }


@app.get("/agents/{agent_name}")
async def get_agent(agent_name: str):
    """Get a specific agent by name"""
    agent = agent_registry.get_agent(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")
    return agent.to_dict()


@app.post("/agents")
async def create_agent(request: AgentCreateRequest):
    """Create a new agent"""
    try:
        builder = AgentBuilder(agent_registry)
        agent = (builder
                .create(request.name, AgentRole(request.role))
                .with_description(request.description)
                .with_instructions(request.instructions)
                .with_tools(*request.tools)
                .with_metadata(**request.metadata)
                .build(register=True))

        if request.model_id:
            agent.model_id = request.model_id
            agent.temperature = request.temperature
            agent_registry.save_agent(agent)

        return {
            "message": f"Agent '{agent.name}' created successfully",
            "agent": agent.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to create agent: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/agents/{agent_name}")
async def update_agent(agent_name: str, request: AgentCreateRequest):
    """Update an existing agent"""
    existing_agent = agent_registry.get_agent(agent_name)
    if not existing_agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    try:
        builder = AgentBuilder(agent_registry)
        agent = (builder
                .create(request.name, AgentRole(request.role))
                .with_description(request.description)
                .with_instructions(request.instructions)
                .with_tools(*request.tools)
                .with_metadata(**request.metadata)
                .build(register=True))

        if request.model_id:
            agent.model_id = request.model_id
            agent.temperature = request.temperature
            agent_registry.save_agent(agent)

        return {
            "message": f"Agent '{agent.name}' updated successfully",
            "agent": agent.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to update agent: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/agents/{agent_name}")
async def delete_agent(agent_name: str):
    """Delete an agent"""
    if agent_registry.delete_agent(agent_name):
        return {"message": f"Agent '{agent_name}' deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")


# ============================================================================
# Workflow Management Endpoints
# ============================================================================

@app.get("/workflows")
async def list_workflows():
    """List all registered workflows"""
    workflows = agent_registry.list_workflows()
    return {
        "workflows": [workflow.to_dict() for workflow in workflows],
        "count": len(workflows)
    }


@app.get("/workflows/{workflow_name}")
async def get_workflow(workflow_name: str):
    """Get a specific workflow by name"""
    workflow = agent_registry.get_workflow(workflow_name)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_name}' not found")
    return workflow.to_dict()


@app.post("/workflows")
async def create_workflow(request: WorkflowCreateRequest):
    """Create a new workflow"""
    try:
        builder = WorkflowBuilder(agent_registry)
        workflow = (builder
                   .create(request.name, OrchestrationPattern(request.pattern))
                   .with_description(request.description)
                   .add_agents(*request.agents)
                   .with_max_iterations(request.max_iterations)
                   .build(register=True))

        if request.termination_condition:
            workflow.termination_condition = request.termination_condition
            agent_registry.save_workflow(workflow)

        return {
            "message": f"Workflow '{workflow.name}' created successfully",
            "workflow": workflow.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to create workflow: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/workflows/{workflow_name}")
async def delete_workflow(workflow_name: str):
    """Delete a workflow"""
    workflow = agent_registry.get_workflow(workflow_name)
    if not workflow:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_name}' not found")

    # Remove from registry (note: need to implement delete in registry)
    if workflow_name in agent_registry.workflows:
        del agent_registry.workflows[workflow_name]
        return {"message": f"Workflow '{workflow_name}' deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_name}' not found")


# ============================================================================
# Template Endpoints
# ============================================================================

@app.get("/templates")
async def list_templates():
    """List all available agent templates"""
    templates = list_agent_templates()
    return {
        "templates": templates,
        "count": len(templates)
    }


@app.get("/templates/{template_name}")
async def get_template(template_name: str):
    """Get a specific agent template"""
    template = get_agent_template(template_name)
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")
    return template.to_dict()


@app.post("/templates/{template_name}/instantiate")
async def instantiate_template(template_name: str, custom_name: str = Query(...)):
    """Instantiate an agent from a template"""
    template = get_agent_template(template_name)
    if not template:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")

    try:
        builder = AgentBuilder(agent_registry)
        agent = (builder
                .create(custom_name, template.role)
                .with_description(template.description)
                .with_instructions(template.instructions)
                .build(register=True))

        return {
            "message": f"Agent '{custom_name}' created from template '{template_name}'",
            "agent": agent.to_dict()
        }
    except Exception as e:
        logger.error(f"Failed to instantiate template: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# Orchestration Endpoints
# ============================================================================

@app.get("/patterns")
async def list_patterns():
    """List all available orchestration patterns"""
    return {
        "patterns": [pattern.value for pattern in OrchestrationPattern],
        "count": len(OrchestrationPattern)
    }


# ============================================================================
# Original Blog Endpoint (Enhanced)
# ============================================================================

@app.post("/blog")
async def http_blog(request_body: dict = Body(...)):
    """Generate a blog post using the agent orchestrator"""
    logger.info('API request received with body %s', request_body)

    topic = request_body.get('topic', 'Starwars')
    user_id = request_body.get('user_id', 'default_user')
    workflow_name = request_body.get('workflow', None)

    # If a specific workflow is requested, try to use it
    # For now, we'll stick with the default orchestrator

    content = f"Write a blog post about {topic}."

    conversation_messages = []
    conversation_messages.append({'role': 'user', 'name': 'user', 'content': content})

    async def process_conversation():
        async for i in orchestrator.process_conversation(user_id, conversation_messages):
            yield i + '\n'

    return StreamingResponse(process_conversation(), media_type="application/json")


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents": len(agent_registry.list_agents()),
        "workflows": len(agent_registry.list_workflows())
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
