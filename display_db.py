import pymongo, pprint, time
from clean_db import DeDuplicate

client = pymongo.MongoClient()
db = client['zhihu']
collection = db['user_urls']
url_list = []

def collect():
    for post in collection.find():
        # pprint.pprint(post)
        url_list.append(post["user_url"])

    return len(url_list)


if __name__ == "__main__":
    lastCounter = 0
    while True:
        #DeDuplicate()
        counter = collect()
        pprint.pprint(url_list)
        print("一共有%d条记录...增量:%d..." % (counter, counter - lastCounter))
        url_list = []
        lastCounter = counter
        time.sleep(3)