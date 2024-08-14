# RevWallet in Docker Compose
Wallet API where users can deposit, withdraw, and check the balance of a wallet. You can run RevWallet using Docker Compose.

## Requirements
RevWallet is a [Flask](https://flask.palletsprojects.com/en/3.0.x/) application that runs on Docker. To get started, ensure you have the following dependencies installed on your system:
- [Docker](https://docs.docker.com/guides/getting-started/)
- [Docker Compose](https://docs.docker.com/compose/gettingstarted/)
- [Python 3.11](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)

If you use `brew`, you can install the necessary dependencies by running:
```
brew install docker
brew install docker-compose
brew install python@3.11
brew install pipenv
```

## Running RevWallet with Docker Compose
To run RevWallet locally using Docker Compose, follow these steps:

1. Start by activating the virtual environment and installing the dependencies:
```
pipenv shell
pipenv install -e .
```
2. Build the Docker images and run the containers:
```
docker compose up --build -d  # this will build the images and run the containers
```

Docker Compose will bring up all the services. Once the containers are up and running, you can interact with the API as follows:

- Fetch existing wallets
```
curl -L -X GET http://revwallet.com/wallet/
```
Example of response: 
```
[] or [{"balance":999.0,"currency":"EUR","id":"1","owner":"test2"}]
```

- Create a new wallet
```
curl -L -X POST http://revwallet.com/wallet/ -d '{"owner": "test2", "initial_balance": "999.00", "currency": "EUR"}' -H "Content-Type: application/json"
```
Example of response: 
```
{"balance":999.0,"currency":"EUR","id":"1","owner":"test2"}
```

- Check current balance
```
curl -L -X GET http://revwallet.com/wallet/balance/1
```
Example of response: 
```
{"balance":999.0,"currency":"EUR","id":"1","owner":"test2"}
```

### Checking the logs
To see the logs of the app, run:
```
docker compose logs revwallet-api
```

### Shutting Down
To shut everything down, run:
```
docker compose down -v
```

## Running Tests
RevWallet has both unit and end-to-end tests. First, activate the virtual environment and sync dependencies:
```
pipenv shell
pipenv sync --dev
```


Then, run the tests:
```
pipenv run pytest
```
