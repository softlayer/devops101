from flask import Flask, Blueprint, current_app, request, render_template
from flask_restful import Api, Resource, url_for
from urllib import quote_plus as quote_plus
from pprint import pprint as pp
from elasticsearch.exceptions import NotFoundError
search = Blueprint('search', __name__)


@search.route('/search', methods=['POST', 'GET'])
@search.route('/search/<int:page>', methods=['GET'])
@search.route('/search/<string:query>', methods=['GET'])
@search.route('/search/<string:query>/<int:page>', methods=['GET'])
@search.route('/search/<string:query>/<string:tags>/<int:page>', methods=['GET'])
def index(query=None, queryFields=["name","tags","short_desc","description", "custom.*"], page=0):

    if request.method == 'POST':
        query = request.form['query']

    es = current_app.config.get("es")
    q = {
        "_source": {
            "includes": ["name","tags","short_desc","description", "custom.*", "extra_stuff.*", "plans.entity"],
            "excludes": ['extra_stuff.i18n']
        }
    }

    if query is not None:
        q["query"] = { 
            "multi_match":{
                "fields":queryFields,
                "query":query,
                "fuzziness":"AUTO"
            }
        }

        base_link = "/search/%s" % quote_plus(query)

    else:
        base_link = "/search" 

    try:
        res = es.search(index="products",body=q,size=24, from_=(page *24))


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
    except NotFoundError:
        return render_template('product/generate.html')
