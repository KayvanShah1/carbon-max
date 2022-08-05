resource "google_secret_manager_secret" "aws_access_key_id" {
  secret_id = "aws_access_key_id"

  labels = {
    label = "aws-account-secret"
  }

  replication {
    automatic = true
  }
}


resource "google_secret_manager_secret_version" "aws_access_key_id" {
  secret = google_secret_manager_secret.aws_access_key_id.id

  secret_data = var.aws_access_key_id
}

resource "google_secret_manager_secret" "aws_secret_access_key" {
  secret_id = "aws_secret_access_key"

  labels = {
    label = "aws-account-secret"
  }

  replication {
    automatic = true
  }
}


resource "google_secret_manager_secret_version" "aws_secret_access_key" {
  secret = google_secret_manager_secret.aws_secret_access_key.id

  secret_data = var.aws_secret_access_key
}

# AWS Account Number
resource "google_secret_manager_secret" "aws_account_number" {
  secret_id = "aws_account_number"

  labels = {
    label = "aws-account-secret"
  }

  replication {
    automatic = true
  }
}


resource "google_secret_manager_secret_version" "aws_account_number" {
  secret = google_secret_manager_secret.aws_account_number.id

  secret_data = var.aws_account_number
}
