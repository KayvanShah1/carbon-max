variable "gcp_project_id" {
  default = "optical-unison-356814"
}

variable "gcp_region" {
  default = "asia-south1"
}

variable "gcp_low_carbon_region" {
  default = "us-central1"
}

variable "source_code" {
  default = "../src"
}

variable "lambda_func_source_code" {
  default = "../lambda"
}

variable "aws_region" {
  default = "us-east-1"
}

variable "gcp_service_account_key_json_path" {}

variable "aws_access_key_id" {}

variable "aws_secret_access_key" {}

variable "aws_account_number" {}
