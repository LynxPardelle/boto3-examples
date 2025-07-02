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
import os
import argparse
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError, ProfileNotFound


def get_boto3_session(profile_name=None):
    """Create a boto3 session with optional profile support."""
    try:
        if profile_name:
            print(f"🔑 Using AWS profile: {profile_name}")
            session = boto3.Session(profile_name=profile_name)
        else:
            # Check if AWS_PROFILE environment variable is set
            env_profile = os.environ.get('AWS_PROFILE')
            if env_profile:
                print(f"🔑 Using AWS profile from environment: {env_profile}")
                session = boto3.Session(profile_name=env_profile)
            else:
                print("🔑 Using default AWS credentials")
                session = boto3.Session()
        
        return session
    
    except ProfileNotFound as e:
        print(f"❌ AWS profile not found: {e}")
        print("   Available profiles can be listed with: aws configure list-profiles")
        return None


def test_credentials(session):
    """Test if AWS credentials are properly configured."""
    try:
        # Create STS client to test credentials
        sts = session.client('sts')
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


def list_s3_buckets(session):
    """List all S3 buckets in the account."""
    try:
        s3 = session.client('s3')
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


def list_ec2_regions(session):
    """List all available EC2 regions."""
    try:
        ec2 = session.client('ec2')
        response = ec2.describe_regions()
        
        regions = response.get('Regions', [])
        print(f"\n🌍 Available EC2 regions ({len(regions)}):")
        for region in regions:
            print(f"   - {region['RegionName']}")
            
    except ClientError as e:
        print(f"❌ Error listing EC2 regions: {e}")


def main():
    """Main function to run all tests."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test boto3 connectivity and basic operations')
    parser.add_argument('--profile', '-p', help='AWS profile name to use')
    parser.add_argument('--list-profiles', action='store_true', 
                       help='List available AWS profiles and exit')
    args = parser.parse_args()
    
    # List profiles if requested
    if args.list_profiles:
        try:
            available_profiles = boto3.Session().available_profiles
            if available_profiles:
                print("� Available AWS profiles:")
                for profile in available_profiles:
                    print(f"   - {profile}")
            else:
                print("📋 No AWS profiles configured")
        except Exception as e:
            print(f"❌ Error listing profiles: {e}")
        return
    
    print("�🚀 Testing boto3 connectivity and basic operations...")
    print("=" * 50)
    
    # Create session with optional profile
    session = get_boto3_session(args.profile)
    if not session:
        sys.exit(1)
    
    # Test credentials first
    if not test_credentials(session):
        print("\n💡 To configure AWS credentials:")
        print("   1. Install AWS CLI: pip install awscli")
        print("   2. Run: aws configure")
        print("   3. Or set environment variables:")
        print("      - AWS_ACCESS_KEY_ID")
        print("      - AWS_SECRET_ACCESS_KEY")
        print("      - AWS_DEFAULT_REGION")
        print("   4. Or use profiles: aws configure --profile myprofile")
        sys.exit(1)
    
    # Run basic tests
    list_s3_buckets(session)
    list_ec2_regions(session)
    
    print("\n✨ boto3 test completed successfully!")
    print("\n💡 Next steps:")
    print("   - Explore more examples in this directory")
    print("   - Check the README.md for detailed documentation")
    print("   - Visit https://boto3.amazonaws.com/v1/documentation/api/latest/index.html")
    print("\n💡 Profile usage:")
    print("   - Use --profile PROFILE_NAME to specify a profile")
    print("   - Use --list-profiles to see available profiles")
    print("   - Set AWS_PROFILE environment variable to use a default profile")


if __name__ == "__main__":
    main()
