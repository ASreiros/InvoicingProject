FROM python:3.11.4-slim-bullseye
# sukelia iš source į docker/app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT gunicorn run:app