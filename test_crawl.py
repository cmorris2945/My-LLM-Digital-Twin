import sys
import os
sys.path.append('.')

print('??? Testing web crawling...')

try:
    from src.steps.etl.crawl_links import crawl_links
    print('? Crawl function imported')
    
    # Test with a simple, fast website
    test_links = ['https://httpbin.org/html']  # Simple test page
    
    print(' Testing crawl with simple URL...')
    result = crawl_links(test_links)
    print(f' Crawl completed: {type(result)}')
    
except Exception as e:
    print(f' Crawling error: {e}')
    import traceback
    traceback.print_exc()
