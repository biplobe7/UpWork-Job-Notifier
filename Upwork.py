# -*- coding: utf-8 -*-
import time
from winsound import Beep
from selenium import webdriver
import re


class UpWork:

    def __init__(self):
        self.job_patter = re.compile(
            """[\w\W]*Fixed-Price[\w\W]*Posted\s([123]\d|\d|a)\smin[\w\W]*Payment\sverified[\w\W]*""")
        self.driver = webdriver.Firefox()
        self.driver.get("https://www.upwork.com/login")

    @staticmethod
    def alert(try_out):
        for item in range(try_out):
            Beep(1300, 600)

    @staticmethod
    def log_title(message_title):
        print """[Log-info] : [{}] : {}""".format(time.ctime(), message_title.center(60, "*"))

    @staticmethod
    def wait_4_continue():
        return raw_input("Process is waiting. Press any key to continue.")

    def collect_job(self):
        job_collection = self.driver.find_elements_by_xpath(
            """//div[@id='feed-jobs']/section[contains(@class,'job-tile')]/div/div/div""")
        result = []
        for job in job_collection:
            result.append(job.text)
        return result

    def job_matched(self, job):
        searched = self.job_patter.search(job)
        return searched is not None

    def reload(self):
        time.sleep(70)
        self.driver.refresh()

    def stop(self):
        self.driver.close()
        # self.driver.quit()


def debug():
    up_work = UpWork()
    up_work.wait_4_continue()
    jobs = up_work.collect_job()
    print "total job found : " + str(len(jobs))
    up_work_log = open("./upwork.log", "w")
    for job in jobs:
        up_work_log.write(job + "\n\n")
    up_work_log.close()
    up_work.stop()
    pass


def main():
    up_work = UpWork()
    up_work.wait_4_continue()
    try:
        while True:
            job_matched = 1
            jobs = up_work.collect_job()
            for job in jobs:
                if up_work.job_matched(job):
                    up_work.log_title("--Job found : Job No: {}--".format(job_matched))
                    print (job + "\n\n")
                    up_work.alert(3)
                    job_matched = job_matched + 1
            if not (job_matched - 1):
                up_work.log_title("--No Match Found--")
            up_work.reload()
    except KeyboardInterrupt:
        up_work.wait_4_continue()
        up_work.stop()
    pass

if __name__ == '__main__':
    main()
    # debug()
    pass
