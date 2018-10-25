import pymongo, os
from selenium import webdriver

client = pymongo.MongoClient()
db = client['zhihu']
collection = db['user_urls']
driver = webdriver.Chrome()
url_list = [item["user_url"] for item in collection.find()]
start_url = 'https://www.zhihu.com/people/xiao-jue-83/followers?page='


def isDuplicate(url):
    if url in url_list:
        return 1
    else:
        return 0

def crawl_user_urls(start_url):
    start_page = int(input(">>start_page:"))
    end_page = int(input(">>end_page:"))
    pages = (start_url + str(x) for x in range(start_page, end_page))
    for page in pages:
        print("[+] trying page:%s" % page)
        driver.get(page)
        url_elements = driver.find_elements_by_class_name('UserLink-link')
        for elem in url_elements:
            user_url = elem.get_attribute('href')
            if (isDuplicate(user_url) == 0):
                result = collection.insert_one({"user_url": user_url})
                print("[+] %s ==> 插入mongodb..." % user_url)
            else:
                print("[!] %s ==> 重复url..." % user_url)
if __name__ == "__main__":
    crawl_user_urls(start_url)
    os.system('pause')
    driver.close()

