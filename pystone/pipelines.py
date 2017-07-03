# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pandas.io.json import json_normalize
from w3lib.html import replace_escape_chars
from scrapy.exceptions import DropItem

import dateparser, re, os, json

class CleanCardsPipeline(object):

    def __init__ (self):
        self.card_list = self.loadcards()

    def loadcards (self):

        with open('cards.json') as f:
            card_list = json.load(f)

        return card_list

    def get_card_id(self, name):

        for card in self.card_list:
            if card.get('name') == name:
                return card['dbfId']

        raise DropItem("Unknown card")

    def process_item(self, item, spider):

        # clean date
        raw_date = item['date'].split()
        item['date'] = dateparser.parse(raw_date[0])

        # user
        item['user'] = replace_escape_chars(item['user'])

        # set
        item['deck_set'] = re.sub('[()]', '', ' '.join(raw_date[1:]))

        # deck rating
        item['rating'] = int(re.findall('\d+', item['rating'])[0])

        # deck count
        item['count'] = list(map(int, item['count']))

        # replace card names by unique ids
        for i, card in enumerate(item['cards']):
            card_name_raw = replace_escape_chars(card)
            card_name_clean = ' '.join(card_name_raw.split())
            item['cards'][i] = self.get_card_id(card_name_clean)

        # multiply ids by card counts
        id_list = []
        for i, j in zip(item['cards'], item['count']):
            id_list.extend([i] * j)

        # replace by list of ids
        item['cards'] = id_list

        # deck id
        item['deck_id'] = int(item['deck_id'])

        # craft cost
        item['craft_cost'] = int(item['craft_cost'])

        # deck format
        if item['deck_format']:
            item['deck_format'] = 'W' # wild
        else:
            item['deck_format'] = 'S' # standard

        # check if 30 cards in deck
        if len(item['cards']) != 30:
            raise DropItem("Incomplete deck")

        # remove count
        del item['count']

        return item
