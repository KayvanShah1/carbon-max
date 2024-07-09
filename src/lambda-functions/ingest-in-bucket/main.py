from datetime import datetime
import json

from bucket import connect_to_buffer_bucket, push_json_to_buffer_bucket


def generate_path(date):
    path = (
        f"sample_data/year={date.year}/month={date.month}/day={date.day}" f"/file_{date.strftime('%Y%m%d%H%M%S')}.json"
    )
    return path


def lambda_handler(event, context):
    """
    Lambda function handler for ingesting data into a bucket.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (object): The runtime information of the Lambda function.

    Returns:
        None
    """

    bucket = connect_to_buffer_bucket("optical-unison-356814-tf-test-bucket")
    path = generate_path(datetime.now())

    messages = event["Records"]
    for record in messages:
        record["body"] = json.loads(record["body"])
        record["body"]["Message"] = json.loads(record["body"]["Message"])

    push_json_to_buffer_bucket(bucket, event["Records"], path)
