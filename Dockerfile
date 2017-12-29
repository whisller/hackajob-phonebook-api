FROM python:3-stretch

COPY requirements.txt /var/tmp/

RUN pip install -r /var/tmp/requirements.txt && rm /var/tmp/requirements.txt

WORKDIR /app

ADD . /app

EXPOSE 8000

CMD python setup.py install && api
