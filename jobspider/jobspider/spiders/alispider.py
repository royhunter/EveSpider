import scrapy
import json

import job
from jobspider.items import JobspiderItem

class AliSpider(scrapy.Spider):
    name = 'ali'
    start_urls = ["https://job.alibaba.com/zhaopin/socialPositionList/doList.json?pageSize=1&t=0.9132508052038073&keyWord=&location=%E5%8C%97%E4%BA%AC&second=&first=%E6%8A%80%E6%9C%AF%E7%B1%BB&pageIndex=1",]

    def job_resp_check(self, jobinfo):
        if jobinfo['isSuccess'] != True:
            print("get job failed")
            return False

        self.totalRecord = jobinfo['returnValue']['totalRecord']
        if self.totalRecord == 0:
            return False

        return True


    def parse(self, response):
        if not self.job_resp_check(json.loads(response.body)):
            yield None

        url = "https://job.alibaba.com/zhaopin/socialPositionList/doList.json?pageSize=" + str(self.totalRecord) + "&t=0.9132508052038073&keyWord=&location=%E5%8C%97%E4%BA%AC&second=&first=%E6%8A%80%E6%9C%AF%E7%B1%BB&pageIndex=1"
        yield scrapy.Request(url, callback=self.parse_job_page)


    def parse_job_page(self, response):
        jobinfo = json.loads(response.body)
        jobs = jobinfo["returnValue"]["datas"]

        for job in jobs:
            item = JobspiderItem()
            item['name'] = job['name']
            item['createtime'] = job['gmtCreate']
            item['updatetime'] = job['gmtModified']
            item['desc'] = job['description']
            item['requirement'] = job['requirement']
            item['departmentName'] = job['departmentName']
            item['category'] = job['secondCategory']
            item['workExperience'] = job['workExperience']
            item['jobid'] = job['id']
            yield item
