FROM python:3.12-slim

WORKDIR /revwallet

COPY wallet wallet
COPY app.py .
COPY Pipfile .
COPY Pipfile.lock .

RUN apt-get update && \
  apt-get install -y gcc libpq-dev

RUN python -m pip install pipenv && \
  python -m pipenv install --system --deploy --ignore-pipfile

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]