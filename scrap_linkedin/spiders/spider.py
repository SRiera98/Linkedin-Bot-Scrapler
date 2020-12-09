import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrap_linkedin.items import ScrapLinkedinItem
from scrapy.exceptions import CloseSpider
from scrap_linkedin.utils.url_extractor import get_urls


class LinkedinSpider(CrawlSpider):
    def __init__(self, search: str, results_limit: int):
        self.__start_urls = get_urls(search)
        self.__results_limit = results_limit
        super(LinkedinSpider, self).__init__()

    @property
    def get_all_urls(self) -> list:
        return self.__start_urls
    start_urls = get_all_urls
    name = "linkedin"  # Para ejecutar desde consola
    item_count = 0
    allowed_domain = ['www.linkedin.com']  # Dominios permitidos
    # URL a scrapear.
    #start_urls = ['http://www.linkedin.com/jobs/search?keywords=Python&locationId=ar:0&start=0&count=25&trk=jobs_jserp_pagination_1']
    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=['//*[@id="main-content"]/div/section/button'])), # Esto es para obtener mas resultados - No funciona.
        Rule(LinkExtractor(allow=(), restrict_xpaths=['//li[contains(@class,"result-card job-result-card result-card--with-hover-state")]/a']), callback='parse_item', follow=True)
    }

    def parse_item(self, response):
        print(f"PROCESANDO : {response.url}\n\n\n")
        items = ScrapLinkedinItem()
        items['job_title'] = response.xpath(
            '/html/body/main/section[1]/section[2]/div[1]/div[1]/h1/text()').get()
        items['job_company'] = response.xpath(
            '/html/body/main/section[1]/section[2]/div[1]/div[1]/h3[1]/span[1]/text() | /html/body/main/section[1]/section[2]/div[1]/div[1]/h3[1]/span[1]/a/text()').get(default="NULL")
        items['job_location'] = response.xpath(
            '/html/body/main/section[1]/section[2]/div[1]/div[1]/h3[1]/span[2]/text()').get()
        items['job_time'] = response.xpath(
            '/html/body/main/section[1]/section[2]/div[1]/div[1]/h3[2]/span[1]/text()').get()
        items['job_url'] = response.url
        items['job_antiquity'] = response.xpath('/html/body/main/section[1]/section[3]/ul/li[1]/span/text()').get()
        items['job_type'] = response.xpath('/html/body/main/section[1]/section[3]/ul/li[2]/span/text()').get()
        items['job_sector'] = response.xpath('/html/body/main/section[1]/section[3]/ul/li[4]/span/text()').get()
        items['job_role'] = response.xpath('/html/body/main/section[1]/section[3]/ul/li[3]/span/text()').get()
        self.item_count += 1
        if self.item_count > self.__results_limit:
            raise CloseSpider('item_exceeded')
        yield items
