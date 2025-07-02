# Setup script for boto3-examples on Windows
# This PowerShell script automates the setup process

Write-Host "🚀 Setting up boto3-examples development environment..." -ForegroundColor Green
Write-Host "=" * 60

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Found Python: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "   Please install Python from https://python.org" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment if it doesn't exist
if (!(Test-Path ".venv")) {
    Write-Host "🔄 Creating virtual environment..." -ForegroundColor Blue
    python -m venv .venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "ℹ️  Virtual environment already exists" -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Blue
& ".\.venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "🔄 Upgrading pip..." -ForegroundColor Blue
python -m pip install --upgrade pip

# Install dependencies
Write-Host "🔄 Installing boto3 and dependencies..." -ForegroundColor Blue
pip install boto3 botocore

# Verify installation
Write-Host "🔄 Verifying installation..." -ForegroundColor Blue
$verification = python -c "import boto3; print(f'boto3 version: {boto3.__version__}')" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ $verification" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to verify boto3 installation" -ForegroundColor Red
    exit 1
}

# Create .env file if it doesn't exist
if (!(Test-Path ".env") -and (Test-Path ".env.example")) {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Blue
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file" -ForegroundColor Green
    Write-Host "   Please edit .env with your AWS credentials" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Configure your AWS credentials (see README.md)" -ForegroundColor White
Write-Host "   2. Test the setup: python examples\test_connection.py" -ForegroundColor White
Write-Host ""
Write-Host "📚 Resources:" -ForegroundColor Cyan
Write-Host "   - Project README: README.md" -ForegroundColor White
Write-Host "   - AWS Documentation: https://docs.aws.amazon.com/" -ForegroundColor White
Write-Host "   - Boto3 Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html" -ForegroundColor White
Write-Host ""
Write-Host "💡 The virtual environment is now active!" -ForegroundColor Green
Write-Host "   To deactivate it later, run: deactivate" -ForegroundColor Yellow
