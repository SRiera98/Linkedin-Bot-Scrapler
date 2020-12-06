# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapLinkedinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_title = scrapy.Field()
    job_company = scrapy.Field()
    job_location = scrapy.Field()
    job_time = scrapy.Field()

    job_url = scrapy.Field()

    job_antiquity = scrapy.Field()
    job_type = scrapy.Field()
    job_sector = scrapy.Field()
    job_role = scrapy.Field()
