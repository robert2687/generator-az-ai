#!/bin/bash
# Quick start script for the Agentic AI App Builder Preview

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                                                                   ║"
echo "║       🤖 Agentic AI App Builder - Interactive Preview            ║"
echo "║                                                                   ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Run the demo
echo "▶️  Starting demo..."
echo ""
python3 "$(dirname "$0")/demo_app.py"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 Next Steps:"
echo ""
echo "  1. Generate a new project:"
echo "     $ yo az-ai"
echo ""
echo "  2. Deploy to Azure:"
echo "     $ azd up"
echo ""
echo "  3. Learn more:"
echo "     $ cat AGENTIC_AI_APP_BUILDER.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
