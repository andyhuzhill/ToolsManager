#!/usr/bin/env python3~
# -*- coding: utf-8 -*-
# @Date    : 2017-08-19 10:50:38
# @Author  : ${Your Name} (${you@example.org})
# @Link    :
# @Version : ${1.0.0}

import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from flask import request, session, render_template, redirect, url_for, flash

from flask_bootstrap import Bootstrap

import db
from forms import AddUserForm


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
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

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/dashboard/add_user', methods=['GET', 'POST'])
def add_user_display():
    add_user_form = AddUserForm()
    if add_user_form.validate_on_submit():
        user_id = add_user_form.user_id.data
        password = add_user_form.password.data
        user_name = add_user_form.name.data
        sex = add_user_form.sex.data
        photo = add_user_form.photo.data
        duty = add_user_form.duty.data
        department = add_user_form.department.data
        telephone = add_user_form.telephone.data
        admin = add_user_form.admin.data
        remarks = add_user_form.remarks.data

        user, err = db.add_user(user_id, password, user_name, sex, photo.read(), duty, department, telephone, admin, remarks)

        if user is not None:
            flash("添加用户成功!")
            return redirect(url_for('index'))
        else:
            flash("添加用户失败!")

    return render_template('add_user.html', form=add_user_form), 200

 
@app.route('/dashboard/batch_add_user', methods=['GET'])
def batch_add_user_display():
    return render_template('batch_add_user.html'), 200


@app.route('/dashboard/add_user', methods=['POST'])
def handle_add_user():
    return redirect(url_for('index')), 200



if __name__ == "__main__":
    app.run()
