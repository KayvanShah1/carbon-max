from datetime import datetime
import json

from bucket import connect_to_buffer_bucket, push_json_to_buffer_bucket


def generate_path(date):
    path = (
        f"sample_data/year={date.year}/month={date.month}/day={date.day}"
        f"/file_{date.strftime('%Y%m%d%H%M%S')}.json"
    )
    return path


def lambda_handler(event, context):
    bucket = connect_to_buffer_bucket("optical-unison-356814-tf-test-bucket")
    path = generate_path(datetime.now())
    for record in event["Records"]:
        record["body"] = json.loads(record["body"])

    push_json_to_buffer_bucket(bucket, path)
