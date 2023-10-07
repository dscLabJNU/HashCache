import hashlib
from pymongo import MongoClient
import logging


mongodb_user = "mongodb://mongodb-user.default:27017"
# mongodb_user = "10.43.99.205:27017"
mongo_client = MongoClient(f"{mongodb_user}")
db = mongo_client["user-db"]  # 获取数据库对象


def load_user():
    c = db['user']
    users = c.find()
    profiles = {}
    for user in users:
        profiles[user['username']] = user['password']
    return profiles

def main(args):
    res = {"correct": False}
    username = args['username']
    sha_sum = hashlib.sha256(args['password'].encode('utf-8')).hexdigest()
    password = str(sha_sum)
    users = load_user()

    for true_username, true_passwd in users.items():
        if username==true_username and password == true_passwd:
            res['correct'] = True
            break

    return res


if __name__ == "__main__":
    print(main({
        "username": "Cornell_493",
        "password": "493"*10
    }))