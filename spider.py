import pymongo, requests, re, os
from selenium import webdriver
from bs4 import BeautifulSoup


client = pymongo.MongoClient()
db = client['zhihu']
collection = db['user_urls']
# headers = {
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
# }
# wb_data = requests.get(url, headers = headers)
# soup = BeautifulSoup(wb_data.text, 'lxml')
# href = soup.find_all("a", class_="List-item")
# print(href)
url = 'https://www.zhihu.com/people/xiao-jue-83/followers?page='
urls = (url + str(x) for x in range(100, 1000))
driver = webdriver.Chrome()
for i in urls:
    print("[+] trying :%s" % i)
    driver.get(i)
    url_elements = driver.find_elements_by_class_name('UserLink-link')
    elems = set(elem for elem in url_elements) #去重复
    for elem in elems:
        print(elem.get_attribute('href'))
        result = collection.insert_one({"user_url": elem.get_attribute('href')})


os.system('pause')
driver.close()

