import scrapy

from blog.items import BlogspiderItem



class BlogSpider(scrapy.Spider):
    name = "blogspider"
    start_urls = ["http://royluo.org/",]

    def parse(self, response):
        #print(response.url)
        href = response.xpath("//a[@class='article-title']/@href").extract_first()
        url = response.urljoin(href)
        #print(url)
        yield scrapy.Request(url, callback=self.parse_blog_page)


    def parse_blog_page(self, response):
        item = BlogspiderItem()
        title = response.xpath("//title/text()").extract_first()
        item['link'] = response.url
        item['title'] = title.split("|")[0] 
        item['date'] = response.xpath("//div/a/time/@datetime").extract_first()
        yield item

        next_page = response.xpath("//a[@id='article-nav-older']/@href").extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, self.parse_blog_page)
