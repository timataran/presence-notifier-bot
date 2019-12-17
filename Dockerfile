FROM python:3.8

COPY ./requirements.txt /
RUN mkdir /code && pip install -r /requirements.txt

WORKDIR /code
COPY ./notifier-bot /code/

CMD ["python", "notifier.py"]