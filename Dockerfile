FROM alpine:3.5

# Base install
RUN apk update && apk add --no-cache \
#    bash \
    python \
    py-pip

# Setup falcon application
# RUN mkdir -p /deploy/
COPY traveller_api /traveller_api
COPY requirements.txt star.sqlite traveller_rest_api.ini docker/gunicorn.conf docker/logging.conf /
RUN pip install -r /requirements.txt

# Set up Prometheus multiprocess registry
RUN mkdir -p /metrics

# Setup supervisord
# RUN mkdir -p /var/log/supervisor
# COPY docker/supervisord.conf /etc/supervisord.conf

# Start processes
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

WORKDIR /
EXPOSE 8000
ENTRYPOINT ["/usr/bin/gunicorn", "--config", "gunicorn.conf", "--log-config", "logging.conf", "--access-logfile", "-", "-w", "4", "traveller_api.app",  "--bind", "0.0.0.0:8000"]
