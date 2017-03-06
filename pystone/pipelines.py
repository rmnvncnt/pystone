# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pandas.io.json import json_normalize
from w3lib.html import replace_escape_chars

import dateparser
import re
import os
import json

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

        return None

    def process_item(self, item, spider):

        # clean date
        raw_date = item['date'].split()
        item['date'] = dateparser.parse(raw_date[0])

        # set
        item['deck_set'] = re.findall('\w+', ''.join(raw_date[1]))

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

        # craft cost
        item['craft_cost'] = int(item['craft_cost'])

        return item
