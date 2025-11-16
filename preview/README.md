# Agentic AI App Builder - Preview Demo

This preview demonstrates all the features of the Agentic AI App Builder without requiring Azure credentials.

## Running the Demo

```bash
# From the preview directory
python demo_app.py
```

## What You'll See

The demo showcases:

1. **Agent Templates** - Pre-configured agents (critic, writer, researcher, etc.)
2. **Agent Builder** - Creating custom agents with the fluent API
3. **Workflow Builder** - Building multi-agent workflows
4. **Agent Registry** - Managing and persisting agents
5. **Orchestration Patterns** - Sequential, parallel, and hierarchical execution
6. **Testing Framework** - Validating agent behavior
7. **REST API** - Available endpoints for programmatic access
8. **Web UI** - Streamlit interface features
9. **Azure Deployment** - Cloud deployment capabilities

## Sample Output

```
████████████████████████████████████████████████████████████████████████
█                                                                      █
█        🤖 AGENTIC AI APP BUILDER - Interactive Demo                 █
█                                                                      █
████████████████████████████████████████████████████████████████████████

======================================================================
  Available Agent Templates
======================================================================

📋 CRITIC
   Role: Code Critic
   Description: Reviews and critiques code for improvements
   Model: gpt-4 (temp: 0.3)

📋 WRITER
   Role: Content Writer
   Description: Creates engaging written content
   Model: gpt-4 (temp: 0.7)

...
```

## No Azure Required

This demo runs entirely locally and doesn't make any API calls. It's designed to help you understand the features and capabilities before generating your actual application.

## Next Steps

After reviewing the demo:

1. **Generate Your App**: Run `yo az-ai` to create a new project
2. **Customize**: Modify agents, workflows, and templates for your use case
3. **Deploy**: Use `azd up` to deploy to Azure
4. **Build**: Start creating your agentic AI application!

## Quick Start

```bash
# Install the generator globally
npm link

# Create a new project
mkdir my-agent-app
cd my-agent-app
yo az-ai

# Follow the prompts to configure your app

# Deploy to Azure
azd up
```

## Features Demonstrated

### 1. Agent Management
- Create agents with builder pattern
- Use pre-configured templates
- Register and retrieve agents
- Persist configurations to YAML

### 2. Workflow Orchestration
- Sequential processing pipelines
- Parallel agent execution
- Hierarchical coordination
- Dynamic pattern switching

### 3. Developer Tools
- REST API for all operations
- Interactive web interface
- Comprehensive testing framework
- Configuration validation

### 4. Azure Integration
- Container Apps deployment
- AI Foundry connectivity
- Authentication & authorization
- Infrastructure as Code

## Documentation

- **Main Docs**: `../AGENTIC_AI_APP_BUILDER.md`
- **Best Practices**: `../generators/app/templates/doc/BEST_PRACTICES.md`
- **Design Principles**: `../generators/app/templates/doc/DESIGN_PRINCIPLES.md`

## Support

For questions or issues:
- Check the documentation in the `docs/` folder
- Review generated project README files
- See architecture decision records in `doc/decisions/`
