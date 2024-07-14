FROM python:3.11.9-alpine

WORKDIR /revwallet

COPY wallet wallet
COPY app.py .
COPY Pipfile .
COPY Pipfile.lock .

RUN python -m pip install pipenv

RUN python -m pipenv install --system --deploy --ignore-pipfile

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
