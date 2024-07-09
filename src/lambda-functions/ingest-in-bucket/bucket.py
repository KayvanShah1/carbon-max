import json

from io import BytesIO
from s3_bucket import S3Bucket


def connect_to_buffer_bucket(BUCKET_NAME="taiyo-projects"):
    """
    Connects to the specified S3 bucket.

    Args:
        BUCKET_NAME (str): The name of the S3 bucket to connect to. Defaults to "taiyo-projects".

    Returns:
        S3Bucket: The connected S3 bucket object.

    Raises:
        Exception: If there is an error connecting to the bucket.

    """
    bucket = None
    try:
        bucket = S3Bucket(bucket=BUCKET_NAME)
        print(f'Successfully connected to the bucket "{BUCKET_NAME}"')
        return bucket
    except Exception as e:
        print(f'{e}\nError connecting to bucket "{BUCKET_NAME}": Please check the credentials again.')


def push_json_to_buffer_bucket(bucket: S3Bucket, json_obj: dict, rel_path: str):
    """
    Pushes a JSON object to an S3 bucket.

    Args:
        bucket (S3Bucket): The S3 bucket to push the JSON object to.
        json_obj (dict): The JSON object to be pushed.
        rel_path (str): The relative path of the file in the bucket.

    Raises:
        Exception: If an error occurs while pushing the file to the bucket.

    Returns:
        None
    """
    try:
        buffer = BytesIO(
            bytes(
                json.dumps(json_obj),
                encoding="utf-8",
            ),
        )
        bucket.upload_file(fileobj=buffer, key=rel_path)
        print(f'Successfully pushed the json file to "{rel_path}"')
    except Exception as e:
        print(f'{e}\nError occured while pushing file to bucket path "{rel_path}"')


def read_json_from_buffer_bucket(bucket: S3Bucket, rel_path: str):
    """
    Reads a JSON file from an S3 bucket and returns the parsed JSON data.

    Args:
        bucket (S3Bucket): The S3 bucket object.
        rel_path (str): The relative path of the JSON file in the bucket.

    Returns:
        dict: The parsed JSON data.

    Raises:
        FileNotFoundError: If the specified file does not exist in the bucket.
        Exception: If there is an error while reading the JSON file.

    """
    try:
        buffer = BytesIO()
        key = list(bucket.search(rel_path))

        if not key:
            raise FileNotFoundError

        key = str(key[0].key)
        bucket.download_file(key=key, fileobj=buffer)
        buffer.seek(0)

        extension = rel_path.split(".")[-1]
        if extension == "json":
            json_data = json.load(buffer)
            return json_data
    except Exception as e:
        print(f"{e}\nFailed to read json from bucket.")
