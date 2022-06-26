FROM python:3.10.4

#обновить образ
RUN apt-get update -y
RUN apt-get upgrade -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/cpu_loadind

COPY ./requirements.txt /usr/srs/requirements.txt
RUN pip install -r /usr/srs/requirements.txt

COPY . /usr/src/cpu_loadind


# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]