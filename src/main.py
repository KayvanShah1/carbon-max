import base64
import functions_framework
from datetime import datetime

import boto3

from bucket import push_json_to_buffer_bucket, connect_to_buffer_bucket
import secrets


def generate_path(date):
    path = (
        f"sample_data/year={date.year}/month={date.month}/day={date.day}"
        f"/file_{date.strftime('%Y%m%d%H%M%S')}.json"
    )
    return path


def get_message_from_subscription(cloud_event):
    # Pull the message from the subscription
    # Decode the binary message to make to JSON compatible
    message = cloud_event.data["message"]
    message["data"] = base64.b64decode(message["data"]).decode("utf-8")
    return message


@functions_framework.cloud_event
# Triggered from a message on a Cloud Pub/Sub topic.
def test_function(cloud_event):
    # Connect to the buffer bucket
    # Create a path where the message is to be pushed
    bucket = connect_to_buffer_bucket("optical-unison-356814-test-bucket")
    path = generate_path(datetime.now())

    message = get_message_from_subscription(cloud_event)

    # Save the JSON message in GCS Bukcet
    push_json_to_buffer_bucket(bucket, message, path)


@functions_framework.cloud_event
def pubsub_to_sns(cloud_event):
    message = get_message_from_subscription(cloud_event)

    # Authenticate AWS Service User Client
    sns = boto3.client(
        "sns",
        aws_access_key_id=secrets.aws_access_key_id,
        aws_secret_access_key=secrets.aws_secret_access_key,
    )
    region = "us-east-2"
    account = secrets.aws_account_number
    topic_name = "user-updates-topic"
    attrs = {"origin": {"DataType": "String", "StringValue": "pubsub"}}
    topic = f"arn:aws:sns:{region}:{account}:{topic_name}"
    sns.publish(TopicArn=topic, Message=message, MessageAttributes=attrs)
