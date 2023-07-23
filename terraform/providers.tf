provider "kubernetes" {
  config_path = "~/.kube/config"
}

terraform {
  backend "s3" {
    bucket = "terraform-tfstate-loc"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}