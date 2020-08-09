import scrapy
from scrapy import Request
import re


def cleanup(input_string):
    if input_string:
        return re.sub(r'[\\r\\n\\t@]', '', input_string).strip()


class Myspider(scrapy.Spider):
    name = "new"

    headers = {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
    }

    def start_requests(self):
        location_list = ['https://www.movoto.com/london-ca/',
                         'https://www.movoto.com/sidney-oh/',
                         'https://www.movoto.com/boston-ma/',
                         'https://www.movoto.com/san-francisco-ca/single-family/bed-5-0/@37.77493,-122.419416/']
        for url in location_list:

            yield Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        property_links = response.css(".card-link::attr(href)").getall()
        for property_link in property_links:
            print(property_link,"++++++++++++++++++++++++++++++++++++")

            # yield Request(url=property_link, callback=self.parse_info)

        try:
            next_page = response.css('a.next::attr(href)').get()
            if next_page:
                print("NEXT PAGE >>>>>>>>>> ",next_page)
                yield Request(url=next_page, callback=self.parse)
        except Exception as e:
            print("#####################",e)

    def parse_info(self, response):

        yield {
            'Property': response.css('.propertyTypeText span::text').get(),
            'Sqft': cleanup(response.css('div~ div+ div b::text').get()),
            'Location': cleanup(response.css('.dpp-header-title .title::text').get()),
            'price': response.css('.price-title::text').get(),
            'County': response.css('.flex-sm-6:nth-child(6) a::text').get(),
            # 'Mortgage Payment': cleanup(response.css('#scrollCal::text').get()),
            'Property type': cleanup(response.css('.flex-sm-6:nth-child(4) span+ span::text').get()),
            'Neighborhood': cleanup(response.css('.flex-sm-6:nth-child(5) a::text').get()),
            'Airbnb Estimate ': cleanup(response.css('#rentalValueLink::text').get()),
            'Status ': cleanup(response.css('.col-sm-6:nth-child(3) .text-bold::text').get()),
            'Year Built ': cleanup(response.css('.col-sm-6:nth-child(6) .text-bold::text').get()),
            'Description': cleanup(response.css('.paragraph::text').get()),
            'Img_Url': response.css('.img-done::attr(src)').getall()
        }






