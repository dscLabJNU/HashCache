import logging
import requests


GEO_NEARBY_FUNCTION = "http://owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/hotelReservation/geo"
GET_RATE_FUNCTION = "http://owdev-apigateway.openwhisk:8080/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/hotelReservation/rate"


def geo_searby(geo_req):
    response = requests.post(GEO_NEARBY_FUNCTION, json=geo_req)
    print(f"response of geo_searby: {response.text}")
    return response.json()['data']


def get_rates(rate_req):
    response = requests.post(GET_RATE_FUNCTION, json=rate_req)
    print(response.json())
    return response.json()['data']


def main(args):
    logging.info("in Search Nearby")

    lat = args['lat']
    lon = args['lon']

    logging.info(f"nearby lat = {lat}")
    logging.info(f"nearby lon = {lon}")
    nearby_resp = geo_searby({
        "lat": lat, "lon": lon
    })

    for hid in nearby_resp['hotel_ids']:
        logging.info(f"get Nearby hotelId = {hid}")

    rates_resp = get_rates({
        "hotel_ids": nearby_resp['hotel_ids'],
        "indate": args['indate'],
        "outdate": args['outdate']
    })

    res = {"hotel_ids": []}
    for rate_plan in rates_resp['rate_plans']:
        res['hotel_ids'].append(rate_plan['hotelId'])

    return res

if __name__=="__main__":
    args = {'lat': 37.812999999999995, 'lon': -122.249, 'indate': 14, 'outdate': 22}
    print(main(args=args))
    
    