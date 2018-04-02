FROM alpine:3.5

# Base install
RUN apk update && apk add --no-cache \
#    bash \
    python \
    py-pip

# Setup falcon application
COPY traveller_api /traveller_api
COPY requirements.txt star.sqlite traveller_rest_api.ini docker/gunicorn.conf docker/logging.conf /
RUN pip install -r /requirements.txt

# Set up Prometheus multiprocess registry
RUN mkdir -p /metrics

# Setup supervisord

# Start processes
WORKDIR /
EXPOSE 8000
ENTRYPOINT ["/usr/bin/gunicorn", "--config", "gunicorn.conf", "--log-config", "logging.conf", "--access-logfile", "-", "-w", "4", "traveller_api.app",  "--bind", "0.0.0.0:8000"]
