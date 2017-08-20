#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-19 10:50:38
# @Author  : ${Your Name} (${you@example.org})
# @Link    : 
# @Version : ${1.0.0}

from flask import Flask
from flask import request

import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/t/", methods=["GET"])
def query_tools():
    qrcode = request.args.get('qr', None)
    return "<h1> qr = {0} </h1>".format(qrcode)

if __name__ == "__main__":
    app.run()
