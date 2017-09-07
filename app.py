#!/usr/bin/env python3~
# -*- coding: utf-8 -*-
# @Date    : 2017-08-19 10:50:38
# @Author  : ${Your Name} (${you@example.org})
# @Link    :
# @Version : ${1.0.0}

import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from flask import request, session, render_template, redirect, url_for, flash, make_response

from flask_bootstrap import Bootstrap

import db
from forms import AddUserForm, AddToolsForm


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
    tool_id = request.args.get('qr', None)
    tool_info = db.query_tool_infos(tool_id)
    return render_template('tools_details.html', info=tool_info), 200


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/images/tools/<tool_id>', methods=['GET'])
def tool_image_handler(tool_id):
    tool_info = db.query_tool_infos(tool_id)
    if tool_info["found"]:
        response = make_response(tool_info["picture"])
        return response
    return ""

@app.route('/images/users/<user_id>', methods=['GET'])
def user_image_handler(user_id):
    user_info = db.query_user(user_id)
    if user_info['found']:
        response = make_response(user_info["user"].photo)
        return response
    return ""

@app.route('/dashboard/add_user', methods=['GET', 'POST'])
def add_user_handler():
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

        user = db.add_user(user_id, password, user_name, sex, photo.read(
        ), duty, department, telephone, admin, remarks)

        if user is not None:
            flash("添加用户成功!")
            return redirect(url_for('dashboard_handler'))
        else:
            flash("添加用户失败!")

    return render_template('add_user.html', form=add_user_form), 200


@app.route('/dashboard/batch_add_user', methods=['GET', 'POST'])
def batch_add_user_display():
    return render_template('batch_add_user.html'), 200


@app.route('/dashboard/user_list', methods=['GET', 'POST'])
def user_list_handler():
    user_infos = db.get_all_user_infos()
    return render_template('user_list.html', user_infos=user_infos), 200

@app.route('/dashboard/add_tools', methods=['GET', 'POST'])
def add_tool_handler():
    add_tools_form = AddToolsForm()
    if add_tools_form.validate_on_submit():
        tool_id = add_tools_form.tool_id.data
        name = add_tools_form.name.data
        model = add_tools_form.model.data
        picture = add_tools_form.picture.data
        position = add_tools_form.position.data
        category = add_tools_form.category.data
        status = add_tools_form.status.data
        need_check = add_tools_form.need_check.data
        last_check_date = add_tools_form.last_check_date.data
        check_period = add_tools_form.check_period.data
        vendor = add_tools_form.vendor.data
        use_bureau = add_tools_form.use_bureau.data
        use_department = add_tools_form.use_department.data
        use_shift = add_tools_form.use_shift.data
        user = add_tools_form.user.data
        remarks = add_tools_form.remarks.data

        tool = db.add_tool(tool_id, name, model, picture.read(), position, category, status, need_check,
                           last_check_date, check_period, vendor, use_bureau, use_department, use_shift, user, remarks)

        if tool is not None:
            flash('添加工具成功!')
            return redirect(url_for('dashboard_handler'))
        else:
            flash('添加工具失败!')

    return render_template('add_tool.html', form=add_tools_form), 200


@app.route('/dashboard/batch_add_tool', methods=['GET', 'POST'])
def batch_add_tools_handler():
    return render_template('batch_add_tool.html'), 200


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_handler():
    return render_template('dashboard.html'), 200

if __name__ == "__main__":
    app.run()
