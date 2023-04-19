from typing import Any

import scrapy


class ExampleSpider(scrapy.Spider):
    name = "api"

    def start_requests(self):
        urls = [
            'https://randomuser.me/api/?results=5',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_body, errback=self.on_error)

    def on_error(self, response):
        self.logger.info(f"[!] Requests is not successful, url -> {response}")

    def parse_results(self, results: list[dict[str, Any]]):
        for item in results:
            self.logger.info(f'[+] User id {item.get("id")}')
            self.logger.info(f'[+] User name {item["name"].get("first", "")} {item["name"].get("last", "")}')
            self.logger.info(f'[+] User email {item.get("email")}')
            self.logger.info(f'[+] User phone {item.get("phone")}')
            self.logger.info(f'[+] User gender {item.get("gender")}')
            self.logger.info(f'[+] User country {item["location"].get("country")}')
            self.logger.info(f'[+] User age {item["dob"].get("age")}')
            self.logger.info(f'[+] User cell {item.get("cell")}')
            self.logger.info(f'[+] User nat {item.get("nat")}')
            self.logger.info(f'[+] User registered {item["registered"].get("date")}\n')

    def parse_json(self, json_response: dict[str, Any]) -> None:
        """Parse and get results from json response."""
        if info := json_response.get("info"):
            self.logger.info(f'[+] Page {info.get("page")}')
        else:
            self.logger.info(f'[!] Info not exists {json_response}')

        if results := json_response.get("results"):
            self.logger.info(f'[+] Founded results size {len(results)}\n')
            self.parse_results(results)
        else:
            self.logger.info(f'[!] Results not exists {json_response}')

    def parse_body(self, response) -> None:
        """Parse the called response."""
        try:
            if json_response := response.json():
                self.logger.info(f'[+] Response body is exists, response type {type(json_response)}')
                self.parse_json(json_response)
            else:
                self.logger.info(f'[!] Response body is not exists, response type {type(json_response)}')
        except Exception as base_exception:
            self.logger.info(f'[!] {base_exception}')
