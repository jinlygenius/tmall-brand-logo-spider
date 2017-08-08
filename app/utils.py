
class BrandsAnalyser(object):
    """
    Analyse source file to get brand keywords for crawling
    """
    def __init__(self, filename=''):
        super(BrandsAnalyser, self).__init__()
        self.filename = filename
        self.brands = self._get_brands()
        self.base_url = 'https://list.tmall.com/search_product.htm?q=%s'

    def _get_brands(self):
        result = list()
        with open(self.filename, 'r') as f:
            for line in f:
                keyword = line.replace('\n', '')
                result.append(keyword)
        return result

    def get_start_urls(self):
        if self.brands:
            return [self.base_url % (brand, ) for brand in self.brands]
        return []
