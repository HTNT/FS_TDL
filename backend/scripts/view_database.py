"""
Script để xem dữ liệu trong database
Chạy: python scripts/view_database.py
"""
import sys
from pathlib import Path

# Thêm thư mục parent vào path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.user import User

def view_database():
    print("=" * 60)
    print("XEM DATABASE")
    print("=" * 60)
    
    # Kết nối database
    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Lấy thông tin các bảng
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n📊 Số bảng trong database: {len(tables)}")
        print(f"Danh sách bảng: {', '.join(tables)}\n")
        
        # Xem dữ liệu bảng users
        print("👥 BẢNG USERS:")
        print("-" * 60)
        
        users = session.query(User).all()
        
        if not users:
            print("⚠️  Chưa có user nào trong database")
        else:
            print(f"Tổng số users: {len(users)}\n")
            
            for i, user in enumerate(users, 1):
                print(f"User #{i}:")
                print(f"  ID: {user.id}")
                print(f"  Username: {user.username}")
                print(f"  Email: {user.email}")
                print(f"  Active: {'✅' if user.is_active else '❌'}")
                print(f"  Superuser: {'✅' if user.is_superuser else '❌'}")
                print(f"  Created: {user.created_at}")
                print()
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    view_database()
