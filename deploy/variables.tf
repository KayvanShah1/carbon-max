variable "gcp_project_id" {
  default = "optical-unison-356814"
}

variable "gcp_region" {
  default = "asia-south1"
}

variable "gcp_low_carbon_region" {
  default = "us-central1"
}

variable "gcp_service_account_key_json_path" {
  default = "../credentials/optical-unison-356814-b09dbfb16473.json"
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
