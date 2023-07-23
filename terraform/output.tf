output "customer_site_service_ip" {
  value = "${data.kubernetes_service.customer-site-service-data.status.0.load_balancer.0.ingress.0.ip}:${kubernetes_service.customer-site-service.spec[0].port[0].port}"
}