import pymongo, pprint

client = pymongo.MongoClient()
db = client['zhihu']
collection = db['user_urls']
url_list = []
count = 0

def DeDuplicate():
    print("正在清洗user_urls数据...")
    global count, collection
    
    for item in collection.find():
        url_list.append(item["user_url"])

    url_set = set(url_list)
    collection.drop()
    collection = db['user_urls']


    for url in url_set:
        #pprint.pprint(url)
        collection.insert_one({"user_url": url})
        count += 1

if __name__ == "__main__":
    DeDuplicate()
    print("清洗后一共有%d条记录..." % count)