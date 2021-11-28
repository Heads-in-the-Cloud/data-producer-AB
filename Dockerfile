FROM austinbaugh/utopia-data-producer-base:0.0.3-SNAPSHOT

WORKDIR /app

EXPOSE 5000

COPY app/ .

ENTRYPOINT python app
