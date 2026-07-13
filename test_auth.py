#!/usr/bin/env python3
"""Test authentication endpoints"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_register():
    """Test user registration"""
    try:
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "test123456",
            "role": "individual"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        print(f"Register: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Registration successful: {data['user']['name']}")
            return data['access_token']
        else:
            print(f"Registration error: {response.text}")
            return None
    except Exception as e:
        print(f"Registration failed: {e}")
        return None

def test_login():
    """Test user login"""
    try:
        login_data = {
            "username": "test@example.com",
            "password": "test123456"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", data=login_data)
        print(f"Login: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Login successful: {data['user']['name']}")
            return data['access_token']
        else:
            print(f"Login error: {response.text}")
            return None
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def test_me(token):
    """Test /me endpoint"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"Me endpoint: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Current user: {data['name']} ({data['role']})")
            return True
        else:
            print(f"Me endpoint error: {response.text}")
            return False
    except Exception as e:
        print(f"Me endpoint failed: {e}")
        return False

def main():
    print("Testing Aegis AI Authentication...")
    print("=" * 40)
    
    # Test health
    if not test_health():
        print("Backend is not running!")
        return
    
    # Test registration
    token = test_register()
    if not token:
        # Try login instead (user might already exist)
        token = test_login()
    
    if token:
        # Test /me endpoint
        test_me(token)
        print("\nAuthentication tests completed successfully!")
    else:
        print("\nAuthentication tests failed!")

if __name__ == "__main__":
    main()