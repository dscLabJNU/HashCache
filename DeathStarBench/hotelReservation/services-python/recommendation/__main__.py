import logging
from pymongo import MongoClient
from geopy import distance


mongodb_recommendation = "mongodb://mongodb-recommendation.default:27017"
# mongodb_recommendation = "10.43.161.137"
mongo_client = MongoClient(mongodb_recommendation)
db = mongo_client["recommendation-db"]  # 获取数据库对象

def get_hotels():
    c = db['recommendation']
    hotels = c.find()
    profiles = {}
    for hotel in hotels:
        # del hotel["_id"]
        profiles[hotel['hotelId']] = hotel
    return profiles

def main(args):
    res = {"hotel_ids": []}
    logging.info("GetRecommendations")

    require = args['require']
    hotels = get_hotels()

    if require == "dist":
        p1 = {
            "pid": "",
            "plat": args['lat'],
            "plon": args['lon']
        }
        min_dist = float('inf')
        for _, hotel in hotels.items():
            tmp_dist = distance.distance((p1['plat'], p1['plon']), (hotel['lat'], hotel['lon']))
            min_dist = min(min_dist, tmp_dist)
        
        # 有可能有多个相同距离的酒店
        for hotel_id, hotel in hotels.items():
            tmp_dist = distance.distance((p1['plat'], p1['plon']), (hotel['lat'], hotel['lon']))
            if tmp_dist == min_dist:
                res['hotel_ids'].append(hotel_id)
    elif require == "rate":
        max_rate = -float('inf')
        for _, hotel in hotels.items():
            max_rate = max(hotel['rate'], max_rate)

        for hotel_id, hotel in hotels.items():
            if hotel['rate'] == max_rate:
                res['hotel_ids'].append(hotel_id)
            
    elif require == "price":
        min_price = float("inf")

        for _, hotel in hotels.items():
            min_price = min(min_price, hotel['price'])

        for hotel_id, hotel in hotels.items():
            if hotel['price'] == min_price:
                res['hotel_ids'].append(hotel_id)
    else:
        logging.error(f"Wrong require parameter: {require}")

    return res

if __name__=="__main__":
    # print(get_hotels())

    # print(main({"lat": 38.25149999999999, "lon": 121.786, "require": "dist"}))
    # print(main({"lat": 38.25149999999999, "lon": 121.786, "require": "rate"}))
    print(main({"lat": 38.25149999999999, "lon": 121.786, "require": "price"}))
