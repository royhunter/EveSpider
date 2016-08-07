from email.mime.text import MIMEText
import smtplib
import time

from_addr = "roy.luo@sanscout.com"
password = "!Thankyou1"
smtp_server = 'webmail.emailsrvr.com'
to_addr_list_str = "royluo@gmail.com, fangguoju@gmail.com, yzx1211@gmail.com"
to_addr_list = ["royluo06@gmail.com", "fangguoju@gmail.com", "yzx1211@gmail.com"]


class Subscribe():
    def __init__(self, col):
        self.col = col


    def mail_content_get(self, post_list):
        body = "<html><body><h1>This is royluo's blog update</h1>"
        for i in range(len(post_list)):
            item =  "<p>" + str(i) + ".  <a href=\"" + post_list[i]['link'] + "\">" + post_list[i]['title'].strip() + "</a>    post at " + post_list[i]['date'] + "</p>"
            body = body + item
        body = body + "</body></html>"
        return body

    def send_mail(self, post_list):
        print(self.mail_content_get(post_list))
        msg = MIMEText(self.mail_content_get(post_list), 'html', 'utf-8')
        msg['From'] = from_addr
        msg['To'] = to_addr_list_str
        msg['Subject'] = 'royluo\'s blog update'
        server =  smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr_list, msg.as_string())
        server.quit()

    def date_adjust(self, date):
        return date.split('T')[0] + ' ' + date.split('T')[1].split('.')[0]

    def one_day_update(self):
        sub = list()
        for post in self.col.find():
            post['date'] = self.date_adjust(post['date'])
            timestamp = time.mktime(time.strptime(post['date'], "%Y-%m-%d %H:%M:%S"))
            #time_now = time.time()
            time_now = 1468301638.0
            time_scan_start = time_now - 24*60*60
            if time_scan_start < timestamp:
                print("this is a new post" + post['title'])
                sub.append(post)
        return sub

    def all_history_post(self):
        all = list()
        for post in self.col.find():
            post['date'] = self.date_adjust(post['date'])
            all.append(post)
        return all


    def start(self):
        self.send_mail(self.one_day_update())
        self.send_mail(self.all_history_post())



