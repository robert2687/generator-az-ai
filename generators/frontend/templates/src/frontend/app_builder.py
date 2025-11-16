 """
Streamlit UI for Agentic AI App Builder
"""
import base64
import json
import logging
import os
import requests
import streamlit as st
<% if (solutionLevel > 100) { -%>
from azure.identity import DefaultAzureCredential
<% } -%>
from dotenv import load_dotenv
from io import StringIO
from subprocess import run, PIPE
from typing import Dict, List, Optional


def load_dotenv_from_azd():
    result = run("azd env get-values", stdout=PIPE, stderr=PIPE, shell=True, text=True)
    if result.returncode == 0:
        logging.info(f"Found AZD environment. Loading...")
        load_dotenv(stream=StringIO(result.stdout))
    else:
        logging.info(f"AZD environment not found. Trying to load from .env file...")
        load_dotenv()


def get_principal_id():
    """Get the principal ID of the current user from request headers provided by EasyAuth."""
    result = st.context.headers.get('x-ms-client-principal-id')
    if result:
        return result
    else:
        return "default_user_id"


def get_principal_display_name():
    """Get the display name of the current user from the request headers provided by EasyAuth."""
    default_user_name = "Default User"
    principal = st.context.headers.get('x-ms-client-principal')
    if principal:
        principal = json.loads(base64.b64decode(principal).decode('utf-8'))
        claims = principal.get("claims", [])
        return next((claim["val"] for claim in claims if claim["typ"] == "name"), default_user_name)
    else:
        return default_user_name


def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False


def make_api_request(endpoint: str, method: str = "GET", data: Dict = None) -> requests.Response:
    """Make an authenticated API request to the backend"""
    backend_url = os.getenv('BACKEND_ENDPOINT', 'http://localhost:8000')
    url = f"{backend_url}{endpoint}"
    headers = {}

<% if (solutionLevel > 100) { -%>
    if not (url.startswith('http://localhost') or url.startswith('http://127.0.0.1')):
        app_id = os.getenv('AZURE_CLIENT_APP_ID')
        token = DefaultAzureCredential().get_token(f'api://{app_id}/.default')
        headers['Authorization'] = f"Bearer {token.token}"
<% } -%>

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=data, headers=headers)
    elif method == "PUT":
        response = requests.put(url, json=data, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    response.raise_for_status()
    return response


# Initialize
load_dotenv_from_azd()

# Page config
st.set_page_config(
    page_title="Agentic AI App Builder",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
st.sidebar.title("🤖 Agentic AI App Builder")
st.sidebar.write(f"Welcome, {get_principal_display_name()}!")
st.sidebar.markdown('<a href="/.auth/logout" target = "_self">Sign Out</a>', unsafe_allow_html=True)
st.sidebar.divider()

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🤖 Agents", "🔄 Workflows", "📝 Templates", "💬 Chat"]
)


# ============================================================================
# Home Page
# ============================================================================
if page == "🏠 Home":
    st.title("🤖 Agentic AI App Builder")
    st.markdown("""
    Welcome to the Agentic AI App Builder! This platform allows you to:

    - **Create and manage AI agents** with custom roles and instructions
    - **Design workflows** that orchestrate multiple agents
    - **Use templates** to quickly create common agent types
    - **Test your agents** in real-time conversations

    Get started by exploring the menu on the left!
    """)

    # Show system status
    st.subheader("System Status")
    try:
        response = make_api_request("/health")
        health = response.json()

        col1, col2, col3 = st.columns(3)
        col1.metric("Status", health.get("status", "unknown").upper())
        col2.metric("Agents", health.get("agents", 0))
        col3.metric("Workflows", health.get("workflows", 0))

    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")


# ============================================================================
# Agents Page
# ============================================================================
elif page == "🤖 Agents":
    st.title("🤖 Agent Management")

    tab1, tab2, tab3 = st.tabs(["View Agents", "Create Agent", "Edit Agent"])

    # View Agents Tab
    with tab1:
        st.subheader("Registered Agents")
        try:
            response = make_api_request("/agents")
            agents_data = response.json()
            agents = agents_data.get("agents", [])

            if not agents:
                st.info("No agents registered yet. Create one in the 'Create Agent' tab!")
            else:
                for agent in agents:
                    with st.expander(f"**{agent['name']}** - {agent['role']}"):
                        st.write(f"**Description:** {agent['description']}")
                        st.write(f"**Instructions:**")
                        st.code(agent['instructions'], language="text")
                        if agent.get('tools'):
                            st.write(f"**Tools:** {', '.join(agent['tools'])}")

                        col1, col2 = st.columns([1, 5])
                        with col1:
                            if st.button("Delete", key=f"del_{agent['name']}"):
                                try:
                                    make_api_request(f"/agents/{agent['name']}", method="DELETE")
                                    st.success(f"Agent '{agent['name']}' deleted!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Failed to delete agent: {e}")
        except Exception as e:
            st.error(f"Failed to load agents: {e}")

    # Create Agent Tab
    with tab2:
        st.subheader("Create New Agent")

        with st.form("create_agent_form"):
            name = st.text_input("Agent Name*", help="Unique identifier for the agent")
            role = st.selectbox(
                "Role*",
                ["planner", "executor", "critic", "researcher", "writer", "analyzer", "coordinator", "custom"]
            )
            description = st.text_area("Description*", help="Brief description of the agent's purpose")
            instructions = st.text_area(
                "Instructions*",
                help="Detailed instructions for the agent's behavior",
                height=200
            )

            st.subheader("Advanced Settings")
            col1, col2 = st.columns(2)
            with col1:
                model_id = st.text_input("Model ID (optional)", help="Specific model to use")
                temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
            with col2:
                max_tokens = st.number_input("Max Tokens (optional)", min_value=0, value=0)
                tools_input = st.text_input("Tools (comma-separated)", help="e.g., search, calculator")

            submitted = st.form_submit_button("Create Agent")

            if submitted:
                if not name or not description or not instructions:
                    st.error("Please fill in all required fields (marked with *)")
                else:
                    try:
                        agent_data = {
                            "name": name,
                            "role": role,
                            "description": description,
                            "instructions": instructions,
                            "temperature": temperature,
                            "tools": [t.strip() for t in tools_input.split(",")] if tools_input else [],
                            "metadata": {}
                        }
                        if model_id:
                            agent_data["model_id"] = model_id
                        if max_tokens > 0:
                            agent_data["max_tokens"] = max_tokens

                        response = make_api_request("/agents", method="POST", data=agent_data)
                        st.success(f"Agent '{name}' created successfully!")
                        st.json(response.json())
                    except Exception as e:
                        st.error(f"Failed to create agent: {e}")

    # Edit Agent Tab
    with tab3:
        st.subheader("Edit Existing Agent")
        try:
            response = make_api_request("/agents")
            agents = response.json().get("agents", [])

            if not agents:
                st.info("No agents available to edit.")
            else:
                agent_names = [a["name"] for a in agents]
                selected_agent = st.selectbox("Select Agent to Edit", agent_names)

                if selected_agent:
                    agent_data = next(a for a in agents if a["name"] == selected_agent)

                    with st.form("edit_agent_form"):
                        new_name = st.text_input("Agent Name", value=agent_data["name"])
                        role = st.selectbox(
                            "Role",
                            ["planner", "executor", "critic", "researcher", "writer", "analyzer", "coordinator", "custom"],
                            index=["planner", "executor", "critic", "researcher", "writer", "analyzer", "coordinator", "custom"].index(agent_data["role"])
                        )
                        description = st.text_area("Description", value=agent_data["description"])
                        instructions = st.text_area("Instructions", value=agent_data["instructions"], height=200)

                        submitted = st.form_submit_button("Update Agent")

                        if submitted:
                            try:
                                update_data = {
                                    "name": new_name,
                                    "role": role,
                                    "description": description,
                                    "instructions": instructions,
                                    "temperature": agent_data.get("temperature", 0.7),
                                    "tools": agent_data.get("tools", []),
                                    "metadata": agent_data.get("metadata", {})
                                }
                                make_api_request(f"/agents/{selected_agent}", method="PUT", data=update_data)
                                st.success(f"Agent '{selected_agent}' updated successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to update agent: {e}")
        except Exception as e:
            st.error(f"Failed to load agents: {e}")


# ============================================================================
# Workflows Page
# ============================================================================
elif page == "🔄 Workflows":
    st.title("🔄 Workflow Management")

    tab1, tab2 = st.tabs(["View Workflows", "Create Workflow"])

    # View Workflows Tab
    with tab1:
        st.subheader("Registered Workflows")
        try:
            response = make_api_request("/workflows")
            workflows_data = response.json()
            workflows = workflows_data.get("workflows", [])

            if not workflows:
                st.info("No workflows registered yet. Create one in the 'Create Workflow' tab!")
            else:
                for workflow in workflows:
                    with st.expander(f"**{workflow['name']}** - {workflow['pattern']}"):
                        st.write(f"**Description:** {workflow['description']}")
                        st.write(f"**Pattern:** {workflow['pattern']}")
                        st.write(f"**Agents:** {', '.join(workflow['agents'])}")
                        st.write(f"**Max Iterations:** {workflow['max_iterations']}")
                        if workflow.get('termination_condition'):
                            st.write(f"**Termination:** {workflow['termination_condition']}")

                        if st.button("Delete", key=f"del_wf_{workflow['name']}"):
                            try:
                                make_api_request(f"/workflows/{workflow['name']}", method="DELETE")
                                st.success(f"Workflow '{workflow['name']}' deleted!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to delete workflow: {e}")
        except Exception as e:
            st.error(f"Failed to load workflows: {e}")

    # Create Workflow Tab
    with tab2:
        st.subheader("Create New Workflow")

        try:
            # Get available agents
            agents_response = make_api_request("/agents")
            available_agents = [a["name"] for a in agents_response.json().get("agents", [])]

            # Get available patterns
            patterns_response = make_api_request("/patterns")
            available_patterns = patterns_response.json().get("patterns", [])

            with st.form("create_workflow_form"):
                name = st.text_input("Workflow Name*")
                description = st.text_area("Description*")
                pattern = st.selectbox("Orchestration Pattern*", available_patterns)

                st.write("**Select Agents (in execution order):**")
                if not available_agents:
                    st.warning("No agents available. Create some agents first!")
                    selected_agents = []
                else:
                    selected_agents = st.multiselect("Agents*", available_agents)

                max_iterations = st.number_input("Max Iterations", min_value=1, value=10)
                termination_condition = st.text_input("Termination Condition (optional)")

                submitted = st.form_submit_button("Create Workflow")

                if submitted:
                    if not name or not description or not selected_agents:
                        st.error("Please fill in all required fields")
                    else:
                        try:
                            workflow_data = {
                                "name": name,
                                "description": description,
                                "pattern": pattern,
                                "agents": selected_agents,
                                "max_iterations": max_iterations,
                                "metadata": {}
                            }
                            if termination_condition:
                                workflow_data["termination_condition"] = termination_condition

                            response = make_api_request("/workflows", method="POST", data=workflow_data)
                            st.success(f"Workflow '{name}' created successfully!")
                            st.json(response.json())
                        except Exception as e:
                            st.error(f"Failed to create workflow: {e}")
        except Exception as e:
            st.error(f"Failed to load resources: {e}")


# ============================================================================
# Templates Page
# ============================================================================
elif page == "📝 Templates":
    st.title("📝 Agent Templates")

    st.markdown("""
    Use pre-built agent templates to quickly create common agent types.
    Select a template and give it a custom name to instantiate.
    """)

    try:
        response = make_api_request("/templates")
        templates = response.json().get("templates", [])

        if not templates:
            st.info("No templates available.")
        else:
            for template_name in templates:
                template_response = make_api_request(f"/templates/{template_name}")
                template = template_response.json()

                with st.expander(f"**{template_name.title()}** Template"):
                    st.write(f"**Role:** {template['role']}")
                    st.write(f"**Description:** {template['description']}")
                    st.write("**Instructions:**")
                    st.code(template['instructions'], language="text")

                    with st.form(f"instantiate_{template_name}"):
                        custom_name = st.text_input("Custom Name for New Agent", value=f"{template_name}_1")
                        submitted = st.form_submit_button("Create from Template")

                        if submitted and custom_name:
                            try:
                                response = make_api_request(
                                    f"/templates/{template_name}/instantiate?custom_name={custom_name}",
                                    method="POST"
                                )
                                st.success(f"Agent '{custom_name}' created from template!")
                                st.json(response.json())
                            except Exception as e:
                                st.error(f"Failed to instantiate template: {e}")
    except Exception as e:
        st.error(f"Failed to load templates: {e}")


# ============================================================================
# Chat Page
# ============================================================================
elif page == "💬 Chat":
    st.title("💬 Test Your Agents")

    st.markdown("""
    Test your agents by requesting a blog post on any topic.
    The agents will collaborate to create content.
    """)

    topic = st.text_input("Topic for blog post", value="cookies")

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Generate", type="primary"):
            result = None
            with st.status("Agents are crafting a response...", expanded=True) as status:
                try:
                    url = f'{os.getenv("BACKEND_ENDPOINT", "http://localhost:8000")}/blog'
                    payload = {"topic": topic, "user_id": get_principal_id()}
                    headers = {}
<% if (solutionLevel > 100) { -%>
                    if not (url.startswith('http://localhost') or url.startswith('http://127.0.0.1')):
                        app_id = os.getenv('AZURE_CLIENT_APP_ID')
                        token = DefaultAzureCredential().get_token(f'api://{app_id}/.default')
                        headers['Authorization'] = f"Bearer {token.token}"
<% } -%>

                    with requests.post(url, json=payload, headers=headers, stream=True) as response:
                        for line in response.iter_lines():
                            result = line.decode('utf-8')
                            if not is_valid_json(result):
                                status.write(result)

                    status.update(label="Backend call complete", state="complete", expanded=False)

                    if result and is_valid_json(result):
                        st.subheader("Generated Blog Post")
                        result_data = json.loads(result)
                        st.markdown(result_data.get("content", result))

                except Exception as e:
                    status.update(label=f"Backend call failed: {e}", state="error", expanded=False)
                    st.error(f"Error: {e}")
