FROM python:3.10.0-alpine
USER root
WORKDIR /charity
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000