#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-19 10:50:38
# @Author  : ${Your Name} (${you@example.org})
# @Link    : 
# @Version : ${1.0.0}

from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/t/", methods=["GET"])
def query_tools():
    qrcode = request.args.get('qr', None)
    return "<h1> qr = {0} </h1>".format(qrcode)

if __name__ == "__main__":
    app.run()
