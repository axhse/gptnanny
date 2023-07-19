FROM python:3.9.10-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["sh", "-e", "entrypoint.sh"]
