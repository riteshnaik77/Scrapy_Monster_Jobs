# ````````````````````````````````````````````````````````````````````````````

from distutils.errors import LinkError
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'banglore_jobs'
    allowed_domains = ['monsterindia.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.monsterindia.com/search/jobs-in-bangalore-2', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        })
        
    def parse(self, response):
        
        for job in response.xpath('//*[@id="srp-jobList"]/div/div'):
             
          yield {
                    'title': job.xpath("normalize-space(.//div/div[1]/div/div/h3/a/text())").get(),
                    'company': job.xpath('.//div/div[1]/div/div/span/a/text()').get(),
                    'url': job.xpath('.//div/div/div/div/h3/a/@href').get(),
                    "experience" : job.xpath('normalize-space(.//div/div[1]/div/div/div/div/div/span/small)').get(),
                    "salary": job.xpath('normalize-space(.//div/div[1]/div/div/div/div[3]/span/small/text())').get(),
                    "posted" : job.xpath('normalize-space(.//div[@class="posted-update pl5 fl"]/span[1]/text())').get(),
                    "location1": job.xpath('normalize-space(.//div/div[1]/div/div/div[@class="searctag row"]/div[1]/span[@class="loc"]/small[1]/text())').get(),
                    "location2": job.xpath('normalize-space(.//div/div[1]/div/div/div[@class="searctag row"]/div[1]/span[@class="loc"]/small[2]/text())').get()

                    # 'User-Agent': response.request.headers['User-Agent']
                }
            
        
          next_page = response.xpath('//*[@id="pag-data"]/a[2]/@href').get()
          if next_page:
                    yield scrapy.Request(url=next_page, callback=self.parse, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
                    })
