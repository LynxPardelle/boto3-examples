#!/usr/bin/env python3
"""
Run All Examples Script

This script runs all the example scripts in sequence to demonstrate
the full capabilities of the boto3-examples project.

Requirements:
- AWS credentials configured
- boto3 installed
- All example scripts present
"""

import os
import sys
import subprocess
import time
import argparse
from pathlib import Path


def run_example(script_name, description, profile=None):
    """Run an example script and return success status."""
    print(f"\n{'='*60}")
    print(f"🚀 Running: {description}")
    print(f"📄 Script: {script_name}")
    if profile:
        print(f"🔑 Profile: {profile}")
    print('='*60)
    
    script_path = Path("examples") / script_name
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        # Run with the virtual environment Python
        if os.name == 'nt':  # Windows
            python_path = ".venv\\Scripts\\python.exe"
        else:  # Unix-like
            python_path = ".venv/bin/python"
        
        # Build command with optional profile
        cmd = [python_path, str(script_path)]
        if profile:
            cmd.extend(['--profile', profile])
        
        result = subprocess.run(
            cmd,
            capture_output=False,  # Show output in real-time
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✅ {description} completed successfully!")
            return True
        else:
            print(f"\n❌ {description} failed with exit code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error running {script_name}: {e}")
        return False


def main():
    """Run all example scripts."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run all boto3 examples')
    parser.add_argument('--profile', '-p', help='AWS profile name to use for all examples')
    parser.add_argument('--interactive', '-i', action='store_true', default=True,
                       help='Prompt before running examples (default: True)')
    parser.add_argument('--no-interactive', dest='interactive', action='store_false',
                       help='Run all examples without prompting')
    args = parser.parse_args()
    
    print("🎯 boto3-examples: Running All Examples")
    print("=" * 60)
    print("This will run all example scripts to demonstrate boto3 capabilities.")
    print("Make sure your AWS credentials are configured before proceeding.")
    if args.profile:
        print(f"🔑 Using AWS profile: {args.profile}")
    print()
    
    # Check if we're in the right directory
    if not Path("examples").exists():
        print("❌ Examples directory not found. Please run this script from the project root.")
        sys.exit(1)
    
    # List of examples to run
    examples = [
        ("test_connection.py", "AWS Connection Test"),
        ("simple_s3_operations.py", "Simple S3 Operations"),
        ("s3_bucket_lifecycle.py", "Complete S3 Lifecycle Demo")
    ]
    
    print(f"📋 Will run {len(examples)} examples:")
    for i, (script, desc) in enumerate(examples, 1):
        print(f"   {i}. {desc}")
    
    if args.interactive:
        print("\n" + "=" * 60)
        input("Press Enter to continue, or Ctrl+C to cancel...")
    
    # Run each example
    results = []
    start_time = time.time()
    
    for script_name, description in examples:
        success = run_example(script_name, description, args.profile)
        results.append((script_name, description, success))
        
        # Add a pause between examples
        if script_name != examples[-1][0]:  # Not the last example
            print("\n" + "-" * 40)
            print("⏸️  Pausing for 3 seconds before next example...")
            time.sleep(3)
    
    # Summary
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print("📊 SUMMARY OF ALL EXAMPLES")
    print('='*60)
    
    successful = 0
    for script_name, description, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {description}")
        if success:
            successful += 1
    
    print(f"\n🎯 Results: {successful}/{len(examples)} examples completed successfully")
    print(f"⏱️  Total time: {duration:.1f} seconds")
    
    if successful == len(examples):
        print("\n🎉 All examples completed successfully!")
        print("   Your boto3 environment is fully functional!")
        print("\n💡 Next steps:")
        print("   - Explore the example code to understand boto3 patterns")
        print("   - Modify the examples for your own use cases")
        print("   - Check out the AWS documentation for more services")
    else:
        print(f"\n⚠️  {len(examples) - successful} example(s) failed.")
        print("   Please check your AWS credentials and permissions.")
        print("   Review the error messages above for troubleshooting.")
    
    print(f"\n📚 Resources:")
    print("   - Project README: README.md")
    print("   - Boto3 docs: https://boto3.amazonaws.com/v1/documentation/api/latest/")
    print("   - AWS docs: https://docs.aws.amazon.com/")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")
        print("Thank you for trying boto3-examples!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
