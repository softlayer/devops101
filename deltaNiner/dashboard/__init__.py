from flask import Flask, render_template, url_for
import searchFactory as  searchFactory
import json
from json2html import *
from pprint import pprint as pp

app = Flask(__name__)


app.config.from_object('config')
app.config['TEMPLATES_AUTO_RELOAD'] = True

es = searchFactory.searchFactory(app)

if app.config['DEBUG']:
    es.setLogging()

app.config['es'] = es.es

@app.route('/sitefaq')
def sitefaq():
    return render_template('site.html')

@app.route('/esfaq')
def esfaq():
    return render_template('es.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from .search.controllers import search as search
from .home.controllers import home as home
from .product.controllers import product as product
from .tags.controllers import tags as tags

app.register_blueprint(home)
app.register_blueprint(search)
app.register_blueprint(product)
app.register_blueprint(tags)


@app.template_filter('jsonify')
def jsonify(string):
    try:
        return json.loads(string)
    except ValueError:
        return ''



@app.template_filter('htmlify')
def htmlify(string):
    if isinstance(string, list):
        string = {'data': string}

    if isinstance(string, basestring):
        return string

    try:
        output = json2html.convert(json = string)
    except Exception as e:
        try:
            test = json.loads(string)
            output = json2html.convert(json = test)
        except Exception as e:
            output = string

    return output
