
# FastAPI WebSocket Service Deployment Steps

This project demonstrates how to deploy a FastAPI WebSocket service on Kubernetes with Docker, Helm, and Prometheus for monitoring. You can monitor the service's health using **Prometheus** and **Blackbox Exporter**.

## Prerequisites:
- Azure account
- Azure CLI installed
- kubectl installed
- Helm installed
- Terraform installed (optional for AKS infrastructure)
- Docker installed
- GitHub Actions setup (optional for CI/CD)
- WebSocket service Docker image: `Oshall95/websocket-service:latest`

## Directory Structure:

- **kubernetes**: Kubernetes deployment files (manifests, Helm charts)
- **.github**: GitHub Actions workflows (if using CI/CD)
- **app.py**: FastAPI application code
- **client.py**: WebSocket client (adjust URI to match your ingress)
- **Dockerfile**: Docker image setup for the FastAPI service
- **requirements.txt**: Python dependencies
- **README.md**: This file

## Step 1: Clone the repository

Clone the repository to your local machine:

```bash
git clone <repo_url>
cd FastAPI-WebSocket
```

## Step 2: Set up the WebSocket Client

In **client.py**, update the WebSocket URI to match your Ingress controller:

```python
uri = "ws://<YOUR_INGRESS_CONTROLLER>/ws/stocks"
```

Replace `<YOUR_INGRESS_CONTROLLER>` with the address of your Ingress controller.

## Step 3: Docker Image (Optional, if not using pre-built image)

If you need to build the Docker image for the service, run the following command:

```bash
docker build -t Oshall95/websocket-service:latest .
```

If you want to skip this and use the pre-built image, you can **pull it** from DockerHub:

```bash
docker pull Oshall95/websocket-service:latest
```

## Step 4: Deploy the WebSocket Service with Helm

1. Navigate to the **kubernetes/helm** directory:

```bash
cd kubernetes/helm
```

2. Install the Helm chart to deploy the service on Kubernetes:

```bash
helm install websocket-service ./webservice-chart
```

3. Verify that the deployment is successful:

```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

### Optional: Deploy AKS with Terraform

If you need to deploy an AKS cluster using Terraform:

1. Initialize Terraform:

```bash
terraform init
```

2. Define the infrastructure in **main.tf**.

3. Apply the configuration to create the AKS cluster:

```bash
terraform apply -auto-approve
```

4. Verify the deployment:

```bash
az aks get-credentials --resource-group <resource_group_name> --name <aks_cluster_name> --overwrite-existing
kubectl get nodes
```

## Step 5: Monitoring with Prometheus

1. **Install Prometheus with Helm**:

```bash
helm install prometheus prometheus-community/prometheus -n monitoring --create-namespace
```

2. **Verify the Prometheus pods are running**:

```bash
kubectl get pods -n monitoring
```

3. **Access Prometheus**:

   If you need to access Prometheus, you can port-forward it to your local machine:

   ```bash
   kubectl port-forward -n monitoring svc/prometheus-server 9090:9090
   ```

   After running the above command, you can access Prometheus at:

   ```
   http://localhost:9090
   ```

## Step 6: Set up Blackbox Exporter

1. **Install Blackbox Exporter** using Helm:

   ```bash
   helm install blackbox-exporter prometheus-community/prometheus-blackbox-exporter -n monitoring --create-namespace
   ```

2. **Access Blackbox Exporter**:

   Similarly, port-forward the Blackbox Exporter service to access it locally:

   ```bash
   kubectl port-forward -n monitoring svc/blackbox-exporter 9115:9115
   ```

   You can then visit Blackbox Exporter’s status page:

   ```
   http://localhost:9115
   ```

## Step 7: Clean Up (Optional)

To destroy the resources created by Terraform:

```bash
terraform destroy -auto-approve
```



## Notes:

- When using the WebSocket client, ensure the URI is updated to match your Ingress controller's address.
- The Docker image **`Oshall95/websocket-service:latest`** has already been pushed to DockerHub, so you can skip the build step and pull the image directly.
- To monitor the service with Prometheus, make sure that Prometheus and Blackbox Exporter are properly set up, and port-forward the services if necessary.
- If you haven't set up Prometheus scraping for Blackbox Exporter, you will need to modify your `prometheus.yml` configuration file to include the Blackbox Exporter targets and configure relabeling rules accordingly.
