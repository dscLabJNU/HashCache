import logging
import random
import time
import requests
owdev_apigateway = "10.43.251.53:8080"
# owdev_apigateway = "owdev-apigateway.openwhisk:8080"
SEARCH_NEARBY_FUNCTION = f"http://{owdev_apigateway}/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/hotelReservation/search"
CHECK_AVAILABILITY_FUNCTION = f"http://{owdev_apigateway}/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/hotelReservation/reservation"
PROFILE_FUNCTION = f"http://{owdev_apigateway}/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/hotelReservation/profile"
RECOMMENDATION_FUNCTION = f"http://{owdev_apigateway}/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/hotelReservation/recommendation"
CHECK_USER_FUNCTION = f"http://{owdev_apigateway}/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/hotelReservation/user"
RESERVATION_FUNCTION = f"http://{owdev_apigateway}/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/hotelReservation/reservation"


def search_nearby(nearby_req):
    response = requests.post(SEARCH_NEARBY_FUNCTION,
                             json=nearby_req)
    return response.json()['data']


def check_availability(check_req):
    check_req.update({
        "branch": "check_availability"
    })
    print(f"check_req:{check_req}")
    response = requests.post(CHECK_AVAILABILITY_FUNCTION,
                             json=check_req)
    return response.json()['data']


def get_profiles(profile_req):
    response = requests.post(PROFILE_FUNCTION, json=profile_req)
    return response.json()['data']


def search_handler(args):
    indate = args.get("indate", None)
    outdate = args.get("outdate", None)
    if not indate or not outdate:
        raise Exception("Please specify indate/outdate params")

    slat, slon = args.get("lat", None), args.get("lon", None)
    if not slat or not slon:
        return Exception("Please specify location params")

    lat = float(slat)
    lon = float(slon)
    print("starts searchHandler querying downstream")

    search_resp = search_nearby(
        {
            "lat": lat,
            "lon": lon,
            "indate": indate,
            "outdate": outdate
        }
    )
    print("SearchHandler gets searchResp")

    locale = args.get("locale", "en")
    print(f"search_resp: {search_resp}")
    reservation_resp = check_availability(
        {
            "check_availability": "check_availability",  # additional param
            "customer_name": "",
            "hotel_ids": search_resp['hotel_ids'],
            "indate": indate,
            "outdate": outdate,
            "room_number": 1
        }
    )
    print(
        f"searchHandler gets reserveResp hotel ids = {reservation_resp['hotel_ids']}")

    profile_resp = get_profiles({
        "hotel_ids": reservation_resp['hotel_ids'],
        "locale": locale
    })

    print("searchHandler gets profileResp")

    return profile_resp['data']


def get_recommendations(recom_req):
    response = requests.post(RECOMMENDATION_FUNCTION,
                             json=recom_req)
    return response.json()['data']


def recommendation_handler(args):
    slat, slon = args.get("lat", None), args.get('lon', None)
    if not slat or not slon:
        raise Exception("Please specify location params")

    lat = float(slat)
    lon = float(slon)

    require = args.get('require', None)
    if require != "dist" and require != "rate" and require != "price":
        raise Exception('Please specify require params')

    rec_resp = get_recommendations({
        "require": require,
        "lat": lat,
        "lon": lon
    })

    locale = args.get("locale", "en")

    profile_resp = get_profiles({
        "hotel_ids": rec_resp['hotel_ids'],
        "locale": locale
    })

    return profile_resp['data']


def check_user(check_req):
    response = requests.post(CHECK_USER_FUNCTION, json=check_req)
    return response.json()['data']


def user_handler(args):
    username = args.get("username", None)
    password = args.get("password", None)
    if not username or not password:
        raise Exception("lease specify username and password")

    check_resp = check_user({
        "username": username,
        "password": password
    })

    login_str = "Login successfully!"
    if not check_resp['correct']:
        login_str = "Failed. Please check your username and password. "

    return {"message": login_str}


def check_data_format(date: str) -> bool:
    if len(date) != 10:
        return False
    for i in range(10):
        if i == 4 or i == 7:
            if date[i] != '-':
                return False
        else:
            if not date[i].isdigit():
                return False
    return True


def make_reservation(reserve_req):
    reserve_req.update({
        "branch": "make_reservation"
    })
    print(f"make_reservation: {reserve_req}")
    response = requests.post(RESERVATION_FUNCTION,
                             json=reserve_req)
    return response.json()['data']


def reservation_hander(args):
    indate = args.get("indate", None)
    outdate = args.get("outdate", None)
    if not indate or not outdate:
        raise Exception("Please specify indate/outdate params")

    if not check_data_format(indate) or not check_data_format(outdate):
        raise Exception("Please check indate/outdate format (YYYY-MM-DD)")

    hotel_id = args.get("hotel_id", None)
    if not hotel_id:
        raise Exception("Please specify hotel_id params")

    customer_name = args.get("customer_name", None)
    if not customer_name:
        raise Exception("Please specify customer_name params")

    username = args.get("username", None)
    password = args.get("password", None)
    if not username or not password:
        raise Exception("lease specify username and password")

    room_number = args.get("number", 0)

    check_resp = check_user({
        "username": username,
        "password": password
    })

    reserve_str = "Login successfully! Now ready to reserve."
    if not check_resp['correct']:
        reserve_str = "Failed. Please check your username and password. "

    reservation_resp = make_reservation({
        "customer_name": customer_name,
        "hotel_id": [hotel_id],
        "indate": indate,
        "outdate": outdate,
        "room_number": int(room_number)
    })
    reserve_str = f"Hotel room ({reservation_resp['hotel_id']})reservation success, provide user name ({customer_name}) to check in"
    if len(reservation_resp['hotel_id']) == 0:
        reserve_str = "Failed. Already reserved."
    return {"message": reserve_str}


def main(args):
    request_path = args['request_path']
    res = {}
    if request_path == '/hotels':
        res = search_handler(args)
    elif request_path == "/recommendations":
        res = recommendation_handler(args)
    elif request_path == '/user':  # login
        res = user_handler(args)
    elif request_path == "/reservation":
        res = reservation_hander(args)

    return res


if __name__ == "__main__":
    from owk_invoke import OwkFunction
    owk_function = OwkFunction()
    # args = owk_function.user_login()
    # args = owk_function.recommend()
    # args = owk_function.search_hotel()
    # args = owk_function.reserve()
    # print(main(args))