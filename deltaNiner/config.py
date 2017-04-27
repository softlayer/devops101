DEBUG = False

import os
import json
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

THREADS_PER_PAGE = 2

SECRET_KEY = 'muchdev'

#RyanT
default_host = "https://admin:PASSWORD@bluemix-sandbox-dal-9-portal6.dblayer.com:25513/"
vcap_services = os.getenv('VCAP_SERVICES')

if vcap_services is not None:
    ELASTICSEARCH_HOST = json.loads(vcap_services)['compose-for-elasticsearch'][0]['credentials']['uri']
    VERIFY_SSL = True
else:
    ELASTICSEARCH_HOST = default_host
    VERIFY_SSL = True


BM_USER = os.getenv('BM_USER')
BM_PASSWORD = os.getenv('BM_PASSWORD')
BM_API_URL = 'https://api.ng.bluemix.net'
BM_LOGIN_URL = 'https://login.ng.bluemix.net/UAALoginServerWAR/oauth/token'
