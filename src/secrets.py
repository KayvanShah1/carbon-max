from google.cloud import secretmanager


def get_secret(client, project_id, secret_id):
    secret_detail = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": secret_detail})
    payload = response.payload.data.decode("UTF-8")
    return payload


client = secretmanager.SecretManagerServiceClient()
gcp_project_id = "optical-unison-356814"

aws_access_key_id = get_secret(client, gcp_project_id, "aws_access_key_id")
aws_secret_access_key = get_secret(client, gcp_project_id, "aws_secret_access_key")
aws_account_number = get_secret(client, gcp_project_id, "aws_account_number")
