data "archive_file" "source" {
  type        = "zip"
  source_dir  = var.source_code
  output_path = "${path.root}/tmp/function.zip"
}

data "archive_file" "lambda_function_source" {
  type        = "zip"
  source_dir  = var.lambda_func_source_code
  output_path = "${path.root}/tmp/lambda_function.zip"
}
