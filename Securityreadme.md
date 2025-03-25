# Security & Compliance Documentation

## 1. Container Security

### Image Scanning
Before deploying container images, we scanned them using **Trivy** to detect vulnerabilities.

#### Steps:
1. Install Trivy:
   ```sh
   curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh
   ```
2. Scan the Docker image:
   ```sh
   trivy image omarelshall1995/fastapi:latest
   ```
3. Review and address reported vulnerabilities.

### Restricting Unnecessary Ports
We ensured that only necessary ports were exposed in `kubernetes/deployment.yaml`:
```yaml
containers:
  - name: websocket-service
    image: omarelshall1995/fastapi:latest
    ports:
      - containerPort: 8000 # Only exposing required ports
```

---

## 2. Network Security

### Azure Private Link / NSG Configuration
To secure WebSocket communication, we implemented **Network Security Groups (NSGs)**:

#### Steps:
1. List available NSGs:
   ```sh
   az network nsg list --resource-group my-new-resource-group --output table
   ```
2. Create an NSG rule to allow only necessary traffic:
   ```sh
   az network nsg rule create --resource-group my-new-resource-group \
       --nsg-name my-nsg --name AllowWebSocket --priority 100 \
       --direction Inbound --access Allow --protocol Tcp \
       --source-port-ranges "*" --destination-port-ranges 8000
   ```
3. Associate the NSG with the AKS subnet:
   ```sh
   az network vnet subnet update --resource-group MC_my-new-resource-group_new-cluster-2_centralindia \
       --vnet-name aks-vnet-11597541 --subnet-name aks-subnet --network-security-group my-nsg
   ```

---

## 3. Authentication & Authorization

### JWT Authentication for WebSocket
We secured WebSocket connections using **JWT authentication**:

#### Steps:
1. Install PyJWT:
   ```sh
   pip install pyjwt
   ```
2. Modify `app.py` to validate JWT tokens:
   ```python
   from fastapi import WebSocket, WebSocketDisconnect, Depends
   import jwt

   SECRET_KEY = "your_secret_key"

   async def validate_token(token: str):
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
           return payload
       except jwt.ExpiredSignatureError:
           return None
       except jwt.InvalidTokenError:
           return None

   @app.websocket("/ws/stocks")
   async def stock_websocket(websocket: WebSocket, token: str = Depends(validate_token)):
       if not token:
           await websocket.close()
           return
       await websocket.accept()
   ```

---

## 4. Secrets Management

### Storing Secrets in Azure Key Vault
To securely store and retrieve sensitive information, we used **Azure Key Vault**.

#### Steps:
1. Create an Azure Key Vault:
   ```sh
   az keyvault create --name my-keyvault --resource-group my-new-resource-group --location centralindia
   ```
2. Store a secret:
   ```sh
   az keyvault secret set --vault-name my-keyvault --name "JWT-SECRET" --value "your_secret_key"
   ```
3. Retrieve the secret in Kubernetes:
   ```sh
   kubectl create secret generic jwt-secret --from-literal=JWT_SECRET=$(az keyvault secret show --name JWT-SECRET --vault-name my-keyvault --query value -o tsv)
   ```

---

## 5. Role-Based Access Control (RBAC)

### Implementing Kubernetes RBAC
We created an RBAC policy to restrict unnecessary access to the Kubernetes cluster.

#### Steps:
1. Define RBAC role in `kubernetes/rbac.yaml`:
   ```yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     namespace: default
     name: websocket-role
   rules:
   - apiGroups: [""]
     resources: ["pods", "services"]
     verbs: ["get", "list"]
   ```
2. Apply the RBAC policy:
   ```sh
   kubectl apply -f kubernetes/rbac.yaml
   ```

---

## 6. Enforcing TLS

### Enabling HTTPS using Let's Encrypt
We used **Cert-Manager** and **Let's Encrypt** to enforce HTTPS on WebSocket connections.

#### Steps:
1. Install Cert-Manager:
   ```sh
   kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
   ```
2. Create a ClusterIssuer for Let's Encrypt:
   ```yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata:
     name: letsencrypt-prod
   spec:
     acme:
       server: https://acme-v02.api.letsencrypt.org/directory
       email: your-email@example.com
       privateKeySecretRef:
         name: letsencrypt-prod
       solvers:
       - http01:
           ingress:
             class: nginx
   ```
3. Apply the certificate issuer:
   ```sh
   kubectl apply -f kubernetes/cluster-issuer.yaml
   ```

---

## Conclusion
This document outlines all security measures implemented to secure the WebSocket service, including **container security, network security, authentication, secrets management, RBAC, and TLS enforcement**. Each section provides exact steps for replication.

