resource "google_app_engine_application" "app" {
  location_id = var.region
}

resource "google_app_engine_standard_app_version" "default" {
  service    = "default"
  version_id = "v1"
  runtime    = "python39"
  entrypoint {
    shell = "gunicorn -b :$PORT app:app"
  }

  deployment {
    zip {
      source_url = google_storage_bucket_object.app_files.self_link
    }
  }

  env_variables = {
    FLASK_ENV = "production"
  }
}

# resource "google_storage_bucket" "app_bucket-1" {
#   name          = var.bucket_name
#   location      = var.region
#   force_destroy = true
# }

# resource "google_storage_bucket_object" "app_files" {
#   name   = "app.zip"
#   bucket = google_storage_bucket.app_bucket-1.name
#   source = "../app.zip"
# }