# RevWallet in Kubernetes with Kind

Wallet API where users can deposit, withdraw, and check the balance of a wallet. You can run RevWallet on Kubernetes with [Kind](https://kind.sigs.k8s.io/) and [Helm](https://helm.sh/).

## Requirements
RevWallet is a [Flask](https://flask.palletsprojects.com/en/3.0.x/) application that runs on Docker. To get started, ensure you have the following dependencies installed on your system:
- [Docker](https://docs.docker.com/guides/getting-started/)
- [Docker Compose](https://docs.docker.com/compose/gettingstarted/)
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Kubectl](https://kubernetes.io/docs/reference/kubectl/)
- [Helm](https://helm.sh/docs/intro/quickstart/)
- [Python 3.12](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)

If you use `brew`, you can install the necessary dependencies by running:
```
brew install docker
brew install kind
brew install helm
brew install python@3.12
brew install pipenv
```

## Running RevWallet on K8s (locally)
To run RevWallet on Kubernetes (locally), follow these steps:

1. Create a local Kubernetes clusters with `kind`:
```
kind create cluster --name revwallet
kind get clusters
```
2. Create a new namespace:
```
kubectl create namespace revwallet-dev
kubectl config set-context kind-revwallet --namespace=revwallet-dev
kubectl get pods
```
3. Deploy the database:
```
kubectl apply -f helm/revwallet-db
```
If you want to make sure the DB is deployed correctly, you can run the following commands to check if resources were created properly:
```
kubectl get pv
kubectl get pvc
kubectl get deployments
kubectl get pods
kubectl get svc
```
You can also connect to the DB:
```
kubectl exec -it <POD> -- psql -h localhost -U revwallet --password -p 5432 revwallet
```
And verify the connection to the DB:
```
\conninfo
```
Expected response:
```
Password:
psql (16.4 (Debian 16.4-1.pgdg120+1))
Type "help" for help.

revwallet=# \connect
Password:
You are now connected to database "revwallet" as user "revwallet".
revwallet=#
```
4. Deploy Alloy:
```
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
kubectl -n revwallet-dev create configmap alloy-config --from-file=config/alloy/config.alloy
helm -n revwallet-dev upgrade --install --values helm/alloy/values.yaml alloy grafana/alloy
```
5. Deploy Loki:
```
helm repo update
helm -n revwallet-dev upgrade --install --values helm/loki/values.yaml loki grafana/loki-stack
```
6. Deploy Prometheus:
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm -n revwallet-dev upgrade --install --values helm/prometheus/values.yaml prometheus prometheus-community/prometheus
```
7. Deploy Grafana:
```
helm repo update
kubectl -n revwallet-dev create configmap revwallet-dashboard --from-file=config/grafana/dashboard.json
helm -n revwallet-dev upgrade --install --values helm/grafana/values.yaml grafana grafana/grafana
```
8. Deploy the API:
```
helm -n revwallet-dev upgrade --install --values charts/revwallet-api-/values.yaml revwallet-api helm/revwallet-api
```
9. Deploy Nginx:
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
kubectl -n revwallet-dev create configmap nginx-html --from-file=config/nginx/revwallet.html --from-file=config/nginx/404.html 
kubectl -n revwallet-dev create configmap nginx-conf --from-file=config/nginx/nginx.conf
helm -n revwallet-dev upgrade --install --values helm/nginx/values.yaml nginx bitnami/nginx
```
To access the app, first, run:
```
kubectl -n revwallet-dev port-forward pod/<NGINX_POD> 8080:8080
```
Then, access the app at http://localhost:8080

## Shutting Down
To clean everything up, run:
```
helm -n revwallet-dev uninstall nginx
helm -n revwallet-dev uninstall alloy
helm -n revwallet-dev uninstall loki
helm -n revwallet-dev uninstall grafana
helm -n revwallet-dev uninstall prometheus
helm -n revwallet-dev uninstall revwallet-api
helm repo remove grafana prometheus-community bitnami
kubectl -n revwallet-dev delete -f helm/revwallet-db
kubectl -n revwallet-dev delete configmap revwallet-dashboard
kubectl -n revwallet-dev delete configmap nginx-conf
kubectl -n revwallet-dev delete configmap nginx-html
```

To delete the cluster, run:
```
kind delete cluster --name revwallet
```

## Running Tests
RevWallet has both unit and end-to-end tests. First, activate the virtual environment and sync dependencies:
```
pipenv shell
pipenv sync --dev
```

Now, make sure the API is accessible from `localhost`:
```
kubectl -n revwallet-dev port-forward <NGINX_POD> 8080:8080
```

Then, run the tests:
```
pipenv run pytest
```
