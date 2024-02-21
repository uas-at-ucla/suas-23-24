import logging
from gunicorn import glogging


class CustomGunicornLogger(glogging.Logger):

    def setup(self, cfg):
        super().setup(cfg)

        # Add filters to Gunicorn logger
        logger = logging.getLogger("gunicorn.access")
        logger.addFilter(PrometheusMetricsFilter())


class PrometheusMetricsFilter(logging.Filter):
    def filter(self, record):
        return record.args['U'] not in ['/metrics', '/favicon.ico']


accesslog = '-'
logger_class = CustomGunicornLogger
