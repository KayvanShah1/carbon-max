import base64
import functions_framework
from datetime import datetime

from bucket import push_json_to_buffer_bucket, connect_to_buffer_bucket


def generate_path(date):
    path = (
        f"sample_data/year={date.year}/month={date.month}/day={date.day}"
        f"/file_{date.strftime('%Y%m%d%H%M%S')}.json"
    )
    return path


@functions_framework.cloud_event
# Triggered from a message on a Cloud Pub/Sub topic.
def test_function(cloud_event):
    # Connect to the buffer bucket
    # Create a path where the message is to be pushed
    bucket = connect_to_buffer_bucket("optical-unison-356814-test-bucket")
    path = generate_path(datetime.now())

    # Pull the message from the subscription
    # Decode the binary message to make to JSON compatible
    message = cloud_event.data["message"]
    message["data"] = base64.b64decode(message["data"]).decode("utf-8")

    # Save the JSON message in GCS Bukcet
    push_json_to_buffer_bucket(bucket, message, path)
