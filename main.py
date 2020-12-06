from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrap_linkedin.spiders.spider import LinkedinSpider

def ask_search()->str:
    return input("¿Que deseas buscar?: ")

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())

    # 'followall' is the name of one of the spiders of the project.
    process.crawl(LinkedinSpider,search=ask_search())
    process.start() # the script will block here until the crawling is finished