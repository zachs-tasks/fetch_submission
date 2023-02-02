FROM python:3
WORKDIR /usr/src/app

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install vim -y

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "./fetch/fetch.py", "-i", "10"]
