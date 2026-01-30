import scrapy
from scrapy.http import FormRequest

class HkexnewsSpiderSpider(scrapy.Spider):
    name = 'hkexnews_spider'
    allowed_domains = ['hkexnews.hk']
    start_urls = ['https://www.hkexnews.hk/sdw/search/searchsdw.aspx']

    def parse(self, response):

        data = {
            '__EVENTTARGET': 'btnSearch',
            '__VIEWSTATE': response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first(),
            '__VIEWSTATEGENERATOR': response.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first(),
            'today': '20260129',
            'sortBy': 'shareholding',
            'sortDirection': 'desc',
            'txtShareholdingDate': '2026/01/28',
            'txtStockCode': '00001'
        }
        self.logger.info("DATA: %s", data) 
        return [FormRequest("https://www.hkexnews.hk/sdw/search/searchsdw.aspx",
                               formdata=data,
                               callback=self.parse_result)]


    def parse_result(self, response):
        table_rows = response.xpath('//*[@id="pnlResultNormal"]//table/tbody/tr')
        for row in table_rows:
            yield {
                'participant_id': row.xpath('.//td[1]/div[2]//text()').extract_first(),
                'participant_name': row.xpath('.//td[2]/div[2]//text()').extract_first(),
                'address': row.xpath('.//td[3]/div[2]//text()').extract_first(),
                'share_holding': row.xpath('.//td[4]/div[2]//text()').extract_first(),
                'percent_issued_shares': row.xpath('.//td[5]/div[2]//text()').extract_first()
            }

