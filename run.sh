#!/bin/bash
# Quick start script for Miro to Chatbot Graph Converter

set -e

echo "🚀 Miro to Chatbot Graph Converter"
echo "===================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Choose an option:"
echo "  1) 🌐 Launch Web UI (Streamlit)"
echo "  2) 💻 Run CLI with demo data"
echo "  3) 🐳 Run with Docker"
echo "  4) 📖 Show documentation"
echo ""

read -p "Enter option (1-4): " option

case $option in
    1)
        echo ""
        echo "🌐 Starting Streamlit web UI..."
        echo "   Access at: http://localhost:8501"
        echo ""
        streamlit run app.py
        ;;
    2)
        echo ""
        echo "💻 Running demo with mock data..."
        python examples/demo_with_mock_data.py
        echo ""
        echo "✅ Demo complete! Check output/ folder"
        ;;
    3)
        echo ""
        echo "🐳 Starting Docker container..."
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker is not installed"
            exit 1
        fi
        docker-compose up --build
        ;;
    4)
        echo ""
        echo "📖 Documentation:"
        echo "   - README.md: Full documentation"
        echo "   - QUICKSTART.md: Quick start guide"
        echo "   - MIRO_SETUP.md: Miro API setup guide"
        echo "   - ARCHITECTURE.md: System architecture"
        echo ""
        if command -v less &> /dev/null; then
            less README.md
        else
            cat README.md
        fi
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac
