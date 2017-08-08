from app.spiders import TmallSpider
import os 

if __name__ == '__main__':
    base_dir_path = os.path.dirname(os.path.realpath(__file__))
    source_file = os.path.join(base_dir_path, 'brands.txt')
    target_image_path = os.path.join(base_dir_path, 'downloads')

    spider = TmallSpider(source_file, target_image_path)
    spider.crawl()