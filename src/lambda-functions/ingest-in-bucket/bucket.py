import json

from io import BytesIO
from s3_bucket import S3Bucket


def connect_to_buffer_bucket(BUCKET_NAME="taiyo-projects"):
    bucket = None
    try:
        bucket = S3Bucket(bucket=BUCKET_NAME)
        print(f'Successfully connected to the bucket "{BUCKET_NAME}"')
        return bucket
    except Exception as e:
        print(
            f'{e}\nError connecting to bucket "{BUCKET_NAME}": Please check the credentials again.'
        )


def push_json_to_buffer_bucket(bucket: S3Bucket, json_obj: dict, rel_path: str):
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
