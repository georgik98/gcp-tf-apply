provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
}

terraform {
  backend "gcs" {
    bucket = "terraform-state-file-georgik16-new-1"
    prefix = "terraform-state"
  }
}