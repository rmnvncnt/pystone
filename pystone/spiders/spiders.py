from scrapy.spiders import SitemapSpider
from scrapy import Item, Field

class DeckItem(Item):

    date = Field()
    cards = Field()
    count = Field()
    deck_type = Field()
    deck_archetype = Field()
    rating = Field()
    craft_cost = Field()

    # pipeline
    deck_set = Field()

class HearthPwnSpider(SitemapSpider):

    name = 'hpspider'
    allowed_domains = ['www.hearthpwn.com']
    sitemap_urls = ['http://www.hearthpwn.com/sitemap.xml']
    sitemap_follow = [('hsdeck')]
    sitemap_rules = [('/decks/', 'parse_item')]

    def parse_item(self, response):
        
        item = DeckItem()

        # deck creation date
        item['date'] = response.xpath(
            "//li[contains(text(), 'Created')]/span/text()"
        ).extract_first()
        
        # card names
        item['cards'] = response.css(
            'aside [data-id]::text'
        ).extract()
        
        # card count
        item['count'] = response.css(
            'aside *::attr(data-count)'
        ).extract()

        # deck type
        item['deck_type'] = response.xpath(
            "//li[contains(text(), 'Deck Type')]/span/text()"
        ).extract_first()

        # deck archetype
        item['deck_archetype'] = response.css(
            'a[href*=archetype]::text'
        ).extract_first()

        # deck rating
        item['rating'] = response.css(
            'div[class~="rating-sum"]::text'
        ).extract_first()

        # craft cost
        item['craft_cost'] = response.css(
            "span.craft-cost::text"
        ).extract_first()

        yield item
