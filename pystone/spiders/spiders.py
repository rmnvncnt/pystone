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
    user = Field()
    title = Field()
    deck_id = Field()
    deck_class = Field()

    # pipeline
    deck_set = Field()
    deck_format = Field()

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

        # user name
        item['user'] = response.css(
            'li.name a::text'
        ).extract_first()

        # title
        item['title'] = response.css(
            'h2[class*="deck-title"]::text'
        ).extract_first()

        # deck id
        item['deck_id'] = response.css(
            '*::attr(data-deck-id)'
        ).extract_first()

        # deck class
        item['deck_class'] = response.css(
            'span[itemprop=title]::text'
        ).extract()[2]

        # deck format
        item['deck_format'] = response.css(
            'p.is-wild::text'
        ).extract_first()

        yield item
