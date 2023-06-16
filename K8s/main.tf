# Configure the Google Cloud provider
provider "google" {
  project = "b00932103-5409"
  region  = "us-central1"
  zone    = "us-central1-a"
}

# Create a GKE cluster
resource "google_container_cluster" "kubernetes-cluster" {
  name               = "kubernetes-cluster"
  location           = "us-central1"
  initial_node_count = 1

  # Node configuration
  node_config {
    service_account = "254065696491-compute@developer.gserviceaccount.com"
    machine_type   = "e2-micro"
    disk_size_gb   = 10
    image_type     = "COS_CONTAINERD"
  }
}




