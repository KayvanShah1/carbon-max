data "archive_file" "source" {
  type        = "zip"
  source_dir  = var.source_code
  output_path = "/tmp/function.zip"
}
