from flask import current_app, Blueprint, request, render_template, \
                  url_for, session, redirect, abort


from pprint import pprint as pp
import logging
import sys
import json

tags = Blueprint('tags', __name__,template_folder='templates')

@tags.route('/tags')
def index():
    es = current_app.config.get("es")
    q = {"aggs":{"products-aggs":{"terms":{"field":"tags","size":50,"order":{"_count":"desc"}}}}}

    tags = es.search(index = "products", doc_type = "bluemix", body=q, size=0)
    hits = tags['aggregations']['products-aggs']['buckets']


    return (json.dumps(hits),200)

@tags.route('/tags/<query>')
def search(query, page=0):
    
    if request.method == 'POST':
        query = request.form['query']

    es = current_app.config.get("es")
    q = {
        "_source": {
            "includes": ["name","tags","short_desc","description", "custom.*", "extra_stuff.*"], 
            "excludes": ['extra_stuff.i18n']
        }
    }
    
    q["query"] = { 
        "multi_match":{
            "fields":["tags","custom.tags"],
            "query":query,
            "fuzziness":"AUTO"
        }
    }
    res = es.search('products', 'bluemix', body=q, size=24, from_=(page *24))
    base_link = "/tags/%s" % (query)


    total_res = len(res['hits']['hits'])
    res['total_res'] = total_res
    if total_res < 24:
        res['nextLink'] = None
        res['previousLink'] = None
    elif page != 0:
        res['nextLink'] = "%s/%s" % (base_link,page + 1 )
        res['previousLink'] = "%s/%s" % (base_link,page - 1 )
    else:
        res['nextLink'] = "%s/%s" % (base_link,page + 1)
        res['previousLink'] = None
    res['page'] = page

    return render_template('search/results.html', services=res, query=query)    