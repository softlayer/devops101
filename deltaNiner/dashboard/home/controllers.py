from flask import Blueprint, request, render_template, \
                  url_for, session, redirect, current_app

from pprint import pprint as pp
import json

home = Blueprint('home', __name__,template_folder='templates')

@home.route('/')
def index():
    return render_template('home/index.html', )
