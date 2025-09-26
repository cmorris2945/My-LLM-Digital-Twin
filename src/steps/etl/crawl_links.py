from urllib.parse import urlparse

from loguru import logger
from tqdm import tqdm
from zenml import get_step_context, step

from llm_engineering.application.crawlers.dispatcher import CrawlerDispatcher
from llm_engineering.domain.documents import UserDocument


@step
def crawl_links(user: UserDocument, links: list[str]) -> Annotated[List[str], "crawled_links"]:

    dispatcher = CrawlerDispatcher.build().register_linkedin().register_medium().register_github()

    logger.info(f"Starting to crawl you meathead... {len(links)} link(s).")

    metadata = {}
    successful_crawls = 0
    for link in tqdm(links):
        successfull_crawl, crawled_domain = _crawl_link(dispatcher, link, user)
        successfull_crawls += successfull_crawl
        
        metadata = _add_to_metadata(metadata, crawled_domain, successfull_crawl)

    step_context = get_step_context()
    step_context.add_output_metadata(output_name="crawled_links", metadata=metadata)

    logger.info(f"Successfully crawled your stupid hole, 'Mack'. This...{successfull_crawls} / {len(links)} links.")

    return links

def _crawl_link(dispatcher:CrawlerDispatcher, link:str, user: UserDocument) -> tuple[bool,str]:

    crawler = dispatcher.get_crawler(link)
    crawler_domain = urlparse(link).netloc

    try:
        crawler.extract(lin=link, user=user)

        return(True, crawler_domain)

    except Exception as e:
        logger.error(f"An error occurred while crawling: {e!s}")

        return (False, crawler_domain)
    
def _add_to_metadata(metadata:dict, domain:str, successfull_crawl:bool) -> dict:
    if domain not in metadata:
        metadata[domain] = {}
    metadata[domain]["successful"] = metadata[domain].get("successful", 0) + successfull_crawl
    metadata[domain]["total"] = metadata[domain].get("total",0) +1

    return metadata

