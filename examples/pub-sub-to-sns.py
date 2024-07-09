import base64
import json
import boto3

from google.cloud import secretmanager


def get_secret(client, project_id, secret_id):
    """
    Retrieves the latest version of a secret from Secret Manager.

    Args:
        client (SecretManagerServiceClient): The Secret Manager client.
        project_id (str): The ID of the project containing the secret.
        secret_id (str): The ID of the secret.

    Returns:
        str: The payload of the latest version of the secret.

    Raises:
        google.api_core.exceptions.NotFound: If the secret or its latest version is not found.
        google.api_core.exceptions.PermissionDenied: If the user does not have permission to access the secret.
        google.api_core.exceptions.InvalidArgument: If the project ID or secret ID is invalid.
        google.api_core.exceptions.GoogleAPICallError: If the request to access the secret fails.
    """
    secret_detail = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": secret_detail})
    payload = response.payload.data.decode("UTF-8")
    return payload


def get_message_from_subscription(cloud_event):
    """
    Retrieves and decodes a message from a Pub/Sub subscription.

    Args:
        cloud_event (dict): The cloud event containing the message.

    Returns:
        dict: The decoded message.

    """
    # Pull the message from the subscription
    # Decode the binary message to make it JSON compatible
    message = cloud_event.data["message"]
    message["data"] = base64.b64decode(message["data"]).decode("utf-8")
    print("Successfully received message from Pub/Sub subscription")
    return message


if __name__ == "__main__":
    message = {
        "glossary": {
            "title": "example glossary",
            "GlossDiv": {
                "title": "S",
                "GlossList": {
                    "GlossEntry": {
                        "ID": "SGML",
                        "SortAs": "SGML",
                        "GlossTerm": "Standard Generalized Markup Language",
                        "Acronym": "SGML",
                        "Abbrev": "ISO 8879:1986",
                        "GlossDef": {
                            "para": "A meta-markup language, used to create markup languages such as DocBook.",
                            "GlossSeeAlso": ["GML", "XML"],
                        },
                        "GlossSee": "markup",
                    }
                },
            },
        }
    }

    print("Connecting to GCP Secret Manager Service Client ...")
    client = secretmanager.SecretManagerServiceClient()
    print("Successfully connected to GCP Secret Manager Service Client")
    gcp_project_id = "optical-unison-356814"

    print("Fetching AWS Client Secrets")
    aws_access_key_id = get_secret(client, gcp_project_id, "aws_access_key_id")
    aws_secret_access_key = get_secret(client, gcp_project_id, "aws_secret_access_key")
    aws_account_number = get_secret(client, gcp_project_id, "aws_account_number")
    aws_account_region = get_secret(client, gcp_project_id, "aws_account_region")

    print("Creating AWS Client ...")
    # Authenticate AWS Service User Client
    sns = boto3.client(
        "sns",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_account_region,
    )

    print("Publishing message to AWS SNS topic")
    # Publish the message to AWS SNS topic
    topic_name = "user-updates-topic"
    attrs = {"origin": {"DataType": "String", "StringValue": "pubsub"}}
    topic = f"arn:aws:sns:{aws_account_region}:{aws_account_number}:{topic_name}"
    sns.publish(
        TopicArn=topic,
        Message=json.dumps({"default": json.dumps(message)}),
        MessageAttributes=attrs,
        MessageStructure="json",
    )
    print("Successfully published message to AWS SNS topic")
