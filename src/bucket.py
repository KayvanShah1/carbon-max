from google.cloud import storage
import traceback

from io import BytesIO
import json


# Establish connection with Google Cloud Storage Bucket
def connect_to_buffer_bucket(
    BUCKET_NAME="psd_data",
):
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(BUCKET_NAME)
        print(f'Successfully connected to the bucket "{BUCKET_NAME}"')
        return bucket
    except Exception as e:
        print(
            f'{e}\nError connecting to bucket "{BUCKET_NAME}": Please check the credentials again.'
        )


# Push and read JSON from bucket
def read_json_from_buffer_bucket(bucket, rel_path: str):
    try:
        blob_object = bucket.blob(rel_path)
        json_data = blob_object.download_as_string()
        extension = rel_path.split(".")[-1]
        if extension == "json":
            json_data = json.load(BytesIO(json_data))
            return json_data
    except Exception as e:
        print(f"{e}\nFailed to read json from bucket.", traceback.format_exc())


def push_json_to_buffer_bucket(bucket, json_obj: dict, rel_path: str):
    try:
        data = bucket.blob(rel_path)
        data.upload_from_string(json.dumps(json_obj), "application/json")
        print(f'Successfully pushed the json file to "{rel_path}"')
    except Exception as e:
        print(
            f'{e}\nError occured while pushing file to bucket path "{rel_path}"',
            traceback.format_exc(),
        )
