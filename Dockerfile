FROM python:3.10.12-slim-buster

WORKDIR /app
RUN apt-get update
RUN apt-get install gcc -y

# Install deps
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD python3 -u bot.py