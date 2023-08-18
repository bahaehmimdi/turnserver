FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y coturn

COPY turnserver.conf /etc/turnserver.conf

EXPOSE 3478 5349

CMD ["turnserver", "-c", "/etc/turnserver.conf"]
