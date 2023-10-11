FROM python:3.11

ENV TZ=Asia/Taipei

WORKDIR /backend

COPY requirements.txt /backend

RUN set -ex \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

RUN apt update -y && apt install ffmpeg -y

CMD python code/app.py