from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrap_linkedin.spiders.spider import LinkedinSpider
from data_functions import *

def ask_search()->str:
    return input("What search do you want to scraping?: ")

if __name__ == '__main__':
    # Obtenemos parametros configurados
    csv, json, file_name, results_limit, ordered_results, location_data = define_options()

    # Lanzamos el crawler.
    process = CrawlerProcess(get_project_settings())
    process.crawl(LinkedinSpider,  search=ask_search(), results_limit = results_limit, location_data = location_data)
    process.start() # Se bloquea acá hasta terminar

    dataframe = create_dataframe("linkedin_items.csv")

    if ordered_results:
        dataframe = order_jobs_by_post_date(dataframe)
    if csv:
        save_dataframe_as_csv(dataframe, f'{file_name}.csv')
    if json:
        save_dataframe_as_json(dataframe, f'{file_name}.json')
    delete_file("linkedin_items.csv")
