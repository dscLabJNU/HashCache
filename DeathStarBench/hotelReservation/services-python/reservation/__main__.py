from pymongo import MongoClient
import memcache
import logging
from datetime import timedelta, datetime
import traceback
import random
mongodb_reservation = "mongodb://mongodb-reservation.default:27017"
# mongodb_reservation = "mongodb://10.43.72.58:27017"
mongo_client = MongoClient(mongodb_reservation)  # 连接 MongoDB 服务器
db = mongo_client["reservation-db"]  # 获取数据库对


memcached_reserve = "memcached-reserve.default:11211"
# memcached_reserve = "10.43.181.160:11211"
memcache_client = memcache.Client([memcached_reserve],
                                  debug=True)  # 连接 memcache 服务器


def check_availability(args):
    res = {
        "hotel_ids": []
    }

    c = db["reservation"]  # 获取名为 "reservation" 的集合对象
    c1 = db["number"]  # 获取名为 "number" 的集合对象
    host_ids = args['hotel_ids']

    for hotelId in host_ids:
        inDate = datetime.strptime(
            str(args['indate']) + "T12:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
        outDate = datetime.strptime(
            str(args['outdate']) + "T12:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")

        indate = inDate.strftime("%Y-%m-%d")

        while inDate < outDate:
            count = 0
            inDate += timedelta(days=1)
            outdate = inDate.strftime("%Y-%m-%d")
            print(f"reservation check date {outdate}")

            memc_key = f"{hotelId}_{inDate.strftime('%Y-%m-%d')}_{outdate}"

            # memcache 读取
            item = memcache_client.get(memc_key)
            if item:
                #  memcached hit
                count = int(item)
                print(f"memcached hit {memc_key} = {count}")
            else:
                # mamcached miss
                reserve = []
                try:
                    reserve = c.find(
                        {'hotelId': hotelId, 'inDate': indate, 'outDate': outdate})
                except Exception as e:
                    logging.error(
                        f"Tried to find hotelId {hotelId} from date {indate} to date {outdate}, but got error {e}")
                    raise Exception(
                        f"Tried to find hotelId {hotelId} from date {indate} to date {outdate}, but got error {e}")
                for r in reserve:
                    print(
                        f"reservation check reservation number = {hotelId}")
                    count += r["number"]
                # Update memcached
                memcache_client.set(memc_key, count)

            # check capacity
            # check memc capacity
            memc_cap_key = f"{hotelId}_cap"
            item = memcache_client.get(memc_cap_key)
            hotel_cap = 0
            if item:
                hotel_cap = int(item)
                print("memcached hit %s = %d", memc_cap_key, hotel_cap)
            else:
                try:
                    num = c1.find_one({"hotelId": hotelId})
                    print(f"num: {num}")
                except Exception:
                    raise Exception(
                        "Tried to find hotelId [%v], but got error", hotelId, traceback.print_exc())

                hotel_cap = int(num['numberOfRoom'])
                # update memcached
                memcache_client.set(memc_cap_key, str(hotel_cap))

            if count + int(args['room_number']) > hotel_cap:
                break

            indate = outdate
            if inDate == outDate:
                res['hotel_ids'].append(hotelId)

    return res


def make_reservation(args):
    res = {
        "hotel_id": []
    }
    c = db["reservation"]  # 获取名为 "reservation" 的集合对象
    c1 = db["number"]  # 获取名为 "number" 的集合对象
    inDate = datetime.strptime(
        str(args['indate']) + "T12:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
    outDate = datetime.strptime(
        str(args['outdate']) + "T12:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
    hotelId = args['hotel_id'][0]

    indate = inDate.strftime("%Y-%m-%d")
    memc_date_num_map = {}
    while inDate < outDate:
        count = 0
        inDate += timedelta(days=1)
        outdate = inDate.strftime("%Y-%m-%d")
        memc_key = f"{hotelId}_{inDate.strftime('%Y-%m-%d')}_{outdate}"

        # memcache 读取
        item = memcache_client.get(memc_key)
        if item:
            #  memcached hit
            count = int(item)
            print(f"memcached hit {memc_key} = {count}")
            memc_date_num_map[memc_key] = count + int(args['room_number'])
        else:
            # mamcached miss
            print("memcached miss, find in mongodb")
            reserve = []
            try:
                reserve = c.find(
                    {'hotelId': hotelId, 'inDate': indate, 'outDate': outdate})
            except Exception as e:
                logging.error(
                    f"Tried to find hotelId {hotelId} from date {indate} to date {outdate}, but got error {e}")
                raise Exception(
                    f"Tried to find hotelId {hotelId} from date {indate} to date {outdate}, but got error {e}")
            for r in reserve:
                count += r["number"]
            memc_date_num_map[memc_key] = count + int(args['room_number'])
            # only update reservation number cache after check succeeds, update in below

        # check capacity
        # check memc capacity
        memc_cap_key = f"{hotelId}_cap"
        item = memcache_client.get(memc_cap_key)
        hotel_cap = 0
        if item:
            # memcached hit
            hotel_cap = int(item)
            print(f"memcached hit {memc_cap_key} = {hotel_cap}")
        else:
            # memcached miss
            print("memcached miss, find in mongodb")
            try:
                num = c1.find_one({"hotelId": hotelId})
            except Exception:
                raise Exception(
                    "Tried to find hotelId [%v], but got error", hotelId, traceback.print_exc())
            hotel_cap = int(num['numberOfRoom'])
            # update memcached
            memcache_client.set(memc_cap_key, str(hotel_cap))

        if count + int(args['room_number']) > hotel_cap:
            return res
        indate = outdate

    # only update reservation number cache after check succeeds
    for key, value in memc_date_num_map.items():
        memcache_client.set(key, str(value))

    inDate = datetime.strptime(
        args['indate'] + "T12:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
    indate = inDate.strftime("%Y-%m-%d")
    while inDate < outDate:
        inDate += timedelta(days=1)
        outdate = inDate.strftime("%Y-%m-%d")
        c.insert_one({
            "hotel_id": hotelId,
            "customer_name": args['customer_name'],
            "indate": indate,
            "outdate": outdate,
            "number": int(args['room_number'])
        })
        indate = outdate
    res['hotel_id'].append(hotelId)
    return res


def main(args):
    branch = args['branch']
    res = {}
    if branch == "check_availability":
        res = check_availability(args)
    elif branch == "make_reservation":
        res = make_reservation(args)

    return res


if __name__ == "__main__":
    args = {'request_path': '/reservation',
            'branch': '/reservation',
            'indate': '2015-04-12',
            'outdate': '2015-04-17',
            'hotel_id': ['67'],
            'customer_name': 'Cornell_61',
            'room_number': '1'}
    reserve_args = {'customer_name': 'Cornell_253',
                    'hotel_id': ['78'],
                    'indate': '2015-04-17',
                    'outdate': '2015-04-18',
                    'room_number': 1,
                    'branch': 'make_reservation'}
    print(main(args))
