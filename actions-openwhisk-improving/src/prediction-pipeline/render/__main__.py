
import json
import numpy as np
import time

def main(args):
    startTime = 1000*time.time()
    print(f"render function -> ARGS: {args}")
    body = args.get("data", {"predictions": [1,2,3,4]})
    x = np.array(body['predictions'])

    text = "Top 1 Prediction: " + str(x.argmax()) + str(x.max())
    print(text)

    response = {
        "statusCode": 200,
        "body": json.dumps({'render': text})
    }

    endTime = 1000*time.time()
    return response

if __name__=="__main__":
    print(main({}))
