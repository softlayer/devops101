from flask import current_app, Blueprint, request, render_template, \
                  url_for, session, redirect, abort, Response

import elasticsearch
from pprint import pprint as pp
product = Blueprint('product', __name__,
        template_folder='templates')

from pprint import pprint as pp


import logging
import sys
import json
import bmServices 
import time

@product.route('/product/')
@product.route('/product/<product_id>', methods=['GET'])
def index(product_id=None):
    es = current_app.config.get("es")
    try:
        res = es.get(index="products", id=product_id)
        if 'custom' not in res['_source']:
            res['_source']['custom'] = {'my_tags' : [''], 'my_notes': '', 'my_competition': ''}
        # pp(res)
    except elasticsearch.exceptions.NotFoundError:
        abort(404)
    return render_template('product/index.html', res=res)



@product.route('/product/<product_id>/custom_tags', methods=['POST'])
def postTags(product_id=None):
    tags = json.loads(request.form.get('data'))
    service = json.loads(request.form.get('service'))
    source = service['_source']

    if 'my_tags' not in source['custom']:
        source['custom']['my_tags'] = ['']

    for tag in tags:
        source['custom']['my_tags'].append(tag['value'])

    es = current_app.config.get("es")
    try:
        es.index(
                index = "products",
                doc_type = 'bluemix',
                id = product_id,
                body = source,
                version = int(service['_version']) + 1,
                version_type='external'
            )
    except elasticsearch.exceptions.NotFoundError:
        abort(404)
    return ('', 204)


@product.route('/product/<product_id>/custom_notes', methods=['POST'])
def postNotes(product_id=None):
    notes = json.loads(request.form.get('data'))
    service = json.loads(request.form.get('service'))
    source = service['_source']


    source['custom']['my_notes'] = notes

    es = current_app.config.get("es")
    try:
        es.index(
                index = "products",
                doc_type = 'bluemix',
                id = product_id,
                body = source,
                version = int(service['_version']) + 1,
                version_type='external'
            )
    except elasticsearch.exceptions.NotFoundError:
        abort(404)
    return ('', 204)

@product.route('/product/generate', methods=['POST'])
def generate():
    sso_code = request.form.get('data')
    print('Hello World! %s' % sso_code)
    main = bmServices.bmServices(current_app,sso_code)
    return Response(main.getBMServices(), mimetype='text/html')
