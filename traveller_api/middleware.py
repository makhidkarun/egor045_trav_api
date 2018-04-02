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
API_PATHS = [
    '/misc/angdia',
    '/ct/lbb6/star',
    '/mt/wbh/star',
    '/t5/cargogen',
    '/ct/lbb2/cargogen/purchase',
    '/ct/lbb2/cargogen/sale',
    '/t5/orbit',
    '/misc/starcolor',
    '/metrics',
    '/ping'
]

class PrometheusMetrics(object):
    '''Prometheus metrics middleware'''

    @staticmethod
    def start_timer(request):
        '''Start request timer'''
        request.start_time = time.time()

    def stop_timer(self, request, response):
        '''Stop request timer'''
        metric_path = self.trim_path(request.path)
        resp_time = time.time() - request.start_time
        if metric_path:
            REQUEST_LATENCY.labels(
                'egor045_trav_api', metric_path).observe(resp_time)
        return response

    def record_request_data(self, request, response):
        '''Record request/response data'''
        metric_path = self.trim_path(request.path)
        resp_time = time.time() - request.start_time
        status = response.status.split(' ')[0]
        if metric_path:
            REQUEST_COUNT.labels(
                'egor045_trav_api',
                request.method,
                metric_path,
                status).inc()
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

    @staticmethod
    def trim_path(path):
        '''Trim request path to remove variable elements'''
        for api_path in API_PATHS:
            if path.startswith(api_path):
                return api_path

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
