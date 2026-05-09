-- Grade Smart Database Initialization Script
-- Database: PostgreSQL
-- Description: Core schema for user accounts, exam templates, grading batches, and test results.

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Role Enum
CREATE TYPE user_role AS ENUM ('admin', 'user');

-- Users Table
CREATE TABLE users (
    id_user UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(150) NOT NULL DEFAULT '',
    gender VARCHAR(20) DEFAULT '',
    password TEXT NOT NULL,
    role user_role DEFAULT 'user'
);

-- Templates Table
CREATE TABLE templates (
    id_template UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    link_image TEXT NOT NULL, -- URL to the template image on storage
    total_questions INTEGER DEFAULT 0,
    type VARCHAR(50) DEFAULT ''
);

-- Batches Table
CREATE TABLE batches (
    id_batch UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_user UUID NOT NULL REFERENCES users(id_user) ON DELETE CASCADE,
    id_template UUID REFERENCES templates(id_template) ON DELETE SET NULL,
    name VARCHAR(100) NOT NULL,
    time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tests Table (Results)
CREATE TABLE tests (
    id_test UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_batch UUID NOT NULL REFERENCES batches(id_batch) ON DELETE CASCADE,
    id_student VARCHAR(50),
    test_code VARCHAR(50),
    image_url TEXT NOT NULL, -- URL to the specific scanned paper
    score FLOAT DEFAULT 0.0,
    status VARCHAR(50)
);

-- Indices for performance
CREATE INDEX idx_batches_user ON batches(id_user);
CREATE INDEX idx_tests_batch ON tests(id_batch);
CREATE INDEX idx_batches_template ON batches(id_template);

-- Seed Data
INSERT INTO users (username, email, full_name, gender, password, role) VALUES 
('user1', 'user1@example.com', 'Nguyễn Văn A', 'male', '$2a$10$WaTyv1Rhk9OT216DfQeU8.Y241FDT/n5I8RYmaGlBcIUhKzxtdO8u', 'user'),
('user2', 'user2@example.com', 'Trần Thị B', 'female', '$2a$10$WaTyv1Rhk9OT216DfQeU8.Y241FDT/n5I8RYmaGlBcIUhKzxtdO8u', 'user'),
('user3', 'user3@example.com', 'Lê Văn C', 'male', '$2a$10$WaTyv1Rhk9OT216DfQeU8.Y241FDT/n5I8RYmaGlBcIUhKzxtdO8u', 'user');
