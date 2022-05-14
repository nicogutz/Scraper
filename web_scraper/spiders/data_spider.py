import json
import os
import pathlib

import scrapy
import urllib3


class DataScraper(scrapy.Spider):
    name = "data"
    http = urllib3.PoolManager()

    def start_requests(self):
        urls = []
        with open(os.path.dirname(__file__) + '/../links_new.json', 'r') as fr:
            urls = json.load(fr)

        # TODO: Remove when done
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        relative_dir_list = response.url.split("/")[3:]
        joined_dir = ""

        for folder in relative_dir_list:
            joined_dir = joined_dir + folder + '/'

        yield {
            relative_dir_list[-1]: {
                'name': response.css('video source::attr(src)').extract_first(),
                'classification': response.css('video source::attr(src)').extract_first(),
                'preparation': response.css('video source::attr(src)').extract_first(),
                'execution': response.css('video source::attr(src)').extract_first(),
                'comments': response.css('video source::attr(src)').extract_first(),
                'target_muscles': response.css('video source::attr(src)').extract_first(),
                'synergist_muscles': response.css('video source::attr(src)').extract_first(),
                'video_url': joined_dir
            }
        }
