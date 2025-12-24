#!/bin/bash

# HireSense Complete Setup Script
# This script sets up both backend and frontend for HireSense

echo "🎯 HireSense - Complete Setup"
echo "================================"
echo ""

# Check if running from correct directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the HireSense root directory"
    exit 1
fi

# Setup Backend
echo "📦 Setting up Backend..."
cd backend

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -Po '(?<=Python )(.+)')
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Backend dependencies installed"

# Setup environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit backend/.env and add your CEREBRAS_API_KEY"
    echo "   Get your API key from: https://cerebras.ai/"
else
    echo "✓ .env file already exists"
fi

cd ..

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

# Check Node version
NODE_VERSION=$(node --version)
echo "✓ Node version: $NODE_VERSION"

# Install dependencies
echo "Installing Node dependencies..."
npm install
echo "✓ Frontend dependencies installed"

cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Edit backend/.env and add your CEREBRAS_API_KEY"
echo "2. Start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:5173 in your browser"
echo ""
echo "🎯 Happy hiring with HireSense!"
