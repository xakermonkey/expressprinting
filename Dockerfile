FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/expressprinting

COPY requirements.txt requirements.txt

RUN set -ex && \
    apt-get update && apt-get -y install nano gcc libcups2-dev libreoffice-writer libreoffice-gnome default-jre libreoffice-java-common &&\
    pip install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod ugo+x script.sh

RUN useradd -ms /bin/bash fduser && \
    chown -R fduser /opt/expressprinting
USER fduser

EXPOSE 8000
EXPOSE 631


CMD ["./script.sh"]
