FROM python:3.10.14-alpine
WORKDIR /app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=config.settings

RUN apk update
RUN apk add postgresql-dev mariadb-dev gcc python3-dev mysql-client mysql-dev musl-dev zlib-dev jpeg-dev  #--(5.2)
#프로젝트 파일을 작업 디렉토리로 복사
COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=config.settings

EXPOSE 8000

#Django runserver command
CMD ["python", "manage.py", "runserver",  "0.0.0.0:8000"]