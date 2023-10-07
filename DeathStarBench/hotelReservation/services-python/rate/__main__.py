import json

from pymongo import MongoClient
import logging
import memcache

mongodb_rate = "mongodb://mongodb-rate.default:27017"
mongo_client = MongoClient(f"{mongodb_rate}")
db = mongo_client["rate-db"]  # 获取数据库对象

memcached_rate = "memcached-rate.default:11211"
memcache_client = memcache.Client(
    [memcached_rate], debug=True)  # 连接 memcache 服务器


def main(args):
    rate_plans = []
    res = {}
    for hotel_id in args['hotel_ids']:
        # First, check memcached.
        memcache_client.delete(hotel_id)
        rate_str = memcache_client.get(hotel_id)
        if rate_str is not None:
            # Memcached hit.
            rate_strs = rate_str.split('\n')
            print(f"Memcached hit, hotelId = {hotel_id}, rate strings: {rate_strs}")

            for rate_str in rate_strs:
                if len(rate_str) != 0:
                    rate_plans.append(json.loads(rate_str))
        else:
            print(f"Memcached miss, hotelId = {hotel_id}")
            print("Memcached miss, set up mongo connection")

            # Memcached miss, set up mongo connection.
            c = db['inventory']

            memc_str = ""

            tmp_rate_plans = []
            for r in c.find({'hotelId': hotel_id}):
                print(f"rate: {r}")
                rate_plans.append(r)
                del r['_id']
                rate_json = json.dumps(r)
                memc_str = memc_str + rate_json + "\n"
            if memc_str:
                # Write to memcached.
                print(f"hotel_id: {hotel_id}")
                memcache_client.set(hotel_id, memc_str)

    # rate_plans.sort()
    res['rate_plans'] = rate_plans
    return res

if __name__ == "__main__":
    resp = main({
        "hotel_ids": ["1", "2", "4"],
        "hotel_ids": ["81"]
    })

    print(resp)
    