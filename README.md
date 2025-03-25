
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

## ArgoCD Setup for CI/CD

### Step 1: Install ArgoCD
Install ArgoCD in your Kubernetes cluster using the following commands:

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Step 2: Expose the ArgoCD API Server
Expose the ArgoCD API server for web access using the following command:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

### Step 3: Get the Admin Password
Retrieve the initial admin password:

```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 --decode
```

### Step 4: Access ArgoCD UI
Open the ArgoCD UI by navigating to `http://localhost:8080` in your web browser. The default username is `admin`, and the password is the one retrieved in the previous step.

### Step 5: Connect ArgoCD to Your GitHub Repository
1. In ArgoCD, go to **Settings** > **Repositories** and add your GitHub repository where the Kubernetes manifests are stored.
2. After adding the repository, create an application by specifying the repository and the path where your Helm charts or Kubernetes manifests are located.

### Step 6: Automate Deployments
ArgoCD will automatically sync your Kubernetes manifests to your cluster every time changes are made to the GitHub repository. You can set this up for continuous deployment.

## GitHub Actions for CI/CD

1. **Create a Service Principal for Azure:**
   Run the following command to create a Service Principal in Azure:

```bash
az ad sp create-for-rbac --name github-actions --role contributor --scopes /subscriptions/<your-subscription-id> --sdk-auth
```

2. **Store Azure Credentials in GitHub Secrets:**
   - AZURE_CLIENT_ID
   - AZURE_CLIENT_SECRET
   - AZURE_SUBSCRIPTION_ID
   - AZURE_TENANT_ID

3. **Create GitHub Actions Workflow:**
   Create a GitHub Actions workflow file in the `.github/workflows/deploy.yml` directory. The workflow should contain the following steps:
   - Log into Azure using the stored secrets.
   - Build the Docker image and push it to DockerHub.
   - Deploy the Kubernetes resources using `kubectl apply -f kubernetes/`.

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v2

      - name: Log in to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Build Docker image
        run: |
          docker build -t <your_dockerhub_username>/fastapi-websocket .
          docker push <your_dockerhub_username>/fastapi-websocket

      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f kubernetes/
```

4. **Verify the Deployment:**
   Once the GitHub Actions workflow runs, verify the deployment by running the following commands:

```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

## Notes:

- Ensure the URI in the WebSocket client (client.py) is updated to match the Ingress controller's address.
- When using ArgoCD, make sure to link it to your GitHub repository for automatic synchronization.
- If there is an ingress conflict, ensure only one ingress resource is applied.

## Troubleshooting:
- In case of issues with ArgoCD syncing, check the ArgoCD logs and verify the repository connection.
- If you encounter issues with ingress resources, ensure the Ingress controller is properly configured and only one ingress resource is applied.

## Clean Up:

To remove the Helm release, run the following command:

```bash
helm uninstall websocket-service
```

To remove the ArgoCD resources:

```bash
kubectl delete namespace argocd
```

To remove the resources created by Terraform:

```bash
terraform destroy -auto-approve
```
