"""
Setup Supabase Database
Run this script to create tables and seed data
"""
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_KEY must be set in .env")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_tables():
    """Read and execute schema.sql"""
    print("📊 Creating database tables...")
    
    with open("database/schema.sql", "r") as f:
        schema = f.read()
    
    print("✅ Schema loaded. Please run this SQL in Supabase SQL Editor:")
    print("\nGo to: https://supabase.com/dashboard/project/_/sql")
    print("\nCopy and paste the following:\n")
    print("-" * 60)
    print(schema)
    print("-" * 60)

def seed_data():
    """Insert sample data"""
    print("\n🌱 Seeding sample data...")
    
    # Sample users
    users = [
        {"name": "Mona Abdallah", "points": 260},
        {"name": "Youssef El-Sherif", "points": 140},
        {"name": "Sara Kamal", "points": 60}
    ]
    
    try:
        for user in users:
            supabase.table("users").insert(user).execute()
        print("✅ Sample users created")
    except Exception as e:
        print(f"⚠️  Users might already exist: {e}")

if __name__ == "__main__":
    print("🚀 Aegis AI Database Setup\n")
    create_tables()
    
    response = input("\n⏸️  Have you run the SQL in Supabase? (y/n): ")
    if response.lower() == 'y':
        seed_data()
        print("\n✅ Database setup complete!")
    else:
        print("\n⏹️  Run the SQL first, then run this script again.")
