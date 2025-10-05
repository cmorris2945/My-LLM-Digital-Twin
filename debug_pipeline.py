import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print('?? Starting debug pipeline...')

try:
    print('?? Testing imports...')
    from llm_engineering.domain.documents import UserDocument
    print(' UserDocument imported')
    
    from llm_engineering.infrastructure.db.mongo import connection
    from llm_engineering.settings import settings
    print(' MongoDB connection imported')
    
    print(' Creating user...')
    user = UserDocument(first_name='Chris', last_name='Morris')
    print(f' User created: {user.full_name}')
    
    print(' Saving user to MongoDB...')
    saved_user = user.save()
    print(' User saved successfully!')
    
    print(' Checking MongoDB collections...')
    db = connection[settings.DATABASE_NAME]
    collections = db.list_collection_names()
    print(f' Collections: {collections}')
    
    for col in collections:
        count = db[col].count_documents({})
        print(f' {col}: {count} documents')
    
    print(' Basic pipeline test completed successfully!')
    
except Exception as e:
    print(f' Error: {e}')
    import traceback
    traceback.print_exc()
