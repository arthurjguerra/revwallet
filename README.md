![Publish](https://github.com/arthurjguerra/revwallet/actions/workflows/chart-publish.yaml/badge.svg)
![Build](https://github.com/arthurjguerra/revwallet/actions/workflows/build.yaml/badge.svg)
[![Latest Release](https://img.shields.io/github/v/release/arthurjguerra/revwallet?include_prereleases)]([https://github.com/kubernetes/minikube/releases/latest](https://github.com/arthurjguerra/revwallet/releases/latest))

# RevWallet
RevWallet is a wallet API that allows users to deposit, withdraw, and check their balance. It serves as a practice project for infrastructure as code, CI/CD, immutable infrastructure, and Python software development.

## Architecture Overview
```mermaid
graph TD
  subgraph RevWallet Architecture
      loki[Loki]
      alloy[Alloy]
      grafana[Grafana]
      prometheus[Prometheus]
      revwallet-db[RevWallet DB]
      revwallet-api[RevWallet API]
      nginx[Nginx]
  end

  loki -.-> grafana
  alloy -.-> loki
  alloy -.-> revwallet-api
  prometheus -.-> grafana
  prometheus -.-> revwallet-api
  revwallet-api -.-> revwallet-db
  nginx --> revwallet-api
  nginx --> prometheus
  nginx --> grafana
  id1 -- /prometheus --> nginx
  id1 -- /grafana --> nginx
  id1[[localhost:8080]] -- /wallet --> nginx

  classDef public fill:#c2e59c,stroke:#000,stroke-width:2px;
  classDef private fill:#f3e59c,stroke:#000,stroke-width:2px;

  class loki private
  class alloy private
  class grafana public
  class prometheus public
  class revwallet-db private
  class revwallet-api public
  class nginx public
```
The RevWallet API is hosted behind an Nginx reverse proxy. Grafana and Prometheus are also routed through Nginx for unified access.

Only the RevWallet API, Grafana, and Prometheus are exposed externally. Internal services like Loki, Alloy, and the database remain accessible only within the internal network.

## Requirements
RevWallet is a [Flask](https://flask.palletsprojects.com/en/3.0.x/) application that runs on Docker. To get started, ensure you have the following dependencies installed on your system:
- [Docker](https://docs.docker.com/guides/getting-started/)
- [Docker Compose](https://docs.docker.com/compose/gettingstarted/)
- [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Kubectl](https://kubernetes.io/docs/reference/kubectl/)
- [Helm](https://helm.sh/docs/intro/quickstart/)
- [Python 3.11](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)

To install dependencies via `brew`:
```
brew install docker docker-compose kind helm python@3.11 pipenv
```

## Running RevWallet with Docker Compose
Start the API:
```
make compose-up
```
Then, access the API at http://localhost:8080

To shut everything down, run:
```
make compose-down
```

For more details, refer to the [Docker Compose documentation](docs/docker-compose.md).

## Running RevWallet on Kubernetes (locally)
Deploy RevWallet to Kubernetes locally:

```
make create deploy
```

Access RevWallet at http://localhost:8080/

To shut everything down, run:
```
make terminate
```

For more details, refer to the [Kubernetes documentation](docs/k8s-kind.md).

## Generating Random Data
To populate the API with sample data, run:

```
make data
```

This command will:
- Create some wallets.
- Check the balance of these wallets.
- Fetch all wallets from the API.

## Observability

### Metrics
RevWallet utilizes the `prometheus-flask-exporter` package to expose basic metrics, including:

- `flask_http_request_duration_seconds`: Duration of Flask HTTP requests in seconds.
- `flask_http_request_total`: Total number of HTTP requests made to Flask.
- `flask_http_request_exceptions_total`: Total number of uncaught exceptions when serving Flask requests.

For more information, refer to the [Prometheus Flask Exporter repository](https://github.com/rycus86/prometheus_flask_exporter).

### Dashboard
RevWallet includes a basic dashboard accessible in Grafana:
![revwallet-dashboard](./docs/img/revwallet-dashboard.png)

## CICD
When a new tag is created, a new version of the RevWallet API chart is released via Github Actions. The Charts are hosted on Github Pages and are publicly available at [ArtifactHub](https://artifacthub.io/packages/helm/revwallet/revwallet-api).

```mermaid
flowchart TD
    start(((start))) --> CI
    CI{{CI}} --> |Compose| BuildAndDeployDockerCompose[Build & Deploy Services with Docker Compose]
    BuildAndDeployDockerCompose --> Tests
    CI --> |Changes in charts| DeployServicesHelm
    CI{{CI}} --> |K8s| BuildNewImage[Build New Image]
    BuildNewImage --> DeployServicesHelm[Deploy Services with Helm]
    DeployServicesHelm --> Tests
    Tests --> finish((end))


    start(((start))) -.-> CD{{CD}}
    CD -.-> NewChartVersion[New Version of Chart]
    NewChartVersion -.-> |CD| Tests
    Tests -.-> |CD| PublishNewChart[Publish New Chart Version]
    CD -.-> |New Tag| BuildNewImageVersion[Build and Publish New Image Version]
    BuildNewImageVersion -.-> UpdateHelmValues[Update Helm Chart with New Image Version]
```

