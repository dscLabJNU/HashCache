msg = "good"
import traceback
try:
    import boto3
    import urllib.request
    from time import time
    import os
    from PIL import Image, ImageFilter
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception as e:
    msg = traceback.format_exc()
# s3_client = boto3.client('s3')
FILE_NAME_INDEX = 2

TMP = "/tmp/"

BUCKET = "openwhiskbucket"
FOLDER = "image_scale/"



def get_s3_instance(args):
    service_name = args.get("service_name", 's3')
    aws_access_key_id = args.get("aws_access_key_id", "your aws_access_key_id")
    aws_secret_access_key = args.get("aws_secret_access_key", "your aws_secret_access_key")
    region_name = args.get("region_name", "ap-southeast-1")
    bucket_name = args.get("bucket_name", BUCKET)
    origin_img = args.get("origin_img", "1")
    bucket_key = args.get("bucket_key", os.path.join(FOLDER, f"{str(origin_img)}.jpeg"))
    # close ssl certification for convinence
    s3 = boto3.client(service_name=service_name,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=region_name,
                      use_ssl=False)
    return s3, bucket_name, bucket_key

cold = True

def main(args):
    global cold
    was_cold = cold
    cold = False
    try:
        s3, bucket_name, bucket_key = get_s3_instance(args=args)
        start_time = time()
        origin_img = s3.get_object(Bucket=bucket_name, Key=bucket_key)['Body']
        fetching_time = time() - start_time
        # This line needs to be commented out when doing IO Scaling tests

        return {"body": { "fetching_time": fetching_time}}
    except Exception as e:
        return {"body": { "cust_error":traceback.format_exc(), "msg":msg, "cold":was_cold }}