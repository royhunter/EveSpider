# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
import smtplib
import time,re

from_addr = "roy.luo@sanscout.com"
password = "!Thankyou1"
smtp_server = 'webmail.emailsrvr.com'
to_addr_list_str = "royluo06@gmail.com"
to_addr_list = ["royluo06@gmail.com"]


class Subscribe():
    job_link_prefix="https://job.alibaba.com/zhaopin/position_detail.htm?spm=0.0.0.0.AryUvR&positionId="

    def __init__(self, col):
        self.col = col


    def mail_content_get(self, post_list):
        body = "<html><body><h1><a href=\"https://job.alibaba.com/zhaopin/index.htm\">This is alibaba job update</a></h1>"
        if len(post_list) == 0:
            body = "<p>no update today</p>"
        else:
            for i in range(len(post_list)):
                jobinfo_url = self.job_link_prefix + str(post_list[i]['jobid'])
                item =  "<p>" + str(i) + "<a href=" + jobinfo_url + ">" + post_list[i]['name'] + "</a><br>description:<br>" + post_list[i]['desc'] + "<br>requirement:<br>" + post_list[i]['requirement'] + "</p>"
                body = body + item
            body = body + "</body></html>"
        return body

    def send_mail(self, post_list):
        print(self.mail_content_get(post_list))
        msg = MIMEText(self.mail_content_get(post_list), 'html', 'utf-8')
        msg['From'] = from_addr
        msg['To'] = to_addr_list_str
        msg['Subject'] = 'royluo\'s job subscribe update'
        server =  smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr_list, msg.as_string())
        server.quit()


    def one_day_update(self):
        sub = list()
        for job in self.col.find():
            if (re.match(u'阿里云', job['name']) or re.match(u'蚂蚁金服', job['name'])) and job['category'] == u'开发':
                timeupdate = job['updatetime']/1000
                #time_now = time.time()
                time_now = 1470494780
                time_scan_start = time_now - 24*60*60
                if time_scan_start < timeupdate:
                    print("this is a new job update" + job['name'])
                    sub.append(job)
        return sub



    def start(self):
        self.send_mail(self.one_day_update())



