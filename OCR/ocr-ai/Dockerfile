FROM python:3.10.4
ENV PYTHONUNBUFFERED 1

WORKDIR /setup
RUN apt-get update && \
    apt-get install -y libglu1-mesa-dev poppler-utils && \
    pip install django python-dotenv paddlepaddle==2.4.2 paddleocr pdf2image mysqlclient django-cors-headers requests

COPY . .
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000