#!/usr/bin/env python3
"""
Agentic AI App Builder - Interactive Demo
No dependencies required - showcases all features
"""


def print_banner():
    """Print welcome banner"""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  🤖 AGENTIC AI APP BUILDER - Interactive Demo".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_agent_templates():
    """Demonstrate available agent templates"""
    print_section("📋 Available Agent Templates")

    templates = {
        "critic": ("Code Critic", "Reviews and critiques code for improvements", "gpt-4", 0.3),
        "writer": ("Content Writer", "Creates engaging written content", "gpt-4", 0.7),
        "researcher": ("Research Specialist", "Conducts thorough research on topics", "gpt-4", 0.5),
        "planner": ("Task Planner", "Creates detailed execution plans", "gpt-4", 0.4),
        "executor": ("Task Executor", "Executes planned tasks efficiently", "gpt-4", 0.3)
    }

    for name, (role, desc, model, temp) in templates.items():
        print(f"  📌 {name.upper()}")
        print(f"     Role: {role}")
        print(f"     Description: {desc}")
        print(f"     Model: {model} (temperature: {temp})\n")


def demo_agent_builder():
    """Demonstrate building agents"""
    print_section("🔨 Building Custom Agents")

    print("  Using the fluent builder API:\n")
    print('  ```python')
    print('  agent = (AgentBuilder("code_reviewer")')
    print('      .with_role("Senior Code Reviewer")')
    print('      .with_description("Reviews code for quality and best practices")')
    print('      .with_instructions("""')
    print('          Review code for:')
    print('          - Code quality and maintainability')
    print('          - Security vulnerabilities')
    print('          - Performance optimization')
    print('      """)')
    print('      .with_model("gpt-4", temperature=0.3)')
    print('      .with_max_tokens(2000)')
    print('      .build())')
    print('  ```\n')

    print("  ✅ Result:")
    print("     Name: code_reviewer")
    print("     Role: Senior Code Reviewer")
    print("     Model: gpt-4 (temp: 0.3)")
    print("     Max Tokens: 2000")


def demo_workflow_builder():
    """Demonstrate workflow building"""
    print_section("🔄 Building Agent Workflows")

    print("  Creating a content creation pipeline:\n")
    print('  ```python')
    print('  workflow = (WorkflowBuilder("content_pipeline")')
    print('      .with_description("End-to-end content creation")')
    print('      .add_agent("researcher", researcher_agent)')
    print('      .add_agent("writer", writer_agent)')
    print('      .add_agent("editor", editor_agent)')
    print('      .with_pattern("sequential")')
    print('      .build())')
    print('  ```\n')

    print("  ✅ Pipeline Flow:")
    print("     1. 🔍 Researcher → Gathers information")
    print("     2. ✍️  Writer → Creates content from research")
    print("     3. ✏️  Editor → Polishes final content")


def demo_orchestration_patterns():
    """Demonstrate orchestration patterns"""
    print_section("⚙️  Orchestration Patterns")

    patterns = [
        ("Sequential", "⏩", "Agents execute one after another, output flows forward"),
        ("Parallel", "⏭️", "All agents execute simultaneously with same input"),
        ("Hierarchical", "🏗️", "Coordinator agent manages and delegates to workers"),
        ("Dynamic", "🔀", "Switch patterns at runtime based on context")
    ]

    for name, emoji, desc in patterns:
        print(f"  {emoji} {name}")
        print(f"     {desc}\n")


def demo_agent_registry():
    """Demonstrate agent registry"""
    print_section("📚 Agent Registry & Persistence")

    print("  ```python")
    print("  # Create registry")
    print("  registry = AgentRegistry()")
    print()
    print("  # Register agents")
    print("  registry.register_agent(critic_agent)")
    print("  registry.register_agent(writer_agent)")
    print()
    print("  # Save to YAML")
    print("  registry.save_to_yaml('agents.yaml')")
    print()
    print("  # Load from YAML")
    print("  registry.load_from_yaml('agents.yaml')")
    print()
    print("  # Retrieve agent")
    print("  agent = registry.get_agent('critic')")
    print("  ```\n")

    print("  ✅ Features:")
    print("     • Central agent management")
    print("     • YAML-based persistence")
    print("     • Easy agent lookup and retrieval")
    print("     • Workflow configuration storage")


def demo_testing_framework():
    """Demonstrate testing"""
    print_section("✅ Testing Framework")

    print("  ```python")
    print("  # Create test suite")
    print("  tester = AgentTester('blog_writer_tests')")
    print()
    print("  # Add test cases")
    print("  tester.add_test_case(")
    print("      name='simple_blog_request',")
    print("      description='Test blog post generation',")
    print("      input_messages=[")
    print("          {'role': 'user', 'content': 'Write about Python'}")
    print("      ],")
    print("      expected_outputs=['blog', 'python']")
    print("  )")
    print()
    print("  # Run tests")
    print("  results = await tester.run_all_tests(agent)")
    print("  ```\n")

    print("  📝 Sample Test Cases:")
    print("     1. simple_blog_request - Blog post generation")
    print("     2. complex_analysis - Multi-perspective analysis")
    print("     3. creative_writing - Story generation\n")

    print("  ⚠️  Note: Test execution requires Azure OpenAI credentials")


def demo_api_endpoints():
    """Show REST API"""
    print_section("🌐 REST API Endpoints")

    endpoints = [
        ("Agents", [
            ("GET", "/agents", "List all agents"),
            ("POST", "/agents", "Create new agent"),
            ("GET", "/agents/{name}", "Get specific agent"),
            ("PUT", "/agents/{name}", "Update agent"),
            ("DELETE", "/agents/{name}", "Delete agent"),
        ]),
        ("Workflows", [
            ("GET", "/workflows", "List all workflows"),
            ("POST", "/workflows", "Create new workflow"),
            ("GET", "/workflows/{name}", "Get specific workflow"),
            ("PUT", "/workflows/{name}", "Update workflow"),
            ("DELETE", "/workflows/{name}", "Delete workflow"),
        ]),
        ("Templates & Execution", [
            ("GET", "/templates", "List available templates"),
            ("POST", "/templates/{name}/instantiate", "Create from template"),
            ("POST", "/conversation", "Execute agent/workflow"),
            ("GET", "/health", "Service health check"),
        ])
    ]

    for category, eps in endpoints:
        print(f"  {category}:")
        for method, path, desc in eps:
            print(f"    {method:6} {path:38} {desc}")
        print()


def demo_ui_features():
    """Describe UI"""
    print_section("🖥️  Streamlit Web Interface")

    pages = [
        ("🏠 Home", "Overview and getting started guide"),
        ("🤖 Agents", "Create, view, edit, and delete agents"),
        ("🔄 Workflows", "Build multi-agent workflows visually"),
        ("📋 Templates", "Browse and instantiate agent templates"),
        ("💬 Chat", "Interactive agent and workflow testing"),
    ]

    for page, desc in pages:
        print(f"  {page}")
        print(f"     {desc}\n")


def demo_deployment():
    """Show Azure deployment"""
    print_section("☁️  Azure Deployment")

    print("  Included Azure Integrations:\n")
    features = [
        ("☁️", "Azure Container Apps", "Serverless container hosting"),
        ("🔐", "Azure AD Auth", "Enterprise authentication"),
        ("🏗️", "Bicep IaC", "Infrastructure as Code templates"),
        ("📦", "Container Registry", "Private image storage"),
        ("🤖", "AI Foundry", "AI model deployment & management"),
        ("📊", "App Insights", "Application monitoring & telemetry"),
        ("🔑", "Key Vault", "Secure secrets management"),
    ]

    for emoji, name, desc in features:
        print(f"  {emoji} {name}")
        print(f"     {desc}\n")

    print("  Quick Deploy Commands:")
    print("    azd init    # Initialize Azure deployment")
    print("    azd up      # Provision & deploy to Azure")
    print("    azd down    # Remove Azure resources")


def demo_architecture():
    """Show architecture"""
    print_section("🏗️  System Architecture")

    print("""
  ┌─────────────────────────────────────────────────────┐
  │           Streamlit Frontend (Port 8501)            │
  │        Agent & Workflow Management UI               │
  └─────────────────┬───────────────────────────────────┘
                    │ HTTP/REST API
  ┌─────────────────▼───────────────────────────────────┐
  │           FastAPI Backend (Port 8000)               │
  │         REST API + Agent Orchestration              │
  ├─────────────────────────────────────────────────────┤
  │ Agent Builder │ Registry │ Dynamic Orchestrator    │
  ├─────────────────────────────────────────────────────┤
  │              Semantic Kernel Runtime                │
  │         (Agent Execution & Plugin System)           │
  └─────────────────┬───────────────────────────────────┘
                    │ Azure OpenAI API
  ┌─────────────────▼───────────────────────────────────┐
  │             Azure OpenAI Service                    │
  │        (GPT-4, GPT-3.5, Embeddings)                 │
  └─────────────────────────────────────────────────────┘
    """)


def print_summary():
    """Print summary"""
    print_section("🎉 Summary & Next Steps")

    print("""
  The Agentic AI App Builder provides:

  ✨ Key Capabilities:
     • 5 pre-configured agent templates
     • Fluent builder API for custom agents
     • Multiple orchestration patterns
     • Complete REST API for programmatic access
     • Interactive Streamlit web interface
     • Comprehensive testing framework
     • YAML-based configuration
     • Full Azure deployment support

  🚀 Getting Started:
     1. Generate project: yo az-ai
     2. Configure options and select features
     3. Deploy to Azure: azd up
     4. Start building agents!

  📚 Documentation:
     • AGENTIC_AI_APP_BUILDER.md - Feature overview
     • README.md - Project setup guide
     • doc/BEST_PRACTICES.md - Development guidelines
     • doc/DESIGN_PRINCIPLES.md - Architecture principles

  🔗 Example Workflows:
     • Content Creation: researcher → writer → editor
     • Code Review: analyzer → critic → improver
     • Data Pipeline: extractor → transformer → validator
     • Support Bot: classifier → resolver → responder

  💡 Use Cases:
     • Automated content generation
     • Code review and improvement
     • Multi-step data processing
     • Customer support automation
     • Research and analysis pipelines
""")


def main():
    """Run the demo"""
    print_banner()
    demo_agent_templates()
    demo_agent_builder()
    demo_workflow_builder()
    demo_orchestration_patterns()
    demo_agent_registry()
    demo_testing_framework()
    demo_api_endpoints()
    demo_ui_features()
    demo_deployment()
    demo_architecture()
    print_summary()

    print("\n" + "=" * 70)
    print("  ✅ Demo Complete! Ready to build agentic AI applications.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
