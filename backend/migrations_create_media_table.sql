-- Migration: Create media table for post attachments
-- Run this SQL if you're not using Alembic migrations

CREATE TABLE IF NOT EXISTS media (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_media_post_id ON media(post_id);
