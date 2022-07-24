# Creates a GCS Bucket to store messages
resource "google_storage_bucket" "bucket" {
  provider                    = google
  name                        = "test-bucket"
  location                    = var.region
  uniform_bucket_level_access = true
}

# Create a GCS bucket to store Cloud Functions
resource "google_storage_bucket" "cloud_functions_bucket" {
  name     = "${var.project_id}-cloud_functions"
  location = var.region
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
  project = var.project_id

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

  labels = {
    my-label = "testing"
  }

  runtime     = "python38"
  entry_point = "test_function" # Set the entry point 

  source_archive_bucket = google_storage_bucket.cloud_functions_bucket.name
  source_archive_object = google_storage_bucket_object.zip.name

  event_trigger {
    event_type = "google.cloud.pubsub.topic.v1.messagePublished"
    resource   = google_pubsub_topic.test_topic.name
    failure_policy {
      retry = true
    }
  }


}

# Create a Gen2 Cloud Function
# resource "google_cloudfunctions2_function" "test_function" {
#   name        = "test-function"
#   location    = var.region
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
#     trigger_region = var.low_carbon_region
#     event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
#     pubsub_topic   = google_pubsub_topic.test_topic.name
#     retry_policy   = "RETRY_POLICY_RETRY"
#   }
# }
