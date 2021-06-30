FROM python:3.7-alpine

LABEL maintainer="Yap Jheng Khin polarbearyap2@gmail.com"

WORKDIR /app

ENV FLASK_APP=runserver.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add bash icu-libs krb5-libs libgcc libintl libssl1.1 libstdc++ zlib
RUN apk add libgdiplus --repository https://dl-3.alpinelinux.org/alpine/edge/testing/

COPY requirements.txt requirements.txt

RUN pip install pip --upgrade
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["flask", "run"]