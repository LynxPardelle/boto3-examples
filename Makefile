# Makefile for boto3-examples project
# Provides common commands for development workflow

.PHONY: help setup install test test-simple test-lifecycle test-connection test-all clean lint format

# Default target
help:
	@echo "boto3-examples Development Commands"
	@echo "=================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup     - Create virtual environment and install dependencies"
	@echo "  install   - Install dependencies in existing environment"
	@echo ""
	@echo "Test Commands:"
	@echo "  test             - Run connection test"
	@echo "  test-connection  - Test AWS credentials and connectivity"
	@echo "  test-simple      - Run simple S3 operations example"
	@echo "  test-lifecycle   - Run complete S3 lifecycle example"
	@echo "  test-all         - Run all examples in sequence"
	@echo ""
	@echo "Development Commands:"
	@echo "  clean     - Remove virtual environment and cache files"
	@echo ""
	@echo "Quality Commands:"
	@echo "  lint      - Run code linting (requires flake8)"
	@echo "  format    - Format code (requires black)"
	@echo ""
	@echo "Usage: make <command>"

# Setup virtual environment and dependencies
setup:
	@echo "🚀 Setting up development environment..."
	python -m venv .venv
	@echo "✅ Virtual environment created"
	@echo "🔄 Installing dependencies..."
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\pip install boto3 botocore
	@echo "✅ Dependencies installed"
	@echo "💡 Activate environment with: .\.venv\Scripts\activate"
else
	.venv/bin/pip install boto3 botocore
	@echo "✅ Dependencies installed" 
	@echo "💡 Activate environment with: source .venv/bin/activate"
endif

# Install dependencies only
install:
	@echo "🔄 Installing dependencies..."
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\pip install boto3 botocore
else
	.venv/bin/pip install boto3 botocore
endif
	@echo "✅ Dependencies installed"

# Run connection test
test:
	@echo "🧪 Running boto3 connection test..."
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\python examples\test_connection.py
else
	.venv/bin/python examples/test_connection.py
endif

# Run connection test (alias)
test-connection:
	@echo "🧪 Running boto3 connection test..."
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\python examples\test_connection.py
else
	.venv/bin/python examples/test_connection.py
endif

# Run simple S3 operations example
test-simple:
	@echo "🪣 Running simple S3 operations example..."
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\python examples\simple_s3_operations.py
else
	.venv/bin/python examples/simple_s3_operations.py
endif

# Run complete S3 lifecycle example
test-lifecycle:
	@echo "🔄 Running complete S3 lifecycle example..."
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\python examples\s3_bucket_lifecycle.py
else
	.venv/bin/python examples/s3_bucket_lifecycle.py
endif

# Run all examples
test-all:
	@echo "🎯 Running all examples..."
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\python run_all_examples.py
else
	.venv/bin/python run_all_examples.py
endif

# Clean up generated files
clean:
	@echo "🧹 Cleaning up..."
	rm -rf .venv
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
	rm -rf .coverage
	@echo "✅ Cleanup completed"

# Lint code (optional - requires flake8)
lint:
	@echo "🔍 Running code linting..."
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\pip install flake8
	.\.venv\Scripts\flake8 examples/ --max-line-length=88
else
	.venv/bin/pip install flake8
	.venv/bin/flake8 examples/ --max-line-length=88
endif

# Format code (optional - requires black)
format:
	@echo "🎨 Formatting code..."
ifeq ($(OS),Windows_NT)
	.\.venv\Scripts\pip install black
	.\.venv\Scripts\black examples/
else
	.venv/bin/pip install black
	.venv/bin/black examples/
endif
