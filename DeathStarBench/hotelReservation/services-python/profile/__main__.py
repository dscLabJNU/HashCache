import logging
import json
from pymongo import MongoClient
import memcache
import traceback


mongodb_profile = "mongodb://mongodb-profile.default:27017"
mongo_client = MongoClient(mongodb_profile) # 连接 MongoDB 服务器
db = mongo_client["profile-db"]  # 获取数据库对象

memcached_profile = "memcached-profile.default:11211"
memcache_client = memcache.Client([memcached_profile], debug=True) # 连接 memcache 服务器


def main(args):
    res = {}
    print("==================== In GetProfiles ====================")
    hotels = []
    hotel_ids = args['hotel_ids']
    for i in hotel_ids:
        # memcache 读取
        item = memcache_client.get(i)
        if not item:
            # mamcached miss
            try:
                c = db["hotels"]
                hotel_prof = c.find_one({"id": i})
                del hotel_prof['_id']
                # print(f"hotel_prof: {hotel_prof}")
            except Exception as e:
                logging.error("Failed get hotels data: ", e)
                traceback.print_exc()
            hotels.append(hotel_prof)

            memc_str = str(hotel_prof)
            memcache_client.set(i, memc_str)
        else: 
            profile_str = str(item)
            print(f"memc hit with {profile_str}")
            hotel_prof = item
            hotels.append(hotel_prof)
    
    res['hotels'] = hotels
    print("====================  In GetProfiles after getting resp ====================")
    return {"data": res}

if __name__ == "__main__":
    request_args = {
        "hotel_ids": ['6'],
        "locale": 'en'
    }
    print(main(request_args))