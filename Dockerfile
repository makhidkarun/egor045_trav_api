FROM alpine:3.7

# Base install
RUN apk update && apk add --no-cache \
#    bash \
    python3

# Setup falcon application
COPY traveller_api /traveller_api
COPY requirements.txt star.sqlite traveller_rest_api.ini docker/gunicorn.conf docker/logging.conf /
RUN pip3 install -r /requirements.txt

# Set up Prometheus multiprocess registry
RUN mkdir -p /metrics

<<<<<<< HEAD
# Setup supervisord

# Start processes
=======
>>>>>>> master
WORKDIR /
EXPOSE 8000
ENTRYPOINT ["/usr/bin/gunicorn", "--config", "gunicorn.conf", "--log-config", "logging.conf", "--access-logfile", "-", "-w", "4", "traveller_api.app",  "--bind", "0.0.0.0:8000"]
