#!/usr/bin/env python3
"""
Simple boto3 example to test AWS connectivity and basic operations.

This script demonstrates:
1. How to create boto3 clients
2. Basic AWS service interactions
3. Error handling with boto3
4. Credential verification

Requirements:
- AWS credentials configured
- boto3 installed
"""

import boto3
import sys
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError


def test_credentials():
    """Test if AWS credentials are properly configured."""
    try:
        # Create STS client to test credentials
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print("✅ AWS credentials are properly configured!")
        print(f"Account ID: {identity.get('Account')}")
        print(f"User ARN: {identity.get('Arn')}")
        print(f"User ID: {identity.get('UserId')}")
        return True
        
    except NoCredentialsError:
        print("❌ No AWS credentials found. Please configure your credentials.")
        print("   Run 'aws configure' or set environment variables.")
        return False
        
    except PartialCredentialsError:
        print("❌ Incomplete AWS credentials. Please check your configuration.")
        return False
        
    except ClientError as e:
        print(f"❌ Error accessing AWS: {e}")
        return False


def list_s3_buckets():
    """List all S3 buckets in the account."""
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        
        buckets = response.get('Buckets', [])
        if buckets:
            print(f"\n📦 Found {len(buckets)} S3 bucket(s):")
            for bucket in buckets:
                print(f"   - {bucket['Name']} (created: {bucket['CreationDate']})")
        else:
            print("\n📦 No S3 buckets found in this account.")
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDenied':
            print("❌ Access denied to S3. Check your IAM permissions.")
        else:
            print(f"❌ Error listing S3 buckets: {e}")


def list_ec2_regions():
    """List all available EC2 regions."""
    try:
        ec2 = boto3.client('ec2')
        response = ec2.describe_regions()
        
        regions = response.get('Regions', [])
        print(f"\n🌍 Available EC2 regions ({len(regions)}):")
        for region in regions:
            print(f"   - {region['RegionName']}")
            
    except ClientError as e:
        print(f"❌ Error listing EC2 regions: {e}")


def main():
    """Main function to run all tests."""
    print("🚀 Testing boto3 connectivity and basic operations...")
    print("=" * 50)
    
    # Test credentials first
    if not test_credentials():
        print("\n💡 To configure AWS credentials:")
        print("   1. Install AWS CLI: pip install awscli")
        print("   2. Run: aws configure")
        print("   3. Or set environment variables:")
        print("      - AWS_ACCESS_KEY_ID")
        print("      - AWS_SECRET_ACCESS_KEY")
        print("      - AWS_DEFAULT_REGION")
        sys.exit(1)
    
    # Run basic tests
    list_s3_buckets()
    list_ec2_regions()
    
    print("\n✨ boto3 test completed successfully!")
    print("\n💡 Next steps:")
    print("   - Explore more examples in this directory")
    print("   - Check the README.md for detailed documentation")
    print("   - Visit https://boto3.amazonaws.com/v1/documentation/api/latest/index.html")


if __name__ == "__main__":
    main()
