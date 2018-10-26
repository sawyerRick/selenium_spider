import pymongo, pprint

client = pymongo.MongoClient()
db = client['zhihu']
collection = db['user_urls']
url_list = []
count = 0

def drop_and_create():
    global count, collection
    
    for item in collection.find():
        url_list.append(item["user_url"])

    url_set = set(url_list)
    collection.drop()
    collection = db['user_urls']

    for url in url_set:
        collection.insert_one({"user_url": url})
        count += 1

if __name__ == "__main__":
    drop_and_create()
    print("清洗后count: %d..." % count)