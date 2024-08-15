# Makefile to build and deploy RevWallet in K8s and Docker Compose

.PHONY: \
	deploy-nginx \
	deploy-api \
	deploy-db \
	deploy-prometheus \
	deploy-alloy \
	deploy-loki \
	deploy-grafana \
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
	setup \
	setup-helm \
	shutdown \
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

setup:
	kind create cluster --name revwallet
	kubectl create namespace revwallet-dev
	kubectl config set-context kind-revwallet --namespace=revwallet-dev
	$(MAKE) setup-helm

setup-helm:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo update

shutdown:
	kind delete cluster --name revwallet

deploy: 
	$(MAKE) deploy-db
	$(MAKE) deploy-alloy
	$(MAKE) deploy-loki
	$(MAKE) deploy-prometheus
	$(MAKE) deploy-grafana
	$(MAKE) deploy-api
	$(MAKE) deploy-nginx

deploy-db:
	kubectl apply -f k8s/revwallet-db

deploy-alloy:
	kubectl -n revwallet-dev create configmap alloy-config --from-file=config/alloy/config.alloy
	helm -n revwallet-dev upgrade --install --values k8s/alloy/values.yaml alloy grafana/alloy

deploy-loki:
	helm -n revwallet-dev upgrade --install --values k8s/loki/values.yaml loki grafana/loki-stack

deploy-prometheus:
	helm -n revwallet-dev upgrade --install --values k8s/prometheus/values.yaml prometheus prometheus-community/prometheus

deploy-grafana:
	kubectl -n revwallet-dev create configmap revwallet-dashboard --from-file=config/grafana/dashboard.json
	helm -n revwallet-dev upgrade --install --values k8s/grafana/values.yaml grafana grafana/grafana

deploy-api:
	helm -n revwallet-dev upgrade --install --values k8s/revwallet-api-chart/values.yaml revwallet-api k8s/revwallet-api-chart

deploy-nginx:
	kubectl -n revwallet-dev create configmap nginx-html --from-file=config/nginx/revwallet.html --from-file=config/nginx/404.html 
	kubectl -n revwallet-dev create configmap nginx-conf --from-file=config/nginx/nginx.conf
	kubectl -n revwallet-dev create configmap nginx-htpasswd --from-file=config/nginx/.htpasswd
	helm -n revwallet-dev upgrade --install --values k8s/nginx/values.yaml nginx bitnami/nginx

delete:
	$(MAKE) delete-nginx 
	$(MAKE) delete-api
	$(MAKE) delete-db
	$(MAKE) delete-prometheus
	$(MAKE) delete-alloy
	$(MAKE) delete-loki
	$(MAKE) delete-grafana

delete-nginx:
	helm -n revwallet-dev uninstall bitnami
	kubectl -n revwallet-dev delete configmap nginx-conf
	kubectl -n revwallet-dev delete configmap nginx-html
	kubectl -n revwallet-dev delete configmap nginx-htpasswd

delete-alloy:
	helm -n revwallet-dev uninstall alloy

delete-loki:
	helm -n revwallet-dev uninstall loki

delete-grafana:
	helm -n revwallet-dev uninstall grafana
	kubectl -n revwallet-dev delete configmap revwallet-dashboard

delete-prometheus:
	helm -n revwallet-dev uninstall prometheus

delete-api:
	helm -n revwallet-dev uninstall revwallet-api

delete-db:
	kubectl -n revwallet-dev delete -f k8s/revwallet-db
