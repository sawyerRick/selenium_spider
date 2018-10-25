import pymongo, pprint

client = pymongo.MongoClient()
db = client['zhihu']
collection = db['user_urls']
url_list = []
count = 0

for post in collection.find():
    pprint.pprint(post)
    url_list.append(post["user_url"])
    count += 1

print(url_list)
print("count: %d" % count)