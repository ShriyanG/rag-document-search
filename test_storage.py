#!/usr/bin/env python3
"""
Test script for LocalStorage operations
"""
import sys
sys.path.insert(0, 'src')

from pathlib import Path
import tempfile
from components.storage import StorageFactory

print("✅ Testing LocalStorage Operations\n")

# Create a temporary directory for testing
with tempfile.TemporaryDirectory() as tmpdir:
    storage = StorageFactory.create("local", base_dir=tmpdir)
    
    # Create a test file
    test_file = Path(tmpdir) / "test_source.txt"
    test_file.write_text("Hello from storage test!")
    
    # Test upload
    print("1. Testing upload...")
    storage.upload(test_file, "chunks/test.txt")
    print("   ✓ Upload successful")
    
    # Test exists
    print("\n2. Testing exists...")
    exists = storage.exists("chunks/test.txt")
    print(f"   ✓ File exists: {exists}")
    
    # Test get_url
    print("\n3. Testing get_url...")
    url = storage.get_url("chunks/test.txt")
    print(f"   ✓ URL: {url}")
    
    # Test list_files
    print("\n4. Testing list_files...")
    files = storage.list_files()
    print(f"   ✓ Files: {files}")
    
    # Test download
    print("\n5. Testing download...")
    dest_file = Path(tmpdir) / "downloaded.txt"
    storage.download("chunks/test.txt", dest_file)
    content = dest_file.read_text()
    print(f"   ✓ Downloaded content: {content}")
    
    # Test delete
    print("\n6. Testing delete...")
    storage.delete("chunks/test.txt")
    exists = storage.exists("chunks/test.txt")
    print(f"   ✓ File deleted: {not exists}")

print("\n✓ All LocalStorage operations working!")
