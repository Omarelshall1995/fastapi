
# FastAPI WebSocket Service Deployment Steps

This project demonstrates how to deploy a FastAPI WebSocket service on Kubernetes with Docker, Helm, and Prometheus for monitoring.

## Prerequisites:
- Azure account
- Azure CLI installed
- kubectl installed
- Helm installed
- Terraform installed
- Docker installed
- GitHub Actions setup (optional)

## Directory Structure:

- **kubernetes**: Kubernetes deployment files (manifests, helm charts)
- **.github**: GitHub Actions workflows (if using CI/CD)
- **app.py**: FastAPI application code
- **client.py**: WebSocket client that connects to the WebSocket server (needs URI adjustment)
- **Dockerfile**: Docker image setup for the FastAPI service
- **requirements.txt**: Python dependencies
- **README.md**: This file

## Step 1: Clone the repository

Clone the repository to your local machine:

```
git clone <repo_url>
cd FastAPI-WebSocket
```

## Step 2: Set up the WebSocket Client

In **client.py**, you'll need to update the WebSocket URI to match your Ingress controller:

```python
uri = "ws://<YOUR_INGRESS_CONTROLLER>/ws/stocks"
```

Replace `<YOUR_INGRESS_CONTROLLER>` with the address of your Ingress controller.

## Step 3: Build the Docker Image

To build the Docker image, use the following command:

```
docker build -t <your_dockerhub_username>/fastapi-websocket .
```

Push the Docker image to DockerHub:

```
docker push <your_dockerhub_username>/fastapi-websocket
```

## Step 4: Deploy with Kubernetes

### Helm Deployment:
1. Navigate to the **kubernetes/helm** directory.
2. Install the Helm chart to deploy the service on Kubernetes:

```bash
helm install websocket-service ./helm
```

3. Verify that the deployment is successful:

```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

### Terraform Deployment:
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

1. Install Prometheus with Helm:

```bash
helm install prometheus prometheus-community/prometheus -n monitoring --create-namespace
```

2. Verify the Prometheus pods are running:

```bash
kubectl get pods -n monitoring
```

## Step 6: Clean Up (Optional)

To destroy the resources created by Terraform:

```bash
terraform destroy -auto-approve
```

## Notes:

- When using the WebSocket client, ensure the URI is updated to match your Ingress controller's address.
- The Docker image has been deployed on DockerHub, and you can pull it using:

```bash
docker pull <your_dockerhub_username>/fastapi-websocket
```

- Make sure to monitor the service with Prometheus after deployment for health checks and metrics.
