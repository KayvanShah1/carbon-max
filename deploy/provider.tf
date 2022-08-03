terraform {
  backend "gcs" {
    bucket      = "terraform-state-manager"
    prefix      = "dummy_project"
    credentials = "../credentials/optical-unison-356814-b09dbfb16473.json"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.29.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 3.83.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.2.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.24.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "google" {
  # Configuration options
  project     = var.gcp_project_id
  credentials = var.gcp_service_account_key_json_path
}

provider "google-beta" {
  project     = var.gcp_project_id
  credentials = var.gcp_service_account_key_json_path
}
