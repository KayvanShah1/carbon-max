# GCP Configuration
variable "gcp_project_id" {
  type    = string
  default = "optical-unison-356814"
}

variable "gcp_region" {
  type    = string
  default = "asia-south1"
}

variable "gcp_low_carbon_region" {
  type    = string
  default = "us-central1"
}

variable "gcp_service_account_key_json_path" {}

# AWS Configuration
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "aws_access_key_id" {}

variable "aws_secret_access_key" {}

variable "aws_account_number" {}

# Source Code Variables
# variable "gcloud_func_source_code" {
#   type    = string
#   default = "../src/google-cloud-functions"
# }

# variable "lambda_func_source_code" {
#   type    = string
#   default = "../src/lambda-functions"
# }

# Local Constant Variables
locals {
  source = "../src"
  lambda = "${local.source}/lambda-functions"
  gcloud = "${local.source}/google-cloud-functions"
}

# Google Cloud & Lambda Functions
locals {
  gcloud_functions = {
    "dump-into-bucket" : "${local.gcloud}/dump-into-bucket",
    "publish-message-to-sns" : "${local.gcloud}/publish-message-to-sns"
  }
  lambda_functions = {
    "ingest-in-bucket" : "${local.lambda}/ingest-in-bucket",
  }
}
