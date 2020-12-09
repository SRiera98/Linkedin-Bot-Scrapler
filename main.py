from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrap_linkedin.spiders.spider import LinkedinSpider
from data_functions import *

def ask_search()->str:
    return input("What search do you want to scraping?: ")

if __name__ == '__main__':
    csv, json, nombre, results_limit, ordered_results = define_options()

    process = CrawlerProcess(get_project_settings())
    process.crawl(LinkedinSpider,  search=ask_search(), results_limit = results_limit)
    process.start() # Se bloquea acá hasta terminar

    dataframe = create_dataframe("linkedin_items.csv")
    if ordered_results:
        dataframe = order_jobs_by_post_date(dataframe)
    if csv:
        save_dataframe_as_csv(dataframe, f'{nombre}.csv')
    if json:
        save_dataframe_as_json(dataframe, f'{nombre}.json')
    delete_file("linkedin_items.csv")
