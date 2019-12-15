FROM python:3.8

ADD ./requirements.txt /
RUN mkdir /code && pip install -r /requirements.txt

WORKDIR /code
ADD ./notifier-bot /code/

CMD ["python", "notifier.py"]