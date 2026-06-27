from datetime import datetime
import random
import string

def generate_user_id() -> str:
    """
    Generate user_id in format: yymmddxxxxxx
    - yy: last 2 digits of year
    - mm: month (01-12)
    - dd: day (01-31)
    - xxxx: 6 random digits
    """
    now = datetime.utcnow()
    yy = now.strftime("%y")
    mm = now.strftime("%m")
    dd = now.strftime("%d")
    
    # Generate 6 random digits
    random_part = ''.join(random.choices(string.digits, k=6))
    
    user_id = f"{yy}{mm}{dd}{random_part}"
    return user_id
