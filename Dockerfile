FROM jfloff/alpine-python:2.7

ADD . /

RUN pip install -r requirements.txt

CMD python bot.py
