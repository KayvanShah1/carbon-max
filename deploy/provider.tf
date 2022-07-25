terraform {
  backend "gcs" {
    bucket      = "terraform-state-manager"
    prefix      = "terraform/state"
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
  }
}

provider "google" {
  # Configuration options
  project     = var.project_id
  credentials = var.service_account_key_json_path
}

provider "google-beta" {
  project     = var.project_id
  credentials = var.service_account_key_json_path
}
