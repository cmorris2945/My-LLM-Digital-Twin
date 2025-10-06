
from src.steps.etl.get_or_create_user import get_or_create_user
from src.steps.etl.crawl_links import crawl_links

# Fixed URLs
links = ['https://github.com/cmorris2945/ARGonaut', 'https://github.com/cmorris2945/ML_ops_anime', 'https://github.com/cmorris2945/ML_pipeliness', 'https://github.com/cmorris2945/multi-transformer-serve-aws', 'https://github.com/cmorris2945/ai_agents', 'https://github.com/cmorris2945/ai_agent_research']

print('Running with fixed URLs...')
user = get_or_create_user('Chris Morris')
result = crawl_links(user, links)
print(f'Result: {result}')
