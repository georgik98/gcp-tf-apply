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

module "vpc" {
  source = "./vpc"

  network_name    = var.network_name
  subnetwork_name = var.subnetwork_name
  ip_cidr_range   = var.ip_cidr_range
  region          = var.region
}

module "app_engine" {
  source = "./app_engine"

  region      = var.region
  bucket_name = var.bucket_name
}