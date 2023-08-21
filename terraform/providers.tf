provider "kubernetes" {
  config_path = "~/.kube/config"
}

# terraform {
#   backend "s3" {
#     bucket = "terraform-tfstate-loc"
#     key    = "terraform.tfstate"
#     region = "us-east-1"
#   }
# }

terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "devops-demo-2023"
    workspaces {
      prefix = "CustomerRegistrationSite-"
    }
  }
}