#!/usr/bin/env python
"""
Script to setup media table without losing existing data
Run: python setup_media_table.py
"""

import os
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.db.base import Base
from app.models.media import Media

def setup_media_table():
    """Create media table if it doesn't exist"""
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    
    try:
        # Check if table exists
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='media')")
            )
            table_exists = result.scalar()
        
        if table_exists:
            print("✅ Media table already exists")
            return
        
        # Create only media table
        print("Creating media table...")
        Media.__table__.create(engine, checkfirst=True)
        print("✅ Media table created successfully")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    setup_media_table()
