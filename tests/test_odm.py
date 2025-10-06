try:
    from llm_engineering.domain.base.nosql import NoSQLBaseDocument
    print('✅ ODM base class imported successfully')
    print(f'Base class: {NoSQLBaseDocument.__name__}')
    
    # Get methods without using backslash in f-string
    methods = [method for method in dir(NoSQLBaseDocument) if not method.startswith('_')]
    print(f'Methods: {methods}')
    
    print('\n Key ODM Features:')
    key_methods = ['save', 'find', 'get_or_create', 'bulk_insert', 'bulk_find', 'to_mongo', 'from_mongo']
    for method in key_methods:
        if method in methods:
            print(f'   {method}')
        else:
            print(f'   {method}')
            
except Exception as e:
    print(f' Import error: {e}')
    import traceback
    traceback.print_exc()
