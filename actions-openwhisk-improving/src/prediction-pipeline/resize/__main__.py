
import pickle
import os
import json
import time
import traceback
msg = 'good'
try:
    import boto3
    import numpy as np
    from PIL import Image
except Exception as e:
    msg = traceback.format_exc()


BUCKET = "openwhiskbucket"
FOLDER = "prediction_pipeline/resize"

RESIZE_IMAGE_PB = "resized_image_{}.pb"  # the placeholder ranging from [0, 95]



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


def main(args):
    startTime = 1000*time.time()
    s3, bucket_name, bucket_key = get_s3_instance(args=args)
    origin_img = s3.get_object(Bucket=bucket_name, Key=bucket_key)[
        'Body']
    image = Image.open(origin_img)

    img = np.array(image.resize((224, 224))).astype(float) / 128 - 1
    resize_img = img.reshape(1, 224, 224, 3)

    serialized_resize = pickle.dumps(resize_img)
    endTime = 1000*time.time()
    #######################################################################################################################
    upload_bucket_key = os.path.join(
        FOLDER, RESIZE_IMAGE_PB.format(str(args.get("origin_img", 0))))
    # Assume it is uploaded to the cloud (saving the quotas)
    # s3.put_object(Bucket=bucket_name, Key=upload_bucket_key, Body=serialized_resize)
    #######################################################################################################################
    response = {"bucket_name": bucket_name,
                "bucket_key": upload_bucket_key}
    return response


if __name__ == "__main__":
    print(main({"origin_img": 4}))
