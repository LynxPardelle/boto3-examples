# Boto3 Examples

This repository contains examples and utilities for working with AWS services using the boto3 Python library.

## Environment Setup

This project uses a Python virtual environment to manage dependencies and ensure consistent behavior across different systems.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- AWS CLI (optional, for easier credential management)

### Setting Up the Virtual Environment

#### 1. Clone the Repository

```bash
git clone https://github.com/LynxPardelle/boto3-examples.git
cd boto3-examples
```

#### 2. Create Virtual Environment

On Windows (PowerShell):
```powershell
python -m venv .venv
```

On macOS/Linux:
```bash
python3 -m venv .venv
```

#### 3. Activate Virtual Environment

On Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

On Windows (Command Prompt):
```cmd
.venv\Scripts\activate.bat
```

On macOS/Linux:
```bash
source .venv/bin/activate
```

#### 4. Install Dependencies

```bash
pip install boto3 botocore
```

#### 5. Verify Installation

```bash
python -c "import boto3; print(boto3.__version__)"
```

### AWS Credentials Setup

Before using boto3, you need to configure your AWS credentials. There are several ways to do this:

#### Option 1: AWS CLI Configuration
```bash
aws configure
```

#### Option 2: Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export AWS_DEFAULT_REGION=us-east-1
```

On Windows (PowerShell):
```powershell
$env:AWS_ACCESS_KEY_ID="your_access_key_here"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key_here"
$env:AWS_DEFAULT_REGION="us-east-1"
```

#### Option 3: AWS Credentials File
Create `~/.aws/credentials`:
```ini
[default]
aws_access_key_id = your_access_key_here
aws_secret_access_key = your_secret_key_here

[default]
region = us-east-1
```

### Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment:

```bash
deactivate
```

### Project Structure

```
boto3-examples/
├── .venv/                 # Virtual environment (created locally)
├── examples/              # Example scripts and utilities
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── LICENSE               # License file
└── README.md             # This file
```

### Common boto3 Usage Patterns

Here are some basic examples of how to use boto3:

#### 1. List S3 Buckets
```python
import boto3

s3 = boto3.client('s3')
response = s3.list_buckets()

for bucket in response['Buckets']:
    print(bucket['Name'])
```

#### 2. Create EC2 Instance
```python
import boto3

ec2 = boto3.resource('ec2')
instance = ec2.create_instances(
    ImageId='ami-12345678',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro'
)
```

#### 3. DynamoDB Operations
```python
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('your-table-name')

# Put item
table.put_item(
    Item={
        'id': '123',
        'name': 'Example Item'
    }
)

# Get item
response = table.get_item(
    Key={
        'id': '123'
    }
)
```

### Best Practices

1. **Always use virtual environments** to isolate project dependencies
2. **Never commit AWS credentials** to version control
3. **Use IAM roles** when running on AWS infrastructure
4. **Implement proper error handling** for AWS API calls
5. **Use pagination** for list operations that might return large datasets
6. **Enable logging** for debugging and monitoring

### Troubleshooting

#### Common Issues

1. **ModuleNotFoundError: No module named 'boto3'**
   - Make sure your virtual environment is activated
   - Verify boto3 is installed: `pip list | grep boto3`

2. **AWS credential errors**
   - Verify your credentials are correctly configured
   - Check the AWS credentials documentation: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

3. **Permission denied errors**
   - Check your IAM user/role has the necessary permissions
   - Review AWS CloudTrail logs for detailed error information

### Resources

- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS SDK Error Handling](https://docs.aws.amazon.com/sdk-for-python/v1/developer-guide/error-handling.html)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
