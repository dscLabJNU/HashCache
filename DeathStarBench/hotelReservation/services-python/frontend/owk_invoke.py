import random


class OwkFunction:
    def get_user(self):
        id = random.randint(0, 500)
        user_name = f"Cornell_{id}"
        pass_word = ""

        for i in range(10):
            pass_word += str(id)
        return user_name, pass_word

    def user_login(self):
        user_name, password = self.get_user()
        print({"username": user_name,
               "password": password})

        return {
            "request_path": "/user",
            "username": user_name,
            "password": password
        }

    def recommend(self):
        coin = random.random()
        req_param = ""
        if coin < 0.33:
            req_param = "dist"
        elif coin < 0.66:
            req_param = "rate"
        else:
            req_param = "price"

        lat = 38.0235 + (random.randint(0, 30) - 240.5)/1000.0
        lon = -122.095 + (random.randint(0, 30) - 157.0)/1000.0
        args = {
            "request_path": "/recommendations",
            "require": req_param,
            "lat": str(lat),
            "lon": str(lon)
        }
        return args

    def search_hotel(self):
        in_date = random.randint(9, 23)
        out_date = random.randint(in_date + 1, 24)

        in_date_str = str(in_date)
        if in_date <= 9:
            in_date_str = f"2015-04-0{in_date_str }"
        else:
            in_date_str = f"2015-04-{in_date_str}"

        out_date_str = str(out_date)
        if out_date <= 9:
            out_date_str = f"2015-04-0{out_date_str}"
        else:
            out_date_str = f"2015-04-{out_date_str}"

        # 定义请求头
        headers = {'Content-Type': 'application/json'}

        lat = 38.0235 + (random.randint(0, 30) - 240.5)/1000.0
        lon = -122.095 + (random.randint(0, 30) - 157.0)/1000.0

        args = {
            "request_path": "/hotels",
            "indate": in_date_str,
            "outdate": out_date_str,
            "lat": lat,
            "lon": lon
        }
        return args

    def reserve(self):
        in_date = random.randint(9, 23)
        out_date = in_date + random.randint(1, 5)

        in_date_str = str(in_date)

        in_date_str = str(in_date)
        if in_date <= 9:
            in_date_str = "2015-04-0" + in_date_str
        else:
            in_date_str = "2015-04-" + in_date_str

        out_date_str = str(out_date)
        if out_date <= 9:
            out_date_str = "2015-04-0" + out_date_str
        else:
            out_date_str = "2015-04-" + out_date_str

        hotel_id = str(random.randint(1, 80))
        user_id, password = self.get_user()
        customer_name = user_id

        room_number = "1"

        args = {
            "request_path": "/reservation",
            "branch": "/reservation",
            
            "indate": in_date_str,
            "outdate": out_date_str,
            "hotel_id": [hotel_id],
            "customer_name": customer_name,
            "username": user_id,
            "password": password,
            "room_number": room_number
        }
        return args