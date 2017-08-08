from urllib.parse import urlparse
from urllib.parse import parse_qs
from .db_connector import TmallBrandsDB
from .utils import BrandsAnalyser
import requests
import time
import os
import errno
from lxml import html
import random
import shutil


class TmallSpider(object):

    def __init__(self, source_file, target_image_path):
        self.source_file = source_file
        self.start_urls = self._get_start_urls()
        self.target_image_path = target_image_path

    def _get_start_urls(self):
        brands_analyser = BrandsAnalyser(self.source_file)
        return brands_analyser.get_start_urls()

    def crawl_a_brand(self, url):
        keyword = ''
        image_urls = ''
        item = {}
        page = requests.get(url)
        tree = html.fromstring(page.content)

        queries = parse_qs(urlparse(url).query)
        keyword = queries.get('q', '')
        if type(keyword) is list:
            keyword = keyword[0]
        print('keyword %s' % keyword)
        image_urls = tree.xpath("//div[@class='m-brand']/a/img/@src")
        if type(image_urls) is list and image_urls:
            image_urls = 'http:%s' % (image_urls[0])
        item['image_urls'] = image_urls
        item['keyword'] = keyword

        # save image
        image_path = os.path.join(self.target_image_path, '%s.jpg' % keyword)
        if not os.path.exists(os.path.dirname(image_path)):
            try:
                os.makedirs(os.path.dirname(image_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        if image_urls:
            r = requests.get(image_urls, stream=True)
            if r.status_code == 200:
                with open(image_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)        

            # save records
            my_db = TmallBrandsDB()
            my_db.process_item(item)

    def crawl(self):
        for url in self.start_urls:
            self.crawl_a_brand(url)
            print(url)
            random_sleep = random.randint(15, 40)
            time.sleep(random_sleep)
