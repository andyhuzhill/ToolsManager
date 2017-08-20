#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-19 10:50:38
# @Author  : ${Your Name} (${you@example.org})
# @Link    : 
# @Version : ${1.0.0}

import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from flask import request, render_template, redirect, url_for

from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'), 200

@app.route('/t/', methods=['GET'])
def query_tools():
    qrcode = request.args.get('qr', None)
    return "<h1> qr = {0} </h1>".format(qrcode)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/dashboard/add_user', methods=['GET'])
def add_user_display():
    return render_template('add_user.html'), 200


@app.route('/dashboard/add_user', methods=['POST'])
def handle_add_user():
    return redirect(url_for('index')), 200


if __name__ == "__main__":
    app.run()
