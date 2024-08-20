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
	helm repo update

terminate:
	$(MAKE) delete
	helm repo remove bitnami grafana prometheus-community
	kind delete cluster --name revwallet

deploy: 
	$(MAKE) db
	$(MAKE) alloy
	$(MAKE) loki
	$(MAKE) prometheus
	$(MAKE) grafana
	$(MAKE) api
	$(MAKE) nginx
	$(MAKE) port-forward

db:
	kubectl apply -f k8s/revwallet-db

alloy:
	kubectl -n revwallet-dev delete configmap alloy-config >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap alloy-config --from-file=k8s/alloy/config.alloy

	helm repo update grafana
	helm -n revwallet-dev upgrade --install --values k8s/alloy/values.yaml alloy grafana/alloy

loki:
	helm repo update grafana
	helm -n revwallet-dev upgrade --install --values k8s/loki/values.yaml loki grafana/loki-stack

prometheus:
	helm repo update prometheus-community
	helm -n revwallet-dev upgrade --install --values k8s/prometheus/values.yaml prometheus prometheus-community/prometheus

grafana:
	kubectl -n revwallet-dev delete configmap revwallet-dashboard >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap revwallet-dashboard --from-file=config/grafana/dashboard.json

	helm repo update grafana
	helm -n revwallet-dev upgrade --install --values k8s/grafana/values.yaml grafana grafana/grafana

api:
	helm repo update
	helm -n revwallet-dev upgrade --install --values k8s/revwallet-api-chart/values.yaml revwallet-api k8s/revwallet-api-chart

nginx:
	kubectl -n revwallet-dev delete configmap nginx-html >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap nginx-html --from-file=config/nginx/revwallet.html --from-file=config/nginx/404.html 

	kubectl -n revwallet-dev delete configmap nginx-conf >/dev/null 2>&1 || true
	kubectl -n revwallet-dev create configmap nginx-conf --from-file=k8s/nginx/nginx.conf

	helm repo update bitnami
	helm -n revwallet-dev upgrade --install --values k8s/nginx/values.yaml nginx bitnami/nginx

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
	kubectl -n revwallet-dev delete configmap nginx-conf
	kubectl -n revwallet-dev delete configmap nginx-html
	helm -n revwallet-dev uninstall nginx

delete-alloy:
	helm -n revwallet-dev uninstall alloy
	kubectl -n revwallet-dev delete configmap alloy-config

delete-loki:
	helm -n revwallet-dev uninstall loki

delete-grafana:
	kubectl -n revwallet-dev delete configmap revwallet-dashboard
	helm -n revwallet-dev uninstall grafana

delete-prometheus:
	helm -n revwallet-dev uninstall prometheus

delete-api:
	helm -n revwallet-dev uninstall revwallet-api

delete-db:
	kubectl -n revwallet-dev delete -f k8s/revwallet-db

################################## Utils Targets #############################
port-forward:
	bash scripts/port-forward

stop-port-forward:
	bash scripts/port-forward --stop

data:
	bash scripts/generate-data