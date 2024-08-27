# Makefile to build and deploy RevWallet in K8s and Docker Compose

.PHONY: \
	nginx \
	api \
	db \
	prometheus \
	alloy \
	loki \
	grafana \
	deploy \
	delete-nginx \
	delete-api \
	delete-db \
	delete-prometheus \
	delete-alloy \
	delete-loki \
	delete-grafana \
	delete \
	compose-up \
	compose-down \
	create \
	setup-helm \
	terminate \
	tests


################################## Tests Targets #############################
tests:
	pipenv sync --dev
	pipenv run pytest


################################## Docker Compose Targets #############################
compose-up:
	pipenv sync
	docker compose up -d --build

compose-down:
	docker compose down -v

################################ K8s Targets (Local) #################################

create:
	kind create cluster --name revwallet
	kubectl create namespace revwallet-dev
	kubectl config set-context kind-revwallet --namespace=revwallet-dev
	$(MAKE) setup-helm

setup-helm:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo add revwallet-api https://arthurjguerra.github.io/revwallet
	helm repo update

terminate:
	$(MAKE) delete
	helm repo remove bitnami grafana prometheus-community
	kind delete cluster --name revwallet

deploy:
	$(MAKE) db
	$(MAKE) prometheus
	$(MAKE) alloy
	$(MAKE) loki
	$(MAKE) grafana
	$(MAKE) api
	$(MAKE) nginx

db:
	helm repo update
	kubectl -n revwallet-dev apply -f helm/revwallet-db/secrets.yaml
	helm -n revwallet-dev upgrade --install --values helm/revwallet-db/values.yaml revwallet-db bitnami/postgresql

api:
	kubectl -n revwallet-dev wait --timeout=5m --for=condition=Ready pod -l app=revwallet-db

	helm repo update
	helm -n revwallet-dev upgrade --install --values helm/revwallet-api/values.yaml revwallet-api revwallet-api/revwallet-api

prometheus:
	helm repo update prometheus-community
	helm -n revwallet-dev upgrade --install --values helm/prometheus/values.yaml prometheus prometheus-community/prometheus

alloy:
	kubectl -n revwallet-dev delete configmap alloy-config >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap alloy-config --from-file=helm/alloy/config.alloy

	helm repo update grafana
	helm -n revwallet-dev upgrade --install --values helm/alloy/values.yaml alloy grafana/alloy

loki:
	helm repo update grafana
	helm -n revwallet-dev upgrade --install --values helm/loki/values.yaml loki grafana/loki-stack

grafana:
	kubectl -n revwallet-dev wait --timeout=5m --for=condition=Ready pod -l app=loki
	kubectl -n revwallet-dev wait --timeout=5m --for=condition=Ready pod -l app=prometheus

	kubectl -n revwallet-dev delete configmap revwallet-dashboard >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap revwallet-dashboard --from-file=config/grafana/dashboard.json

	helm repo update grafana
	helm -n revwallet-dev upgrade --install --values helm/grafana/values.yaml grafana grafana/grafana

nginx:
	kubectl -n revwallet-dev get pods

	kubectl describe pod -l app=revwallet-api

	$(MAKE) stop-port-forward

	sleep 45
	kubectl describe pod -l app=revwallet-api

	kubectl -n revwallet-dev wait --timeout=5m --for=condition=Ready pod -l app=revwallet-api
	kubectl -n revwallet-dev wait --timeout=5m --for=condition=Ready pod -l app=prometheus
	kubectl -n revwallet-dev wait --timeout=5m --for=condition=Ready pod -l app=grafana

	kubectl -n revwallet-dev delete configmap nginx-html >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap nginx-html --from-file=config/nginx/revwallet.html --from-file=config/nginx/404.html 

	kubectl -n revwallet-dev delete configmap nginx-conf >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap nginx-conf --from-file=helm/nginx/nginx.conf

	helm repo update bitnami
	helm -n revwallet-dev upgrade --install --values helm/nginx/values.yaml nginx bitnami/nginx

	$(MAKE) port-forward

delete:
	$(MAKE) stop-port-forward
	$(MAKE) delete-nginx 
	$(MAKE) delete-api
	$(MAKE) delete-db
	$(MAKE) delete-prometheus
	$(MAKE) delete-alloy
	$(MAKE) delete-loki
	$(MAKE) delete-grafana

delete-nginx:
	$(MAKE) stop-port-forward
	kubectl -n revwallet-dev delete configmap nginx-conf >/dev/null 2>&1 || true
	kubectl -n revwallet-dev delete configmap nginx-html >/dev/null 2>&1 || true
	helm -n revwallet-dev uninstall nginx

delete-alloy:
	helm -n revwallet-dev uninstall alloy
	kubectl -n revwallet-dev delete configmap alloy-config

delete-loki:
	helm -n revwallet-dev uninstall loki

delete-grafana:
	kubectl -n revwallet-dev delete configmap revwallet-dashboard >/dev/null 2>&1 || true
	helm -n revwallet-dev uninstall grafana

delete-prometheus:
	helm -n revwallet-dev uninstall prometheus

delete-api:
	helm -n revwallet-dev uninstall revwallet-api

delete-db:
	kubectl -n revwallet-dev delete -f helm/revwallet-db/secrets.yaml
	helm -n revwallet-dev uninstall revwallet-db

################################## Utils Targets #############################
port-forward:
	bash scripts/port-forward

stop-port-forward:
	bash scripts/port-forward --stop

data:
	bash scripts/generate-data

help:
	@echo "RevWallet Makefile Usage:"
	@echo "  make help                 - Display this help message."
	@echo "  make create               - Create a local k8s cluster with kind."
	@echo "  make deploy               - Deploy the API and all dependencies on k8s."
	@echo "  make db                   - Deploy only the RevWallet database on k8s."
	@echo "  make prometheus           - Deploy only Prometheus on k8s."
	@echo "  make alloy                - Deploy only Alloy on k8s."
	@echo "  make loki                 - Deploy only Loki on k8s."
	@echo "  make grafana              - Deploy only Grafana on k8s."
	@echo "  make api                  - Deploy only the RevWallet API on k8s."
	@echo "  make nginx                - Deploy only Nginx on k8s."
	@echo "  make test                 - Run the tests."
	@echo "  make data                 - Generate sample data."
	@echo "  make compose-up           - Start RevWallet API and dependencies with Docker Compose."
	@echo "  make compose-down         - Stop RevWallet API and dependencies with Docker Compose."
	@echo "  make terminate            - Delete all the running pods and terminate the k8s cluster."
	@echo "  make port-forward         - Start port forwarding to Nginx."
	@echo "  make stop-port-forward    - Stop port forwarding to Nginx."
	@echo "  make setup-helm           - Install Helm repositories."
	@echo "  make delete               - Delete the RevWallet API and all dependencies on k8s."
	@echo "  make delete-db            - Delete only the RevWallet DB on k8s."
	@echo "  make delete-prometheus    - Delete only Prometheus on k8s."
	@echo "  make delete-alloy         - Delete only Alloy on k8s."
	@echo "  make delete-loki          - Delete only Loki on k8s."
	@echo "  make delete-grafana       - Delete only Grafana on k8s."
	@echo "  make delete-api           - Delete only the RevWallet API on k8s."
	@echo "  make delete-nginx         - Delete only Nginx deployment on k8s."
