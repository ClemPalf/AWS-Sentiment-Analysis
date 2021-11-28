# FIRST FUNCTION serialize_image_data
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event["s3_key"]
    bucket = event["s3_bucket"]

    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket, key, "/tmp/image.png")
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

# SECOND FUNCTION perform_inference
# I do think importing the sagemaker module is very bad practice, therefore I chose to use the recommanded way (using the runtime instance)
import json
import base64
import boto3

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2021-11-27-21-38-15-051"

def lambda_handler(event, context):
    
    # The SageMaker runtime is what allows us to invoke the endpoint that we've created.
    runtime = boto3.Session().client('sagemaker-runtime')

    # Decode the image data
    image = base64.b64decode(event["image_data"])

    response = runtime.invoke_endpoint(EndpointName = ENDPOINT,      # The name of the endpoint we created
                                         ContentType = 'image/png',    # The data format that is expected
                                         Body = image)                 # The decoded image
                                         
    inferences = json.loads(response['Body'].read().decode())

    # We return the data back to the Step Function    
    event["inferences"] = inferences
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

# THIRD FUNCTION filter_low_confidence
import json

THRESHOLD = .93

def lambda_handler(event, context):

    # Grab the inferences from the event
    inferences = event["inferences"]

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = (inferences[0] > THRESHOLD) or (inferences[1] > THRESHOLD)

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }