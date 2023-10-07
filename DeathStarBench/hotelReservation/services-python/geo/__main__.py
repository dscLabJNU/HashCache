import logging
from pymongo import MongoClient
from geopy.distance import geodesic


mongodb_geo = "mongodb://mongodb-geo.default:27017"
# mongodb_geo = "10.43.230.124:27017"
mongo_client = MongoClient(f"{mongodb_geo}")
db = mongo_client["geo-db"]  # 获取数据库对象
MAX_SEARCH_RESULTS = 5
MAX_SEARCH_RADIUS = 5000000  # Km


def get_geo_index():
    c = db['geo']
    points = c.find()
    geo_index = list(points)
    return geo_index


def k_nearest(center_dict, max_search_results=MAX_SEARCH_RESULTS, max_search_radius=MAX_SEARCH_RADIUS):
    center = (center_dict['lat'], center_dict['lon'])
    geo_index = get_geo_index()
    # example index: 'hotelId': '47', 'lat': 38.0655, 'lon': -122.03399999999999

    # targets = [(index['lat'], index['lon']) for index in geo_index]
    targets = [{"id": index['hotelId'], "lat": index['lat'],
                "lon": index['lon']} for index in geo_index]

    # Filter out targets that are too far away.
    filtered_targets = [target for target in targets if geodesic(
        center, (target['lat'], target['lon'])).km <= max_search_radius]

    # Find the K nearest targets using a sorted list.
    nearest_targets = sorted(filtered_targets, key=lambda x: geodesic(center, (x['lat'], x['lon'])).m)[
        :max_search_results]

    # print("Nearest targets:")
    # for target in nearest_targets:
    #     print(
    #         f" - id: {target['id']}, {target['lat']}, {target['lon']} (distance = {geodesic(center, (target['lat'], target['lon'])).km} kilometers)")
    return nearest_targets


def get_nearby_points(lat, lon):
    print(f"In geo getNearbyPoints, lat = {lat}, lon = {lon}")
    return k_nearest(center_dict={"lat": lat, "lon": lon})


def main(args):
    print("In geo Nearby")
    lat = args['lat']
    lon = args['lon']
    points = get_nearby_points(float(lat), float(lon))

    print(f"geo after getNearbyPoints, len = {len(points)}")
    res = {
        "hotel_ids": []
    }
    for p in points:
        logging.info(f"In geo Nearby return hotelId = {p['id']}")
        res['hotel_ids'].append(p['id'])

    return res


if __name__ == "__main__":
    center = {
        "lat": 30.67,
        "lon": 104.06
    }
    print(main({'lat': 37.802, 'lon': -122.246}))
