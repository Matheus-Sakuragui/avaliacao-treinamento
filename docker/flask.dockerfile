FROM python:3.12.1

EXPOSE 5000

RUN apt-get update && apt-get install -y build-essential

RUN mkdir -p -m 777 /flaskr
WORKDIR /flaskr

COPY ./flaskr/. /flaskr
COPY ./requirements.txt /flaskr

RUN chmod -R 777 ./


EXPOSE 5000

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

CMD ["python", "-m", "flask", "run"]