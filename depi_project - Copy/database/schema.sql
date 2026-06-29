-- Aegis AI Database Schema for Supabase

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    points INTEGER DEFAULT 0,
    badge TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Departments table
CREATE TABLE IF NOT EXISTS departments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    icon TEXT,
    description TEXT,
    attempts INTEGER DEFAULT 0,
    score_sum INTEGER DEFAULT 0,
    correct INTEGER DEFAULT 0,
    risk_level INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scenarios table (training sessions)
CREATE TABLE IF NOT EXISTS scenarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    department_key TEXT,
    sector TEXT,
    difficulty TEXT NOT NULL,
    channel TEXT NOT NULL,
    sender_name TEXT,
    sender_handle TEXT,
    title TEXT,
    message TEXT,
    is_phishing BOOLEAN NOT NULL,
    user_classification BOOLEAN,
    selected_flags TEXT[],
    score INTEGER,
    correct BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Quiz results table (for senior citizen mode)
CREATE TABLE IF NOT EXISTS quiz_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    score INTEGER NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes (if they don't exist)
CREATE INDEX IF NOT EXISTS idx_users_points ON users(points DESC);
CREATE INDEX IF NOT EXISTS idx_scenarios_user_id ON scenarios(user_id);
CREATE INDEX IF NOT EXISTS idx_scenarios_department ON scenarios(department_key);
CREATE INDEX IF NOT EXISTS idx_scenarios_created_at ON scenarios(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_departments_risk ON departments(risk_level DESC);

-- Insert default departments (if they don't exist)
INSERT INTO departments (key, name, icon, description) VALUES
    ('accounting', 'Accounting', '💰', 'Fake invoices and urgent wire-transfer requests'),
    ('hr', 'Human Resources', '🗂️', 'Resumes and attachments carrying malware'),
    ('it', 'IT', '🖥️', 'Credential theft and privilege escalation attempts'),
    ('marketing', 'Marketing', '📣', 'Fake messages from ad agencies and partners'),
    ('sales', 'Sales', '📈', 'Fraudulent deals and contracts from fake prospects')
ON CONFLICT (key) DO NOTHING;

-- Create or replace function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers if they don't exist
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_departments_updated_at ON departments;
CREATE TRIGGER update_departments_updated_at BEFORE UPDATE ON departments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE scenarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_results ENABLE ROW LEVEL SECURITY;

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view their own data" ON users;
DROP POLICY IF EXISTS "Users can update their own data" ON users;
DROP POLICY IF EXISTS "Users can view their own scenarios" ON scenarios;
DROP POLICY IF EXISTS "Users can insert their own scenarios" ON scenarios;
DROP POLICY IF EXISTS "Anyone can view leaderboard" ON users;
DROP POLICY IF EXISTS "Anyone can view departments" ON departments;
DROP POLICY IF EXISTS "Anyone can update departments" ON departments;

-- Allow authenticated users to read/write their own data
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own data" ON users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view their own scenarios" ON scenarios
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own scenarios" ON scenarios
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Public read access for leaderboard
CREATE POLICY "Anyone can view leaderboard" ON users
    FOR SELECT USING (true);

-- Public read access for departments
CREATE POLICY "Anyone can view departments" ON departments
    FOR SELECT USING (true);

CREATE POLICY "Anyone can update departments" ON departments
    FOR UPDATE USING (true);
