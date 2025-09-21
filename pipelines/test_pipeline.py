import sys
import os
# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zenml import pipeline
from src.steps.etl.get_or_create_user import get_or_create_user

@pipeline
def test_user_pipeline(user_name: str = "Chris Morris"):
    """Test pipeline for user creation."""
    user = get_or_create_user(user_name)
    return user

if __name__ == "__main__":
    test_user_pipeline()