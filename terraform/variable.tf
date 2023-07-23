variable "customer_site_image" {
  description = "The image of the customer site"
  default     = "idrisniyi94/customer-registration:latest"
}

variable "customer_site_port" {
  description = "The port of the customer site"
  default     = 5000
}

variable "customer_site_external_port" {
  description = "The external port of the customer site"
  default     = 31356
}