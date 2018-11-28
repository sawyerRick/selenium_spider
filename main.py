#写到DetailCrawler准备提取用户关键信息
from selenium import webdriver
import threading
import os, pprint, pymongo, time
import random, logging
from clean_db import DeDuplicate



class Db():
    def __init__(self, dbname="None", col_name="None"):
        # 初始化
        self.client = pymongo.MongoClient()
        self.dbname = dbname
        self.db = self.client[dbname]
        self.col_name = col_name
        self.col = self.db[self.col_name]
        self.data_list = [post for post in self.col.find()]


    def set_dbname(self, name):
        self.dbname = name
        self.db = self.client[self.dbname]
        self.data_list = [post for post in self.col.find()]


    def set_colname(self, name):
        self.col = self.db[name]
        self.data_list = [post for post in self.col.find()]



    def insert_one(self, data_dict):
        self.col.insert_one(data_dict)


    def get_datalist_from(self, col):
        self.col = col
        return [post for post in self.col.find()]


    def get_dbname(self):
        return self.dbname


    def get_colname(self):
        return self.col_name


    def isDuplicate(self, url):
        if url in self.data_list:
            return 1
        else:
            return 0


class Crawler():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.sex_dict = {"他":"男", "她":"女"}
        self.followers_page_min = 1
        self.followers_page_max = 1
        

    def isCAPTCHA(self, name):
        if name:
            return 0
        else:
            return 1


class DetailCrawler(Crawler):
    #获取页面Detail类爬虫
    def get_details_from(self, homepage=None):
        pass


class HomePageCrawler(Crawler):
    # 获取主页URL类爬虫

    def get_followers_from(self, user, page_minimum=0, page_maximum=100):
        # 生成0-100随机爬取页面
        complete = int(page_maximum - page_minimum)
        page_counter = 0
        visted_list = []
        while len(visted_list) != complete:
            randnum = random.randint(page_minimum, page_maximum)
            if randnum not in visted_list:
                visted_list.append(randnum)

        db = Db("zhihu", "user_urls")
        self.driver.get(user.get_follower_page())

        for page in visted_list:
            self.driver.get(user.get_follower_page(page))
            url_elements = self.driver.find_elements_by_class_name('UserLink-link')
            page_counter += 1
            percent = (int(page_counter) / complete) * 100
            if url_elements == []:
                print("%s爬取已完成%.2f%%..." % (threading.current_thread().getName(), percent))
                print("[!] stop at page :%s" % user.get_homepage())
                print("[!] 等待输入验证码/检查页面情况...")
                os.system("pause")
                self.driver.get(user.get_follower_page(page))
            for elem in url_elements[0:len(url_elements):2]: # 避免重复步为2
                user_url = elem.get_attribute('href')
                db.insert_one({"user_url": user_url})
            print("%s爬取已完成%.2f%%..." % (threading.current_thread().getName(), percent))

        self.driver.close()


class User():
    def __init__(self, homepage="None"):
        self.__homepage = str(homepage)
        self.__name = "None"
        self.__sex = "None"
        self.__industry = "None"
        self.__career_exp = "None"
        self.__remark = "None"
        self.__followers_page = homepage + "followers"
        self.__data = {}
        

    def get_name(self):
        print("%s" % self.__name)
        return self.__name


    def get_homepage(self):
        print("%s" % self.__homepage)
        return self.__homepage


    def get_follower_page(self, n=1):
        #print("%s" % self.__followers_page + "?page=" + str(n))
        return self.__followers_page + "?page=" + str(n)


    def set_details(self, name="None", sex="None", industry="None", career_exp="None", remark="None", data={}):
        self.__name = name
        self.__sex = sex
        self.__industry = industry
        self.__career_exp = career_exp
        self.__remark = remark
        self.__data = data

    def get_details(self):
        print(self.__data)
        return self.__data

# homepage_crawler.get_followers_from(user1, 2500, 5000)

def getting_home_page(url="https://www.zhihu.com/people/GreenFinch/", pages=10, threads=4):
    minimum_page = 0
    maximum_page = 0
    for i in range(threads):
        user1 = User(url)
        homepage_crawler = HomePageCrawler()
        maximum_page += pages / threads
        t = threading.Thread(target=homepage_crawler.get_followers_from, args=(user1, int(minimum_page), int(maximum_page)))
        t.start()
        minimum_page = maximum_page


    main_thread = threading.main_thread()
    for t in threading.enumerate():
        # 跳过主线程(不然程序会终止，看不到后续了)
        if t is main_thread:
            continue
        print('joining %s', t.getName())
        t.join()
    # print("homepage爬取完成...")
    # DeDuplicate()

if __name__ == "__main__":

    getting_home_page()