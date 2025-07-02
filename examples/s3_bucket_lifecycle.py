#!/usr/bin/env python3
"""
Comprehensive S3 Bucket and File Operations Example

This script demonstrates the complete lifecycle of S3 operations:
1. Create a test bucket
2. Upload a file to the bucket
3. List buckets to verify creation
4. List objects in the bucket
5. Download the file
6. Delete the file
7. Delete the bucket

Requirements:
- AWS credentials configured with S3 permissions
- boto3 installed
"""

import boto3
import os
import sys
import time
import tempfile
import argparse
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError, ProfileNotFound


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


class S3Manager:
    """A class to manage S3 operations with proper error handling."""
    
    def __init__(self, session, region='us-east-1'):
        """Initialize S3 client."""
        try:
            self.s3_client = session.client('s3', region_name=region)
            self.s3_resource = session.resource('s3', region_name=region)
            self.region = region
            print(f"✅ S3 client initialized for region: {region}")
        except NoCredentialsError:
            print("❌ AWS credentials not found. Please configure your credentials.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error initializing S3 client: {e}")
            sys.exit(1)
    
    def create_bucket(self, bucket_name):
        """Create an S3 bucket."""
        try:
            print(f"🔄 Creating bucket: {bucket_name}")
            
            # For us-east-1, don't specify LocationConstraint
            if self.region == 'us-east-1':
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.region}
                )
            
            # Wait for bucket to be created
            print("   Waiting for bucket to be created...")
            waiter = self.s3_client.get_waiter('bucket_exists')
            waiter.wait(Bucket=bucket_name)
            
            print(f"✅ Bucket '{bucket_name}' created successfully")
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'BucketAlreadyExists':
                print(f"❌ Bucket '{bucket_name}' already exists globally")
            elif error_code == 'BucketAlreadyOwnedByYou':
                print(f"ℹ️  Bucket '{bucket_name}' already exists and is owned by you")
                return True
            else:
                print(f"❌ Error creating bucket: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error creating bucket: {e}")
            return False
    
    def list_buckets(self):
        """List all S3 buckets."""
        try:
            print("🔄 Listing all S3 buckets...")
            response = self.s3_client.list_buckets()
            
            buckets = response.get('Buckets', [])
            if buckets:
                print(f"📦 Found {len(buckets)} bucket(s):")
                for bucket in buckets:
                    creation_date = bucket['CreationDate'].strftime('%Y-%m-%d %H:%M:%S')
                    print(f"   - {bucket['Name']} (created: {creation_date})")
            else:
                print("📦 No buckets found")
            
            return [bucket['Name'] for bucket in buckets]
            
        except ClientError as e:
            print(f"❌ Error listing buckets: {e}")
            return []
    
    def upload_file(self, bucket_name, local_file_path, s3_key=None):
        """Upload a file to S3 bucket."""
        try:
            if s3_key is None:
                s3_key = os.path.basename(local_file_path)
            
            print(f"🔄 Uploading '{local_file_path}' to bucket '{bucket_name}' as '{s3_key}'")
            
            # Upload with metadata
            self.s3_client.upload_file(
                local_file_path, 
                bucket_name, 
                s3_key,
                ExtraArgs={
                    'Metadata': {
                        'uploaded-by': 'boto3-examples',
                        'upload-timestamp': datetime.now().isoformat()
                    }
                }
            )
            
            print(f"✅ File uploaded successfully as '{s3_key}'")
            return True
            
        except FileNotFoundError:
            print(f"❌ Local file not found: {local_file_path}")
            return False
        except ClientError as e:
            print(f"❌ Error uploading file: {e}")
            return False
    
    def list_objects(self, bucket_name):
        """List all objects in a bucket."""
        try:
            print(f"🔄 Listing objects in bucket '{bucket_name}'...")
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            
            if 'Contents' in response:
                objects = response['Contents']
                print(f"📄 Found {len(objects)} object(s):")
                for obj in objects:
                    size_mb = obj['Size'] / (1024 * 1024)
                    modified = obj['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
                    print(f"   - {obj['Key']} ({size_mb:.2f} MB, modified: {modified})")
                
                return [obj['Key'] for obj in objects]
            else:
                print("📄 No objects found in bucket")
                return []
                
        except ClientError as e:
            print(f"❌ Error listing objects: {e}")
            return []
    
    def download_file(self, bucket_name, s3_key, local_file_path):
        """Download a file from S3."""
        try:
            print(f"🔄 Downloading '{s3_key}' from bucket '{bucket_name}' to '{local_file_path}'")
            
            self.s3_client.download_file(bucket_name, s3_key, local_file_path)
            
            print(f"✅ File downloaded successfully to '{local_file_path}'")
            return True
            
        except ClientError as e:
            print(f"❌ Error downloading file: {e}")
            return False
    
    def delete_object(self, bucket_name, s3_key):
        """Delete an object from S3."""
        try:
            print(f"🔄 Deleting object '{s3_key}' from bucket '{bucket_name}'")
            
            self.s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
            
            print(f"✅ Object '{s3_key}' deleted successfully")
            return True
            
        except ClientError as e:
            print(f"❌ Error deleting object: {e}")
            return False
    
    def delete_bucket(self, bucket_name):
        """Delete an S3 bucket (must be empty)."""
        try:
            print(f"🔄 Deleting bucket '{bucket_name}'")
            
            # Ensure bucket is empty first
            objects = self.list_objects(bucket_name)
            if objects:
                print(f"⚠️  Bucket contains {len(objects)} objects. Deleting them first...")
                for obj_key in objects:
                    self.delete_object(bucket_name, obj_key)
            
            # Delete the bucket
            self.s3_client.delete_bucket(Bucket=bucket_name)
            
            # Wait for bucket to be deleted
            print("   Waiting for bucket to be deleted...")
            waiter = self.s3_client.get_waiter('bucket_not_exists')
            waiter.wait(Bucket=bucket_name)
            
            print(f"✅ Bucket '{bucket_name}' deleted successfully")
            return True
            
        except ClientError as e:
            print(f"❌ Error deleting bucket: {e}")
            return False
    
    def bucket_exists(self, bucket_name):
        """Check if a bucket exists."""
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError:
            return False


def create_test_file():
    """Create a temporary test file for upload."""
    content = f"""This is a test file created for S3 operations demonstration.

Generated on: {datetime.now().isoformat()}
Purpose: Testing boto3 S3 upload/download functionality

Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.

This file will be:
1. Uploaded to S3
2. Listed in bucket contents
3. Downloaded back
4. Deleted from S3
5. Used to test bucket cleanup

End of test file.
"""
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_file.write(content)
    temp_file.close()
    
    print(f"📝 Created test file: {temp_file.name}")
    print(f"   File size: {len(content)} bytes")
    
    return temp_file.name


def main():
    """Main function demonstrating complete S3 workflow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Complete S3 bucket lifecycle demo')
    parser.add_argument('--profile', '-p', help='AWS profile name to use')
    parser.add_argument('--region', '-r', default='us-east-1', help='AWS region to use (default: us-east-1)')
    args = parser.parse_args()
    
    print("🚀 Starting S3 Bucket and File Operations Demo")
    print("=" * 55)
    
    # Create session with optional profile
    session = get_boto3_session(args.profile)
    if not session:
        sys.exit(1)
    
    # Initialize S3 manager
    s3_manager = S3Manager(session, args.region)
    
    # Generate unique bucket name (S3 bucket names must be globally unique)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    bucket_name = f"boto3-examples-test-{timestamp}"
    
    # Create test file
    test_file_path = create_test_file()
    test_file_name = os.path.basename(test_file_path)
    download_path = f"downloaded_{test_file_name}"
    
    try:
        print(f"\n🎯 Test bucket name: {bucket_name}")
        print(f"🎯 Test file: {test_file_name}")
        
        # Step 1: List buckets before creation
        print(f"\n{'='*20} BEFORE CREATION {'='*20}")
        initial_buckets = s3_manager.list_buckets()
        
        # Step 2: Create bucket
        print(f"\n{'='*25} CREATE BUCKET {'='*25}")
        if not s3_manager.create_bucket(bucket_name):
            print("❌ Failed to create bucket. Exiting.")
            sys.exit(1)
        
        # Step 3: Verify bucket creation
        print(f"\n{'='*20} VERIFY BUCKET CREATION {'='*20}")
        updated_buckets = s3_manager.list_buckets()
        if bucket_name in updated_buckets:
            print(f"✅ Bucket '{bucket_name}' confirmed in bucket list")
        else:
            print(f"❌ Bucket '{bucket_name}' not found in bucket list")
        
        # Step 4: Upload file
        print(f"\n{'='*25} UPLOAD FILE {'='*27}")
        if not s3_manager.upload_file(bucket_name, test_file_path):
            print("❌ Failed to upload file")
        
        # Step 5: List objects in bucket
        print(f"\n{'='*23} LIST BUCKET OBJECTS {'='*23}")
        objects = s3_manager.list_objects(bucket_name)
        
        # Step 6: Download file
        print(f"\n{'='*25} DOWNLOAD FILE {'='*26}")
        if objects and s3_manager.download_file(bucket_name, test_file_name, download_path):
            # Verify download
            if os.path.exists(download_path):
                download_size = os.path.getsize(download_path)
                original_size = os.path.getsize(test_file_path)
                print(f"✅ Download verification: {download_size} bytes (original: {original_size} bytes)")
                
                if download_size == original_size:
                    print("✅ File sizes match - download successful!")
                else:
                    print("⚠️  File sizes don't match")
        
        # Step 7: Delete file from S3
        print(f"\n{'='*24} DELETE S3 OBJECT {'='*24}")
        if objects:
            s3_manager.delete_object(bucket_name, test_file_name)
        
        # Step 8: Verify object deletion
        print(f"\n{'='*20} VERIFY OBJECT DELETION {'='*20}")
        remaining_objects = s3_manager.list_objects(bucket_name)
        if not remaining_objects:
            print("✅ Bucket is now empty")
        
        # Step 9: Delete bucket
        print(f"\n{'='*25} DELETE BUCKET {'='*26}")
        s3_manager.delete_bucket(bucket_name)
        
        # Step 10: Verify bucket deletion
        print(f"\n{'='*20} VERIFY BUCKET DELETION {'='*21}")
        if not s3_manager.bucket_exists(bucket_name):
            print(f"✅ Bucket '{bucket_name}' successfully deleted")
        else:
            print(f"❌ Bucket '{bucket_name}' still exists")
        
        # Final bucket list
        print(f"\n{'='*22} FINAL BUCKET LIST {'='*22}")
        final_buckets = s3_manager.list_buckets()
        
        print(f"\n🎉 S3 Operations Demo Completed Successfully!")
        print(f"📊 Summary:")
        print(f"   - Initial buckets: {len(initial_buckets)}")
        print(f"   - Final buckets: {len(final_buckets)}")
        print(f"   - Test bucket created and deleted: ✅")
        print(f"   - File uploaded and downloaded: ✅")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Operation interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        # Cleanup local files
        print(f"\n🧹 Cleaning up local files...")
        
        try:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
                print(f"✅ Removed test file: {test_file_path}")
        except Exception as e:
            print(f"⚠️  Could not remove test file: {e}")
        
        try:
            if os.path.exists(download_path):
                os.remove(download_path)
                print(f"✅ Removed downloaded file: {download_path}")
        except Exception as e:
            print(f"⚠️  Could not remove downloaded file: {e}")
        
        # Emergency cleanup: delete test bucket if it still exists
        try:
            if s3_manager.bucket_exists(bucket_name):
                print(f"🚨 Emergency cleanup: Removing bucket '{bucket_name}'...")
                s3_manager.delete_bucket(bucket_name)
        except Exception as e:
            print(f"⚠️  Emergency cleanup failed: {e}")
            print(f"   Please manually delete bucket '{bucket_name}' if it exists")


if __name__ == "__main__":
    main()
