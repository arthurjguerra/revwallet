# revwallet
Simple Web application to practice infrastructure as code, CI/CD, immutable infrastructure, and software development. This application is a basic wallet where a user can add and withdrawal money.

## TODO
- [X] Implement unit tests to validate three operations in a wallet: check current wallet balance, add money to a wallet and withdrawal money from a wallet.
- [X] Implement the wallet API that accepts the three operations above (without persisting anything).
- [X] Add unit tests to CICD.
- [X] Create a simple web app in Flask that can interact with the wallet API to show the current balance in the wallet, add money to it, and withdrawal money from the wallet.
- [X] Create a database that will be used to persist all three operations supported by the wallet API.
- [ ] Have the DB + the app running locally using Docker.
- [ ] Implement integration tests to check if all operations work from end to end.
- [ ] Add all tests to CICD
- [ ] Implement code to spin up the minimal infrastructure required to run this in AWS: networking, DB, container orchestrator.
- [ ] Implement nice error page

## How to run the tests?
```
pipenv shell
pipenv sync --dev
pipenv run pytest
```

## How to run it locally?
```
pipenv shell
pipenv install -e .
flask --app wallet run --debug  # run flask in debug mode
```

Access the app at http://127.0.0.1:5000/

## How to run it?
TBD.

## Next steps
TBD.