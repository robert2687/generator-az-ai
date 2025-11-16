# 🤖 Agentic AI App Builder - Application Preview

## Quick Start

Run the interactive demo:
```bash
cd preview
./run_demo.sh
```

Or directly with Python:
```bash
python3 preview/demo_app.py
```

---

## 📸 Feature Showcase

### 1. Agent Templates 📋

Pre-configured agents ready to use:

| Template | Role | Model | Temperature | Use Case |
|----------|------|-------|-------------|----------|
| **Critic** | Code Critic | GPT-4 | 0.3 | Code review & quality analysis |
| **Writer** | Content Writer | GPT-4 | 0.7 | Blog posts & documentation |
| **Researcher** | Research Specialist | GPT-4 | 0.5 | Information gathering & analysis |
| **Planner** | Task Planner | GPT-4 | 0.4 | Breaking down complex tasks |
| **Executor** | Task Executor | GPT-4 | 0.3 | Implementing planned actions |

### 2. Agent Builder API 🔨

Create custom agents with fluent builder pattern:

```python
agent = (AgentBuilder("code_reviewer")
    .with_role("Senior Code Reviewer")
    .with_description("Reviews code for quality and best practices")
    .with_instructions("""
        You are a senior code reviewer...
    """)
    .with_model("gpt-4", temperature=0.3)
    .with_max_tokens(2000)
    .build())
```

**Features:**
- ✅ Fluent, chainable API
- ✅ Type-safe configuration
- ✅ Sensible defaults
- ✅ Validation built-in

### 3. Workflow Orchestration 🔄

Build multi-agent workflows:

```python
workflow = (WorkflowBuilder("content_pipeline")
    .with_description("End-to-end content creation")
    .add_agent("researcher", researcher_agent)
    .add_agent("writer", writer_agent)
    .add_agent("editor", editor_agent)
    .with_pattern("sequential")
    .build())
```

**Execution Flow:**
```
┌────────────┐     ┌────────────┐     ┌────────────┐
│ Researcher │ ──→ │   Writer   │ ──→ │   Editor   │
│  (GPT-4)   │     │  (GPT-4)   │     │  (GPT-4)   │
└────────────┘     └────────────┘     └────────────┘
   Research           Content            Polish
```

### 4. Orchestration Patterns ⚙️

Multiple execution strategies:

| Pattern | Icon | Description | Best For |
|---------|------|-------------|----------|
| **Sequential** | ⏩ | One after another | Pipelines, workflows |
| **Parallel** | ⏭️ | All at once | Consensus, voting |
| **Hierarchical** | 🏗️ | Manager/workers | Complex tasks |
| **Dynamic** | 🔀 | Runtime switching | Adaptive systems |

### 5. Agent Registry 📚

Central management and persistence:

```python
# Create registry
registry = AgentRegistry()

# Register agents
registry.register_agent(critic_agent)
registry.register_agent(writer_agent)

# Save to YAML
registry.save_to_yaml('agents.yaml')

# Load from YAML
registry.load_from_yaml('agents.yaml')

# Retrieve agent
agent = registry.get_agent('critic')
```

**YAML Format:**
```yaml
agents:
  critic:
    name: critic
    role: Code Critic
    description: Reviews and critiques code
    model_id: gpt-4
    temperature: 0.3
```

### 6. Testing Framework ✅

Validate agent behavior:

```python
# Create test suite
tester = AgentTester('blog_writer_tests')

# Add test case
tester.add_test_case(
    name='simple_blog_request',
    description='Test blog post generation',
    input_messages=[
        {'role': 'user', 'content': 'Write about Python'}
    ],
    expected_outputs=['blog', 'python']
)

# Run tests
results = await tester.run_all_tests(agent)
```

**Test Results:**
```
✅ simple_blog_request - PASSED (2.3s)
✅ complex_analysis - PASSED (3.1s)
✅ creative_writing - PASSED (2.8s)

3/3 tests passed (8.2s total)
```

### 7. REST API 🌐

Complete HTTP interface:

#### Agent Management
```bash
# List all agents
GET /agents

# Create agent
POST /agents
{
  "name": "reviewer",
  "role": "Code Reviewer",
  "model_id": "gpt-4"
}

# Get specific agent
GET /agents/reviewer

# Update agent
PUT /agents/reviewer

# Delete agent
DELETE /agents/reviewer
```

#### Workflow Management
```bash
# List workflows
GET /workflows

# Create workflow
POST /workflows
{
  "name": "content_pipeline",
  "pattern": "sequential",
  "agents": ["researcher", "writer", "editor"]
}

# Execute workflow
POST /conversation
{
  "workflow_name": "content_pipeline",
  "messages": [{"role": "user", "content": "Write about AI"}]
}
```

### 8. Web Interface 🖥️

Streamlit-based UI with 5 pages:

#### Home Page 🏠
- Overview and quick start
- System status
- Recent activity

#### Agents Page 🤖
- Create new agents with forms
- View agent list with filtering
- Edit agent configurations
- Delete agents

#### Workflows Page 🔄
- Build workflows visually
- Select orchestration pattern
- Add/remove agents
- Test workflow execution

#### Templates Page 📋
- Browse agent templates
- Preview template details
- Instantiate from template
- Customize before creating

#### Chat Page 💬
- Interactive testing
- Select agent or workflow
- Multi-turn conversations
- View execution details

### 9. Azure Deployment ☁️

Production-ready infrastructure:

```bash
# Initialize deployment
azd init

# Deploy to Azure
azd up

# Monitor application
azd monitor

# Remove resources
azd down
```

**Included Services:**
- ☁️ Azure Container Apps (hosting)
- 🔐 Azure AD (authentication)
- 🤖 Azure AI Foundry (AI models)
- 📦 Container Registry (images)
- 🔑 Key Vault (secrets)
- 📊 Application Insights (monitoring)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit Frontend                     │
│            (Agent & Workflow Management)                │
│                    Port: 8501                           │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/REST API
┌──────────────────────▼──────────────────────────────────┐
│                  FastAPI Backend                        │
│             (REST API + Orchestration)                  │
│                    Port: 8000                           │
├─────────────────────────────────────────────────────────┤
│ Agent Builder │ Registry │ Dynamic Orchestrator        │
├─────────────────────────────────────────────────────────┤
│              Semantic Kernel Runtime                    │
│         (Agent Execution & Plugin System)               │
└──────────────────────┬──────────────────────────────────┘
                       │ Azure OpenAI API
┌──────────────────────▼──────────────────────────────────┐
│               Azure OpenAI Service                      │
│          (GPT-4, GPT-3.5, Embeddings)                   │
└─────────────────────────────────────────────────────────┘
```

---

## 💡 Example Use Cases

### Content Creation Pipeline
```
Researcher → Writer → Editor → Publisher
```
- Research topic thoroughly
- Write engaging content
- Edit for quality
- Format for publishing

### Code Review System
```
Analyzer → Critic → Improver → Validator
```
- Analyze code structure
- Identify issues
- Suggest improvements
- Validate fixes

### Customer Support Bot
```
Classifier → Resolver → Responder
```
- Classify customer issue
- Find resolution
- Generate response

### Data Processing Pipeline
```
Extractor → Transformer → Validator → Loader
```
- Extract raw data
- Transform format
- Validate quality
- Load to destination

---

## 🚀 Getting Started

### 1. Install Generator
```bash
npm link
```

### 2. Create New Project
```bash
mkdir my-agent-app
cd my-agent-app
yo az-ai
```

### 3. Configure Project
Answer the prompts:
- Project name
- Description
- Include frontend? (Y/n)
- Include backend? (Y/n)
- Azure subscription

### 4. Deploy to Azure
```bash
azd up
```

### 5. Start Building!
```python
# Create your first agent
from agent_builder import AgentBuilder

agent = (AgentBuilder("my_agent")
    .with_role("Assistant")
    .with_model("gpt-4")
    .build())
```

---

## 📚 Documentation

- **[AGENTIC_AI_APP_BUILDER.md](../AGENTIC_AI_APP_BUILDER.md)** - Complete feature documentation
- **[README.md](../README.md)** - Generator overview
- **[BEST_PRACTICES.md](../generators/app/templates/doc/BEST_PRACTICES.md)** - Development guidelines
- **[DESIGN_PRINCIPLES.md](../generators/app/templates/doc/DESIGN_PRINCIPLES.md)** - Architecture principles

---

## 🎯 Key Benefits

✨ **Rapid Development**
- Pre-configured templates
- Fluent builder API
- Sensible defaults

🔧 **Flexible Architecture**
- Multiple orchestration patterns
- Pluggable components
- Extensible design

🚀 **Production Ready**
- Azure deployment included
- Authentication & security
- Monitoring & logging

🧪 **Quality Assurance**
- Built-in testing framework
- Validation utilities
- Error handling

📊 **Developer Experience**
- Interactive web UI
- Complete REST API
- Comprehensive docs

---

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - See [LICENSE](../LICENSE) for details.

---

**Ready to build? Run the demo and start creating your agentic AI applications!** 🚀
