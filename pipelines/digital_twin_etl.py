import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zenml import pipeline
from src.steps.etl.get_or_create_user import get_or_create_user
from src.steps.etl.crawl_links import crawl_links

@pipeline
def digital_twin_etl(
    user_full_name: str = "Chris Morris",
    links: list[str] = None

):
    """Full ETL pipeline using my webistes and accounts as a data source."""
    
    ## create user...
    user = get_or_create_user(user_full_name)
    

    ## crawl all my links...
    if links in None:
        links = [
               # GitHub Profile & Repositories
                "https://github.com/cmorris2945",
                "https://github.com/cmorris2945/Titanic-MLOps",  # current project
                # My other specific repos:
                "https://github.com/cmorris2945/ARGonaut",
                "https://github.com/cmorris2945/ML_ops_anime",
                "https://github.com/cmorris2945/ai_agent_research/tree/main/llm_research",
                "https://github.com/cmorris2945/ML_pipeliness",
                "https://github.com/cmorris2945/multi-transformer-serve-aws",
                "https://github.com/cmorris2945/ai_agents",
                
                # LinkedIn Profile
                "https://www.linkedin.com/in/c-r-7354a877/"
        ]

        crawled_data = crawl_links(user=user, links=links)

        return crawled_data
    
    if __name__ =="__main__":
        digital_twin_etl()