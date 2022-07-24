import base64
import functions_framework


@functions_framework.cloud_event
# Triggered from a message on a Cloud Pub/Sub topic.
def test_function(cloud_event):
    # Print out the data from Pub/Sub, to prove that it worked
    message = cloud_event.data["message"]
    message["data"] = base64.b64decode(message["data"])
    print(message)
