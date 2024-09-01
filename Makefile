# Makefile to build and deploy RevWallet in K8s and Docker Compose

.PHONY: \
	local-nginx \
	local-api \
	local-db \
	local-prometheus \
	local-alloy \
	local-loki \
	local-grafana \
	local-deploy \
	local-delete-nginx \
	local-delete-api \
	local-delete-db \
	local-delete-prometheus \
	local-delete-alloy \
	local-delete-loki \
	local-delete-grafana \
	local-delete \
	compose-up \
	compose-down \
	local-create \
	setup-helm \
	local-terminate \
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

local-create:
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

local-terminate:
	$(MAKE) local-delete
	helm repo remove bitnami grafana prometheus-community
	kind delete cluster --name revwallet

local-deploy:
	$(MAKE) local-db
	$(MAKE) local-prometheus
	$(MAKE) local-alloy
	$(MAKE) local-loki
	$(MAKE) local-grafana
	$(MAKE) local-api
	$(MAKE) local-nginx

local-db:
	helm repo update
	kubectl -n revwallet-dev apply -f helm/revwallet-db/secrets.yaml
	helm -n revwallet-dev upgrade --install --values helm/revwallet-db/values.yaml revwallet-db bitnami/postgresql

local-api:
	kubectl -n revwallet-dev wait --timeout=5m --for=condition=Ready pod -l app=revwallet-db

	helm repo update
	helm -n revwallet-dev upgrade --install --values helm/revwallet-api/values.yaml revwallet-api revwallet-api/revwallet-api

local-prometheus:
	helm repo update prometheus-community
	helm -n revwallet-dev upgrade --install --values helm/prometheus/values.yaml prometheus prometheus-community/prometheus

local-alloy:
	kubectl -n revwallet-dev delete configmap alloy-config >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap alloy-config --from-file=helm/alloy/config.alloy

	helm repo update grafana
	helm -n revwallet-dev upgrade --install --values helm/alloy/values.yaml alloy grafana/alloy

local-loki:
	helm repo update grafana
	helm -n revwallet-dev upgrade --install --values helm/loki/values.yaml loki grafana/loki-stack

local-grafana:
	kubectl -n revwallet-dev wait --timeout=5m --for=condition=Ready pod -l app=loki
	kubectl -n revwallet-dev wait --timeout=5m --for=condition=Ready pod -l app=prometheus

	kubectl -n revwallet-dev delete configmap revwallet-dashboard >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap revwallet-dashboard --from-file=config/grafana/dashboard.json

	helm repo update grafana
	helm -n revwallet-dev upgrade --install --values helm/grafana/values.yaml grafana grafana/grafana

local-nginx:
	$(MAKE) stop-port-forward

	kubectl -n revwallet-dev wait --timeout=3m --for=condition=Ready pod -l app=revwallet-api
	kubectl -n revwallet-dev wait --timeout=3m --for=condition=Ready pod -l app=prometheus
	kubectl -n revwallet-dev wait --timeout=5m --for=condition=Ready pod -l app=grafana

	kubectl -n revwallet-dev delete configmap nginx-html >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap nginx-html --from-file=config/nginx/revwallet.html --from-file=config/nginx/404.html 

	kubectl -n revwallet-dev delete configmap nginx-conf >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap nginx-conf --from-file=helm/nginx/nginx.conf

	helm repo update bitnami
	helm -n revwallet-dev upgrade --install --values helm/nginx/values.yaml nginx bitnami/nginx

	$(MAKE) port-forward

local-delete:
	$(MAKE) stop-port-forward
	$(MAKE) delete-nginx 
	$(MAKE) delete-api
	$(MAKE) delete-db
	$(MAKE) delete-prometheus
	$(MAKE) delete-alloy
	$(MAKE) delete-loki
	$(MAKE) delete-grafana

local-delete-nginx:
	$(MAKE) stop-port-forward
	kubectl -n revwallet-dev delete configmap nginx-conf >/dev/null 2>&1 || true
	kubectl -n revwallet-dev delete configmap nginx-html >/dev/null 2>&1 || true
	helm -n revwallet-dev uninstall nginx

local-delete-alloy:
	helm -n revwallet-dev uninstall alloy
	kubectl -n revwallet-dev delete configmap alloy-config

local-delete-loki:
	helm -n revwallet-dev uninstall loki

local-delete-grafana:
	kubectl -n revwallet-dev delete configmap revwallet-dashboard >/dev/null 2>&1 || true
	helm -n revwallet-dev uninstall grafana

local-delete-prometheus:
	helm -n revwallet-dev uninstall prometheus

local-delete-api:
	helm -n revwallet-dev uninstall revwallet-api

local-delete-db:
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
	@echo "  make help                    - Display this help message."
	@echo "  make local-create            - Create a local k8s cluster with kind."
	@echo "  make local-deploy            - Deploy the API and all dependencies on k8s."
	@echo "  make local-db                - Deploy only the RevWallet database on k8s."
	@echo "  make local-prometheus        - Deploy only Prometheus on k8s."
	@echo "  make local-alloy             - Deploy only Alloy on k8s."
	@echo "  make local-loki              - Deploy only Loki on k8s."
	@echo "  make local-grafana           - Deploy only Grafana on k8s."
	@echo "  make local-api               - Deploy only the RevWallet API on k8s."
	@echo "  make local-nginx             - Deploy only Nginx on k8s."
	@echo "  make test                    - Run the tests."
	@echo "  make data                    - Generate sample data."
	@echo "  make compose-up              - Start RevWallet API and dependencies with Docker Compose."
	@echo "  make compose-down            - Stop RevWallet API and dependencies with Docker Compose."
	@echo "  make local-terminate         - Delete all the running pods and terminate the k8s cluster."
	@echo "  make port-forward            - Start port forwarding to Nginx."
	@echo "  make stop-port-forward       - Stop port forwarding to Nginx."
	@echo "  make setup-helm              - Install Helm repositories."
	@echo "  make local-delete            - Delete the RevWallet API and all dependencies on k8s."
	@echo "  make local-delete-db         - Delete only the RevWallet DB on k8s."
	@echo "  make local-delete-prometheus - Delete only Prometheus on k8s."
	@echo "  make local-delete-alloy      - Delete only Alloy on k8s."
	@echo "  make local-delete-loki       - Delete only Loki on k8s."
	@echo "  make local-delete-grafana    - Delete only Grafana on k8s."
	@echo "  make local-delete-api        - Delete only the RevWallet API on k8s."
	@echo "  make local-delete-nginx      - Delete only Nginx deployment on k8s."
