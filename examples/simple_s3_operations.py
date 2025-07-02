#!/usr/bin/env python3
"""
Simple S3 Operations Example

A simpler version of S3 operations for learning purposes.
This script demonstrates basic S3 operations step by step.

Requirements:
- AWS credentials configured with S3 permissions
- boto3 installed
"""

import boto3
import tempfile
import os
from datetime import datetime
from botocore.exceptions import ClientError


def main():
    """Demonstrate basic S3 operations."""
    print("🪣 Simple S3 Operations Example")
    print("=" * 35)
    
    # Create S3 client
    try:
        s3 = boto3.client('s3')
        print("✅ S3 client created")
    except Exception as e:
        print(f"❌ Error creating S3 client: {e}")
        return
    
    # Generate unique bucket name
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    bucket_name = f"simple-boto3-test-{timestamp}"
    
    print(f"🎯 Using bucket name: {bucket_name}")
    
    try:
        # 1. Create bucket
        print("\n1️⃣  Creating bucket...")
        s3.create_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' created")
        
        # 2. Create a test file
        print("\n2️⃣  Creating test file...")
        test_content = f"Hello from boto3! Created at {datetime.now()}"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            test_file_path = f.name
        
        file_name = "test-file.txt"
        print(f"✅ Test file created: {file_name}")
        
        # 3. Upload file
        print("\n3️⃣  Uploading file to bucket...")
        s3.upload_file(test_file_path, bucket_name, file_name)
        print(f"✅ File uploaded to bucket")
        
        # 4. List buckets
        print("\n4️⃣  Listing all buckets...")
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        print(f"✅ Found {len(buckets)} bucket(s)")
        
        if bucket_name in buckets:
            print(f"✅ Our bucket '{bucket_name}' is in the list!")
        
        # 5. List objects in bucket
        print("\n5️⃣  Listing objects in our bucket...")
        response = s3.list_objects_v2(Bucket=bucket_name)
        
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"   📄 {obj['Key']} ({obj['Size']} bytes)")
        
        # 6. Download file
        print("\n6️⃣  Downloading file...")
        download_path = "downloaded-test-file.txt"
        s3.download_file(bucket_name, file_name, download_path)
        print(f"✅ File downloaded to: {download_path}")
        
        # Verify download
        with open(download_path, 'r') as f:
            downloaded_content = f.read()
        
        if downloaded_content == test_content:
            print("✅ Download verified - content matches!")
        
        # 7. Delete file from bucket
        print("\n7️⃣  Deleting file from bucket...")
        s3.delete_object(Bucket=bucket_name, Key=file_name)
        print(f"✅ File '{file_name}' deleted from bucket")
        
        # 8. Delete bucket
        print("\n8️⃣  Deleting bucket...")
        s3.delete_bucket(Bucket=bucket_name)
        print(f"✅ Bucket '{bucket_name}' deleted")
        
        print("\n🎉 All operations completed successfully!")
        
    except ClientError as e:
        print(f"❌ AWS Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Cleanup local files
        try:
            if 'test_file_path' in locals() and os.path.exists(test_file_path):
                os.remove(test_file_path)
            if os.path.exists("downloaded-test-file.txt"):
                os.remove("downloaded-test-file.txt")
            print("🧹 Local files cleaned up")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")


if __name__ == "__main__":
    main()
