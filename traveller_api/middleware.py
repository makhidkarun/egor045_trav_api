'''middleware.py'''

import time
import falcon
from prometheus_client import Counter, Histogram
from prometheus_client import multiprocess, CollectorRegistry
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter(
    'request_count',
    'App Request Count',
    ['app_name', 'method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'request_latency_seconds',
    'Request latency',
    ['app_name', 'endpoint']
)


class PrometheusMetrics(object):
    '''Prometheus metrics middleware'''

    @staticmethod
    def start_timer(request):
        '''Start request timer'''
        request.start_time = time.time()

    @staticmethod
    def stop_timer(request, response):
        '''Stop request timer'''
        resp_time = time.time() - request.start_time
        REQUEST_LATENCY.labels(
            'egor045_trav_api', request.path).observe(resp_time)
        return response

    @staticmethod
    def record_request_data(request, response):
        '''Record request/response data'''
        REQUEST_COUNT.labels(
            'egor045_trav_api',
            request.method,
            request.path,
            response.status_code).inc()
        return response

    def process_request(self, req, resp):
        '''Pre-routing request processing'''
        self.start_timer(req)

    def process_resource(self, req, resp, resource, params):
        '''Post-routing request processing'''
        pass

    def process_response(self, req, resp, resource, req_succeeded):
        '''Post-routing response processing'''
        self.record_request_data(req, resp)
        self.stop_timer(req, resp)


class Metrics(object):
    '''Report Prometheus metrics'''

    @staticmethod
    def on_get(req, resp):
        '''GET /metrics/'''
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        data = generate_latest(registry)

        resp.body = data
        resp.content_type = CONTENT_TYPE_LATEST
        resp.status = falcon.HTTP_200
