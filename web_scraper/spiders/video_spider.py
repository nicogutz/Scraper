import json
import os
import pathlib
import shutil

import scrapy
import urllib3


class VideoScraper(scrapy.Spider):
    name = "video"
    http = urllib3.PoolManager()

    def start_requests(self):
        urls = []
        with open(os.path.dirname(__file__) + '/../links_new.json', 'r') as fr:
            urls = json.load(fr)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        relative_dir_list = response.url.split("/")[3:]
        joined_dir = ""

        for folder in relative_dir_list:
            joined_dir = joined_dir + folder + '/'

        path = pathlib.Path(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Images/', joined_dir))
        path_str = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Images/', joined_dir)
        path.mkdir(parents=True, exist_ok=True)

        video_url = response.css('video source::attr(src)').extract_first()
        headers = {}

        with self.http.request('GET', video_url, preload_content=False, headers=headers) as r, \
                open(path_str + 'video.mp4', 'wb') as out_file:
            shutil.copyfileobj(r, out_file)
