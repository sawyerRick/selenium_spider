
#子类添加属性问题
from selenium import webdriver
import os, pprint, pymongo, time

class Db():
    def __init__(self, dbname="None", col_name="None"):
        self.client = pymongo.MongoClient()
        self.dbname = dbname
        self.db = self.client[dbname]
        self.col_name = col_name
        self.col = self.db[self.col_name]
        self.data_list = [post for post in self.col.find()]


    def set_dbname(self, name):
        self.dbname = name;
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
    def __init__(self, deriver):
        self.driver = deriver
        self.sex_dict = {"他":"男", "她":"女"}
        self.followers_page_min = 1
        self.followers_page_max = 1
        self.db = Db()
        

    def isCAPTCHA(self, name):
        if name:
            return 0
        else:
            return 1


class DetailCrawler(Crawler):
    def get_details_from(self, user):
        self.driver.get(user.get_homepage())
        self.driver.find_element_by_xpath(r"//*[@id='ProfileHeader']/div/div[2]/div/div[2]/div[3]/button").click()
        name  = self.driver.find_element_by_xpath(r"//*[@id='ProfileHeader']/div/div[2]/div/div[2]/div[1]/h1/span[1]").text
        if self.isCAPTCHA(name) != 0:
            print("[!] stop at page :%s" % user.get_homepage())
            print("[!] 等待输入验证码...")
            os.system("pause")
        sex = self.driver.find_element_by_xpath(r"//*[@id='Profile-activities']/div[1]/h4/span").text[0]
        industry = self.driver.find_element_by_xpath(r"//*[@id='ProfileHeader']/div/div[2]/div/div[2]/div[2]/div/div/div[2]/div").text
        career_exp = self.driver.find_elements_by_class_name("ProfileHeader-field")
        remark = self.driver.find_element_by_xpath(r"//*[@id='ProfileHeader']/div/div[2]/div/div[2]/div[2]/div/div/div[5]/div").text
        data = {
            "name": name,
            "url": user.get_homepage(),
            "sex": self.sex_dict[sex],
            "industry": industry,
            "career_exp": [exp.text for exp in career_exp],
            "remark": remark
        }
        user.set_details(name=name, sex=sex, industry=industry, career_exp=career_exp, remark=remark, data=data)
        self.driver.close()
        self.db.set_dbname("zhihu")
        self.db.set_col("userDetail")
        self.db.insert_ont(data)
        print("%s insert to col userDetail ..." % data)


class HomePageCrawler(Crawler):
    def get_followers_from(self, user):
        db = Db("zhihu", "user_urls")
        self.driver.get(user.get_follower_page())
        #获取最大页数问题为未解决
        #time.sleep(2)
        #self.followers_page_max = self.driver.find_element_by_xpath(r"//*[@id='Profile-following']/div[2]/div[21]/button[5]").text
        print(self.followers_page_max)
        for page in range(100):
            self.driver.get(user.get_follower_page(page))
            url_elements = self.driver.find_elements_by_class_name('UserLink-link')
            if url_elements == []:
                print("[!] stop at page :%s" % user.get_homepage())
                print("[!] 等待输入验证码...")
                os.system("pause")
                self.driver.get(user.get_follower_page())
            for elem in url_elements:
                user_url = elem.get_attribute('href')
                print(db.data_list)
                if (db.isDuplicate(user_url) == 0):
                    self.db.insert_one({"user_url": user_url})
                    print("[+] url: %s ==> 插入user_urls..." % user_url)
                else:
                    print("[!] url: %s ==> 重复url..." % user_url)

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
        print("%s" % self.__followers_page + "?page=" + str(n))
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


# user1 = User("https://www.zhihu.com/people/xiao-jue-83/")
# detail_crawer = DetailCrawler(webdriver.Chrome())
# detail_crawer.get_details_from(user1)
# user1.get_details()

# home_crawler = HomePageCrawler(webdriver.Chrome())
# home_crawler.get_followers_from(user1)

# zhihu_db = Db("zhihu")
# vklist = zhihu_db.get_col("user_urls")
# print(vklist)
user1 = User("https://www.zhihu.com/people/xiao-jue-83/")
homepage_crawler = HomePageCrawler(webdriver.Chrome())
homepage_crawler.get_followers_from(user1)
# detail_crawler = DetailCrawler(webdriver.Chrome())