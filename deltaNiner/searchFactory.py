import elasticsearch
import logging
import sys
import certifi


class searchFactory():
    def __init__(self, app):

        es_config = [app.config['ELASTICSEARCH_HOST']]
        self.es = elasticsearch.Elasticsearch(es_config,
            use_ssl=True,
            verify_certs=app.config['VERIFY_SSL'],
            timeout=60,
            retry_on_timeout=True,
            max_retries=3)

    def setLogging(self):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        es_log = logging.getLogger("elasticsearch")
        es_log.setLevel(logging.DEBUG)
        eslog = logging.getLogger("elasticsearch.trace")
        eslog.setLevel(logging.DEBUG)