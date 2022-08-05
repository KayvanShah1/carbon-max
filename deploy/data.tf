data "archive_file" "gcf_dump-into-bucket" {
  type        = "zip"
  source_dir  = "${var.gcloud_func_source_code}/dump-into-bucket"
  output_path = "${path.root}/tmp/gcf/dump-into-bucket.zip"
}

data "archive_file" "gcf_publish-message-to-sns" {
  type        = "zip"
  source_dir  = "${var.gcloud_func_source_code}/publish-message-to-sns"
  output_path = "${path.root}/tmp/gcf/publish-message-to-sns.zip"
}

data "archive_file" "lf_ingest-in-bucket" {
  type        = "zip"
  source_dir  = "${var.lambda_func_source_code}/ingest-in-bucket"
  output_path = "${path.root}/tmp/lf/ingest-in-bucket.zip"
}
