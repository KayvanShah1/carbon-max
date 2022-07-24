import base64
from lib2to3.pgen2.pgen import generate_grammar
import functions_framework
from datetime import datetime

from bucket import push_json_to_buffer_bucket, connect_to_buffer_bucket


def generate_path(date):
    path = f"sample_data/{date.year}/{date.month}/json_{date.day}.json"
    return path


@functions_framework.cloud_event
# Triggered from a message on a Cloud Pub/Sub topic.
def test_function(cloud_event):
    bucket = connect_to_buffer_bucket("optical-unison-356814-test-bucket")
    path = generate_path(datetime.now())

    # Print out the data from Pub/Sub, to prove that it worked
    message = cloud_event.data["message"]
    message["data"] = base64.b64decode(message["data"]).decode("utf-8")
    push_json_to_buffer_bucket(bucket, message, path)
