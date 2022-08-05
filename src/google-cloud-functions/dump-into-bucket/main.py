import base64
import functions_framework
from datetime import datetime


from bucket import push_json_to_buffer_bucket, connect_to_buffer_bucket


def get_secret(client, project_id, secret_id):
    secret_detail = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": secret_detail})
    payload = response.payload.data.decode("UTF-8")
    return payload


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
    print("Successfully received message from Pub/Sub subscription")
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
