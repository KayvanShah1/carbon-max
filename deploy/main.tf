# Creates a GCS Bucket to store messages
resource "google_storage_bucket" "bucket" {
  provider                    = google
  name                        = "${var.gcp_project_id}-test-bucket"
  location                    = var.gcp_region
  uniform_bucket_level_access = true
  force_destroy               = true
}

# Create a GCS bucket to store Cloud Functions
resource "google_storage_bucket" "cloud_functions_bucket" {
  name          = "${var.gcp_project_id}-cloud_functions"
  location      = var.gcp_region
  force_destroy = true
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "zip" {
  source       = data.archive_file.source.output_path
  content_type = "application/zip"

  name   = "src-${data.archive_file.source.output_md5}.zip"
  bucket = google_storage_bucket.cloud_functions_bucket.name

  depends_on = [
    google_storage_bucket.cloud_functions_bucket,
    data.archive_file.source
  ]
}

# Create a Pub/Sub Topic
resource "google_pubsub_topic" "test_topic" {
  name    = "test-topic"
  project = var.gcp_project_id

  labels = {
    foo = "bar"
  }

  message_retention_duration = "86600s"
}

# Create a Subscription to Pub/Sub Topic with pull delivery
resource "google_pubsub_subscription" "test_subscription" {
  name  = "test-subscription"
  topic = google_pubsub_topic.test_topic.name

  ack_deadline_seconds    = 20
  enable_message_ordering = false

  labels = {
    foo = "bar"
  }
}

# Create a Gen1 Cloud Function
resource "google_cloudfunctions_function" "test_function" {
  name        = "test-function"
  description = "Pulls the messages from Google Pub/Sub subscription"
  region      = var.gcp_region

  labels = {
    my-label = "testing"
  }

  runtime     = "python38"
  entry_point = "test_function" # Set the entry point 

  source_archive_bucket = google_storage_bucket.cloud_functions_bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.test_topic.name
    failure_policy {
      retry = true
    }
  }
}

# Create a Gen2 Cloud Function
# resource "google_cloudfunctions2_function" "test_function" {
#   name        = "test-function"
#   location    = var.gcp_region
#   description = "Pulls the messages from Google Pub/Sub subscription"

#   build_config {
#     runtime     = "python38"
#     entry_point = "test_function" # Set the entry point 
#     source {
#       storage_source {
#         bucket = google_storage_bucket.cloud_functions_bucket.name
#         object = google_storage_bucket_object.zip.name
#       }
#     }
#   }

#   service_config {
#     max_instance_count = 3
#     min_instance_count = 1
#     available_memory   = "256M"
#     timeout_seconds    = 60
#   }

#   event_trigger {
#     trigger_region = var.gcp_low_carbon_region
#     event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
#     pubsub_topic   = google_pubsub_topic.test_topic.name
#     retry_policy   = "RETRY_POLICY_RETRY"
#   }
# }

# Create a S3 Bucket to store the messages
resource "aws_s3_bucket" "test_bucket" {
  bucket = "${var.gcp_project_id}-tf-test-bucket"
}

# Create a S3 Bucket to store the lambda functions source code zip files
resource "aws_s3_bucket" "test_bucket_lambda_functions" {
  bucket = "${var.gcp_project_id}-tf-test-bucket-lambda-functions"
}

# Storing lambda functions source code zip files in a S3 bucket
resource "aws_s3_object" "test_object_zip" {
  bucket = aws_s3_bucket.test_bucket_lambda_functions.bucket
  key    = "src-${var.gcp_project_id}-tf-test-lambda-function.zip"
  source = data.archive_file.lambda_function_source.output_path

  # etag = filemd5(data.archive_file.lambda_function_source.output_path)
}

# Create SNS Topic
resource "aws_sns_topic" "user_updates" {
  name = "user-updates-topic"
  delivery_policy = jsonencode({
    "http" : {
      "defaultHealthyRetryPolicy" : {
        "minDelayTarget" : 20,
        "maxDelayTarget" : 20,
        "numRetries" : 3,
        "numMaxDelayRetries" : 0,
        "numNoDelayRetries" : 0,
        "numMinDelayRetries" : 0,
        "backoffFunction" : "linear"
      },
      "disableSubscriptionOverrides" : false,
      "defaultThrottlePolicy" : {
        "maxReceivesPerSecond" : 1
      }
    }
  })
}

# Create SQS Queue for messages
resource "aws_sqs_queue" "user_updates_queue" {
  name                      = "user-updates-queue"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
  # redrive_policy = jsonencode({
  #   deadLetterTargetArn = aws_sqs_queue.terraform_queue_deadletter.arn
  #   maxReceiveCount     = 4
  # })
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Id" : "sqspolicy",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : "*",
        "Action" : ["sqs:*", "lambda:*"],
      }
    ]
  })
}

# Create a subscription to SNS Topic and attach it to the SQS Queue
resource "aws_sns_topic_subscription" "user_updates_sqs_target" {
  topic_arn = aws_sns_topic.user_updates.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.user_updates_queue.arn
}

# Create an IAM role to use lambda function as a service 
resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : ["sts:AssumeRole"],
          "Principal" : {
            "Service" : "lambda.amazonaws.com"
          },
          "Effect" : "Allow",
          "Sid" : ""
        }
      ]
  })
}

# Create an IAM Policy with permissions to use lambda and SQS
resource "aws_iam_policy" "lambda_sqs_policy" {
  name        = "lambda_sqs_policy"
  path        = "/"
  description = "IAM policy for SQS Message Recipients from a lambda"

  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Action" : [
            "sqs:*", "lambda:*"
          ],
          "Resource" : "*",
          "Effect" : "Allow"
        }
      ]
  })
}

# Attach the IAM Policy to the IAM Role
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_sqs_policy.arn
}

# Create a lambda function from the source archive object from S3 bucket
resource "aws_lambda_function" "test_lambda" {
  function_name = "${var.gcp_project_id}-tf-lambda-function-test"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "main.lambda_handler"

  s3_bucket = aws_s3_bucket.test_bucket_lambda_functions.bucket
  s3_key    = aws_s3_object.test_object_zip.key

  runtime = "python3.9"
}

# Add event source mapping to
resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn = aws_sqs_queue.user_updates_queue.arn
  function_name    = aws_lambda_function.test_lambda.arn
}
