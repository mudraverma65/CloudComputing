
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

  node_config {
    machine_type = "e2-standard-2"
    disk_size_gb = 100
    preemptible  = false
  }
}

resource "google_compute_disk" "kubernetes-cluster" {
  name  = "kubernetes-cluster"
  type  = "pd-standard"
  size  = 1
  zone  = "us-central1-a"
}