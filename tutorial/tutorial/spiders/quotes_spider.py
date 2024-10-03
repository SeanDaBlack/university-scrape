from pathlib import Path
import urllib.parse
import scrapy
from scrapy.linkextractors import LinkExtractor

# from schools import *

school = "morehouse.edu"

allowed_domains = ["morehouse.edu"]

disallowed_domains = []
start_urls = [
    "https://morehouse.edu/about/leadership",
]


class QuotesSpider(scrapy.Spider):

    name = "quotes"

    allowed_domains = allowed_domains

    disallowed_domains = disallowed_domains
    start_urls = start_urls
    link_ext = LinkExtractor(allow=allowed_domains, deny=disallowed_domains)

    def parse(self, response):

        emails = response.css("a::attr(href)").re(r".*@morehouse.edu")
        decoded_emails = [urllib.parse.unquote(email) for email in emails]

        for email_address in decoded_emails:
            if "mailto:" in email_address or f"morehouse.edu" in email_address:
                yield {
                    "email": email_address,
                    "link": response.url,
                }
        for link in self.link_ext.extract_links(response):
            if "blog" in link.url:
                continue
            elif "calendar" in link.url:
                continue

            elif "news" in link.url:
                continue
            elif "files" in link.url:
                continue
            yield scrapy.Request(link.url, callback=self.parse)
        # # extract links from the page
        # # limit redirect pathing to 20 links deep
