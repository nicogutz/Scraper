import json
import os
import pathlib
import re

import scrapy
import urllib3


class DataScraper(scrapy.Spider):
    name = "data"
    http = urllib3.PoolManager()

    def start_requests(self):
        urls = []
        with open(os.path.dirname(__file__) + '/../links_new.json', 'r') as fr:
            urls = json.load(fr)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        main_shell = response.css('[id="mainShell"]')
        main_text = main_shell.css('article p::text').getall()

        relative_dir_list = response.url.split("/")[3:]
        joined_dir = ""

        for folder in relative_dir_list:
            joined_dir = joined_dir + folder + '/'

        classification_table = main_shell.css('table td strong::text, table td a::text').getall()

        table_indexes = [i for i, item in enumerate(classification_table) if
                         re.search('Utility:|Mechanics:|Force:', item)]

        titles_and_lists = main_shell.css(
            'article p strong::text, article p a strong::text , article li a::text').getall()
        try:
            target_index = titles_and_lists.index('Target')
            syn_index = titles_and_lists.index('Synergists')
            stab_index = min([i for i, item in enumerate(titles_and_lists) if re.search('Stabilizer', item)])

            target_muscles = titles_and_lists[target_index + 1:syn_index]
            synergist_muscles = titles_and_lists[syn_index + 1: stab_index]

        except ValueError:
            target_muscles = None
            synergist_muscles = None

        try:
            utility = classification_table[table_indexes[0] + 1: table_indexes[1]],
        except IndexError:
            utility = None

        try:
            mechanics = classification_table[table_indexes[1] + 1: table_indexes[2]],
        except IndexError:
            mechanics = None

        try:
            force = classification_table[table_indexes[2] + 1: table_indexes[2] + 2],
        except IndexError:
            force = None
            
        yield {
            relative_dir_list[-1]: {
                'name': response.css('[id="headerShell"] [class="page-title"]::text').extract_first(),
                'utility': utility,
                'mechanics': mechanics,
                'force': force,
                'preparation': main_text[0],
                'execution': main_text[1],
                'comments': main_text[2],
                'target_muscles': target_muscles,
                'synergist_muscles': synergist_muscles,
                'video_url': 'https://a21pt313.studev.groept.be/Videos/' + joined_dir + 'video.mp4'
            }
        }
