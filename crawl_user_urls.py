import pymongo, os, queue, threading
from selenium import webdriver

client = pymongo.MongoClient()
db = client['zhihu']
collection = db['user_urls']
db_url_list = [item["user_url"] for item in collection.find()]
start_url = 'https://www.zhihu.com/people/xiao-jue-83/followers?page='


def make_queue(start_url):
    start_page = int(input(">>start_page:"))
    end_page = int(input(">>end_page:"))
    url_queue = queue.Queue()
    for x in range(start_page, end_page):
        url_queue.put(start_url + str(x))
    return url_queue


def isDuplicate(url):
    if url in db_url_list:
        return 1
    else:
        return 0


def crawl_user_urls(page):
    driver = webdriver.Chrome()
    print('[+] thread %s is running.' % threading.current_thread().name)
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
    driver.close()

if __name__ == "__main__":
    url_queue = make_queue(start_url)
    while not url_queue.empty():
        crawl_thread = threading.Thread(target=crawl_user_urls, args=(url_queue.get(),))
        crawl_thread.start()
    os.system('pause')
