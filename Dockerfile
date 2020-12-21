FROM python:3.7-alpine

COPY .env ./
COPY bots/__init__.py /bots/
COPY bots/twitter_auth.py /bots/
COPY bots/tweet_listener.py /bots/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "tweet_listener.py"]
