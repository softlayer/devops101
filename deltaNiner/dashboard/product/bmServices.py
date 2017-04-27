import elasticsearch
import logging
import sys
import requests

import certifi

from pprint import pprint as pp
import json
import flask
import time
from datetime import datetime

class bmServices():

    def __init__(self, app, passcode=None):
        # pp(app.config)
        self.username = app.config['BM_USER']
        self.password = app.config['BM_PASSWORD']


        es_config = [app.config['ELASTICSEARCH_HOST']]
        self.es = elasticsearch.Elasticsearch(
            es_config,
            use_ssl=True,
            verify_certs=app.config['VERIFY_SSL'],
            timeout=60,
            retry_on_timeout=True,
            max_retries=3
        )
        # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        # es_log = logging.getLogger("elasticsearch")
        # es_log.setLevel(logging.DEBUG)
        # eslog = logging.getLogger("elasticsearch.trace")
        # eslog.setLevel(logging.DEBUG)
        self.base_url = app.config['BM_API_URL']
        self.login_url = app.config['BM_LOGIN_URL']
        self.bearerToken = self.getBearerToken(passcode)

    def getBearerToken(self, passcode=None):
        headers = {
            'Accept': 'application/json',
            'Content-Type' : 'application/x-www-form-urlencoded'
        }
        if passcode is None:
            payload = {
                'response_type': 'token',
                'grant_type': 'password',
                'password': self.password,
                'scope' : None,
                'username': self.username
            }
        else:
            # Get one at https://login.ng.bluemix.net/UAALoginServerWAR/passcode
            payload = {
                'response_type': 'token',
                'grant_type': 'password',
                'passcode': passcode
            }
        # auth= "cf: " is required, for some reason...
        pp(payload)
        response = requests.post(self.login_url, data=payload, headers=headers, auth=('cf',''))
        pp(response.text)
        if response.status_code != 200:
            raise Exception("Auth Error")
        r = response.json()
        return r['access_token']

    def getBMServices(self):
        next_url = "/v2/services"
        while next_url is not None:
            response = requests.get("%s%s" % (self.base_url,next_url))
            if response.status_code != 200:
                yield("ERROR")
            services = response.json()
            print("Total Services %s\n" % services['total_results'])
            for service in services['resources']:
                yield("%s\n" % service['entity']['description'])
                to_put = self.formatService(service)
                self.putBmService(to_put)

            next_url = services['next_url']
            print("NEXT: %s\n" % next_url )

    def getServicePlans(self, service_url):
        headers = {
            'Authorization': "bearer %s" % self.bearerToken
        }
        response = requests.get("%s%s" % (self.base_url,service_url), headers=headers)
        r = response.json()

        return r['resources']

    def formatService(self, service):
        print("%s" % service['entity']['description'])
        # pp(service)
        # print("======########=======\n")
        plans = self.getServicePlans(service['entity']['service_plans_url'])
        if service['metadata']['updated_at'] is None:
            service['metadata']['updated_at'] = service['metadata']['created_at']
        to_put = {
            'name' : service['entity']['label'],
            'short_desc': service['entity']['description'],
            'tags': service['entity']['tags'],
            'service_plans_url': service['entity']['service_plans_url'],
            'extra_stuff' : json.loads(service['entity']['extra']),
            'plans' : plans,
            'entity': service['entity'],
            'metadata': service['metadata']
        }
        # pp(to_put)
        return to_put

    def putBmService(self,service):
        # print("putBmService")
        # print("=============\n")
        # print("%s" % json.dumps(service))
        # print("=============\n")
        try:
            self.es.index(
                index="products",
                doc_type='bluemix',
                id=service['entity']['unique_id'],
                body=service,
                version=1,
                version_type='external',
                timestamp=service['metadata']['updated_at']
            )
            # Sleeping to let the ES server do the indexing and not get overloaded
            time.sleep(1)
        except elasticsearch.exceptions.ConnectionTimeout:
            print("Timed out adding %s, sleeping for 5s" % service['name'])
            time.sleep(5)
            pass
        except elasticsearch.exceptions.ConflictError as e:
#            pp(e)
#            print("Document CONFLICT")
            self.resolveConflict(service)

    def resolveConflict(self, service):
        print("\tResolving conflict for %s" % service['entity']['unique_id'])
        old_product = self.es.get(index="products", id=service['entity']['unique_id'])
        es_date = datetime.strptime(old_product['_source']['metadata']['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
        bmx_date  = datetime.strptime(service['metadata']['updated_at'], "%Y-%m-%dT%H:%M:%SZ")
        diff = es_date - bmx_date
        print("\tES_DATE: %s | %s bmx_date" % (es_date,bmx_date))
        if(diff.total_seconds() >= 0):
            print("\tES is newer, discarding update")
        else:
            print("\tBMX is newer, merging custom fields and updating")
            if 'custom' not in old_product['_source']:
                old_product['_source']['custom'] = {}

            service['custom'] = old_product['_source']['custom']
            self.es.index(
                index="products",
                doc_type='bluemix',
                id=service['entity']['unique_id'],
                body=service,
                version= int(old_product['_version']) + 1,
                version_type='external',
                timestamp=service['metadata']['updated_at']
            )



if __name__ == "__main__":
    main = bmServices()
    main.getBMServices()
    # main.getServicePlans('/v2/services/2197e136-a2c6-4758-a084-27dd5540103e/service_plans')
