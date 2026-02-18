#!/bin/bash

# Quick Start Script for LightRAG Chatbot
# This script helps you get started quickly

set -e

echo "🚀 LightRAG Chatbot - Quick Start"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This script is designed for macOS${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}❌ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

if ! command_exists psql; then
    echo -e "${YELLOW}⚠️  PostgreSQL not found. Installing...${NC}"
    brew install postgresql@14
    brew services start postgresql@14
fi

echo -e "${GREEN}✅ Prerequisites OK${NC}"
echo ""

# Setup Backend
echo "🔧 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Setup .env
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp ../config/.env.example .env
    echo -e "${YELLOW}⚠️  Please edit backend/.env and add your OPENAI_API_KEY${NC}"
fi

cd ..
echo -e "${GREEN}✅ Backend setup complete${NC}"
echo ""

# Setup Frontend
echo "🎨 Setting up Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

cd ..
echo -e "${GREEN}✅ Frontend setup complete${NC}"
echo ""

# Setup Database
echo "🗄️  Setting up Database..."
if ! psql -lqt | cut -d \| -f 1 | grep -qw lightrag; then
    echo "Creating database..."
    createdb lightrag
    echo -e "${GREEN}✅ Database created${NC}"
else
    echo -e "${GREEN}✅ Database already exists${NC}"
fi
echo ""

# Summary
echo "=================================="
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Configure your OpenAI API key:"
echo "   nano backend/.env"
echo ""
echo "2️⃣  Start the backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "3️⃣  Start the frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4️⃣  Load mock data (Terminal 3):"
echo "   source backend/venv/bin/activate"
echo "   python scripts/ingest.py"
echo ""
echo "5️⃣  Open browser:"
echo "   http://localhost:3000"
echo ""
echo "📚 For detailed instructions, see SETUP_GUIDE.md"
