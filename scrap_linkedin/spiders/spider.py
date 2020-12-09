import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrap_linkedin.items import ScrapLinkedinItem
from scrapy.exceptions import CloseSpider
from scrap_linkedin.utils.url_extractor import get_urls, get_total_jobs_aux
from tqdm import tqdm

class LinkedinSpider(CrawlSpider):
    def __init__(self, search: str, results_limit: int):
        self.__start_urls = get_urls(search)
        self.__results_limit = results_limit
        self.__total_jobs = get_total_jobs_aux(search)

        if self.__results_limit >= 999999:
            self.__progress_bar = tqdm(total=self.__total_jobs)
        elif self.__total_jobs < self.__results_limit:
            self.__progress_bar = tqdm(total=self.__total_jobs)
        elif self.__total_jobs >= self.__results_limit:
            self.__progress_bar = tqdm(total=int(self.__results_limit))
        self.__progress_bar.write("SCRAPING IN PROGRESS... (DON'T WORRY IF THE PROGRESS BAR DON'T REACH 100%)")
        self.__advance = 1
        super(LinkedinSpider, self).__init__()

    @property
    def get_all_urls(self) -> list:
        return self.__start_urls
    # URL a scrapear.
    start_urls = get_all_urls
    name = "linkedin"  # Para ejecutar desde consola
    item_count = 0
    allowed_domain = ['www.linkedin.com']  # Dominios permitidos
    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=['//*[@id="main-content"]/div/section/button'])), # Esto es para obtener mas resultados - No funciona.
        Rule(LinkExtractor(allow=(), restrict_xpaths=['//li[contains(@class,"result-card job-result-card result-card--with-hover-state")]/a']), callback='parse_item', follow=True)
    }

    def parse_item(self, response):
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
        items['job_sector'] = response.xpath('normalize-space(/html/body/main/section[1]/section[3]/ul/li[4]/span/text())').get()
        items['job_role'] = response.xpath('/html/body/main/section[1]/section[3]/ul/li[3]/span/text()').get()
        self.item_count += 1
        self.__progress_bar.update(self.__advance)
        if self.item_count > self.__results_limit:
            raise CloseSpider('LIMIT EXCEEDED!')
        yield items
