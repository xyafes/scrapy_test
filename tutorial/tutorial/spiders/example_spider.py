from pathlib import Path

import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Parse the called response."""
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        file_object = Path(filename)
        file_object.write_bytes(response.body)
        self.log(f'Response url {response.url}')
        self.log(f'[+] Saved file {filename}')
        self.log(f'[+] Request {response.request}')
        self.log(f'[+] Certificate {response.certificate}')
        self.log(f'[+] Ip address {response.ip_address}')
        self.log(f'[+] Protocol {response.protocol}')
        self.log(f'[+] File stats {file_object.stat()}')

