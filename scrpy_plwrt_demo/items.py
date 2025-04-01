# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ThesisItem(scrapy.Item):
    title=scrapy.Field()
    issue_year=scrapy.Field()
    abstract=scrapy.Field()
    link=scrapy.Field()

