FROM python:3.8

RUN mkdir /code
WORKDIR /code
ADD ./notifier-bot /code/
RUN pip install -r /code/requirements.txt

CMD ["python", "notifier.py"]