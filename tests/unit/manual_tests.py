import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from llm_engineering.application import utils
from llm_engineering.domain.documents import UserDocument

def create_or_get_user(user_full_name: str) -> UserDocument:
    first, last = utils.split_user_full_name(user_full_name)
    return UserDocument.get_or_create(first, last)

if __name__ == "__main__":
    user = create_or_get_user("Chris Morris")
    print(user)
    print(user.id)
    print(user.full_name)