resource "kubernetes_namespace" "customer-site" {
  metadata {
    name = "customer-site"
  }
}

resource "kubernetes_deployment" "customer-site-deployment" {
  metadata {
    name      = "customer-site-deployment"
    namespace = kubernetes_namespace.customer-site.metadata.0.name
    labels = {
      app = "customer-site"
    }
  }
  spec {
    replicas = var.customer_site_replicas
    selector {
      match_labels = {
        app = "customer-site"
      }
    }
    template {
      metadata {
        labels = {
          app = "customer-site"
        }
      }
      spec {
        container {
          image = var.customer_site_image
          name  = "customer-site"
          port {
            container_port = var.customer_site_port
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "customer-site-service" {
  metadata {
    name      = "customer-site-service"
    namespace = kubernetes_namespace.customer-site.metadata.0.name
  }
  spec {
    selector = {
      app = "customer-site"
    }
    port {
      port        = var.customer_site_external_port
      target_port = var.customer_site_port
    }
    type = "LoadBalancer"
  }
}

data "kubernetes_service" "customer-site-service-data" {
  metadata {
    name      = kubernetes_service.customer-site-service.metadata[0].name
    namespace = kubernetes_namespace.customer-site.metadata[0].name
  }
}