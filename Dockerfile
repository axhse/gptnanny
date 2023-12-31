FROM python:3.9.10-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

RUN export MANAGER_TOKEN=x && python manage.py migrate && unset MANAGER_TOKEN
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
