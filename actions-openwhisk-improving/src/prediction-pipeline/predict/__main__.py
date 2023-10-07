
msg = 'good'
try:
    import time
    import traceback
    import os
    import json
    import pickle
    import boto3
    # import tensorflow as tf
    # import tensorflow.compat.v1 as tf
    # tf.disable_v2_behavior()
    import numpy as np
    import hashlib
except Exception as e:
    msg = traceback.format_exc()


BUCKET = "openwhiskbucket"
FOLDER = "prediction_pipeline/resize"

RESIZE_IMAGE_PB = "resized_image_0.pb"
MOBILENET_PB = 'mobilenet_v2_1.0_224_frozen.pb'


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


def get_hash(s):
    return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16)


def main(args):
    try:
        print(f"predition function -> ARGS: {args}")
        # Use S3 to communicate big messages
        #######################################################################################################################
        s3, bucket_name, bucket_key = get_s3_instance(args.get('data', {}))
        resize_pickle = s3.get_object(Bucket=bucket_name, Key=bucket_key)[
            'Body'].read()
        #######################################################################################################################
        # startTime = 1000*time.time()
        # img = pickle.loads(resize_pickle)
        # mobilenet_pickle = s3.get_object(
        #     Bucket=bucket_name, Key=os.path.join(FOLDER, MOBILENET_PB))['Body'].read()

        # gd = tf.GraphDef.FromString(mobilenet_pickle)

        # inp, predictions = tf.import_graph_def(
        #     gd,  return_elements=['input:0', 'MobilenetV2/Predictions/Reshape_1:0'])

        # with tf.Session(graph=inp.graph):
        #     x = predictions.eval(feed_dict={inp: img})

        seed = get_hash(bucket_key) % (2**32)
        np.random.seed(seed)
        matrix = np.random.rand(1, 5).tolist()

        return {'predictions': matrix}
    except Exception as e:
        return {"cust_error": traceback.format_exc()}


if __name__ == "__main__":
    print(main({"data": {
        'bucket_name': 'openwhiskbucket',
        'bucket_key': 'prediction_pipeline/resize/resized_image_1.pb'
        }}))
