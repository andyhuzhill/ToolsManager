#!/usr/bin/env python3~
# -*- coding: utf-8 -*-
# @Date    : 2017-08-19 10:50:38
# @Author  : ${Your Name} (${you@example.org})
# @Link    :
# @Version : ${1.0.0}

import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask, request, session, render_template, redirect, url_for, flash, make_response

from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, LoginManager, current_user

import db
from forms import LoginForm, AddUserForm, AddToolsForm, SiteInfoForm

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = u'请先登录以访问该网页!'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
login_manager.init_app(app)


@app.route('/', methods=['GET'])
@login_required
def index():
    siteInfo = db.get_site_info()
    userinfo = None
    if current_user.is_authenticated:
        userinfo = db.query_user(current_user.get_id())

    return render_template('index.html', userinfo=userinfo, siteInfo=siteInfo)


@app.route('/t/', methods=['GET', 'POST'])
def query_tools():
    tool_id = request.args.get('qr', None)
    tool_info = db.query_tool_infos(tool_id)
    return render_template('tools_details.html', info=tool_info)


@app.route('/borrow_request/<tool>/from/<user>', methods=['POST'])
@login_required
def borrow_request(tool, user):
    app.logger.debug("borrow request tool_id = " + tool)
    app.logger.debug("borrow request user_id = " + user)
    db.request_borrow_tool(tool, user)
    return redirect(url_for('query_tools', qr=tool))


@app.route('/send_to_check/<tool>', methods=["POST"])
@login_required
def send_to_check(tool):
    app.logger.debug("send_to_check tool_id = " + tool)

    db.send_tool_to_check(tool)

    return redirect(url_for('query_tools', qr=tool))


@app.route('/approve_borrow/<tool>', methods=["POST"])
@login_required
def approve_borrow(tool):
    app.logger.debug("approve borrow tool_id = " + tool)

    db.approve_borrow(tool, current_user, "")

    return redirect(url_for('query_tools', qr=tool))


@app.route('/deny_borrow/<tool>', methods=["POST"])
@login_required
def deny_borrow(tool):
    app.logger.debug("deny borrow tool_id = " + tool)

    db.deny_borrow(tool)

    return redirect(url_for('query_tools', qr=tool))


@app.route('/return_request/<tool>', methods=["POST"])
@login_required
def return_request(tool):
    app.logger.debug("return_request tool_id = " + tool)
    db.request_return(tool)

    return redirect(url_for('query_tools', qr=tool))


@app.route('/approve_return/<tool>', methods=['POST'])
@login_required
def approve_return(tool):
    app.logger.debug("approve_return tool_id = " + tool)

    db.approve_return(tool, current_user)

    return redirect(url_for('query_tools', qr=tool))


@app.route('/deny_return/<tool>', methods=["POST"])
@login_required
def deny_return(tool):
    app.logger.debug("deny_return tool_id = " + tool)

    db.deny_return(tool, current_user, "")

    return redirect(url_for('query_tools', qr=tool))


@app.route('/check_finished/<tool>', methods=["POST"])
@login_required
def check_finished(tool):
    app.logger.debug("check_finished tool_id = " + tool)

    db.check_finished(tool)

    return redirect(url_for('query_tools', qr=tool))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    site_info = db.get_site_info()
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        login_password = login_form.login_password.data
        user = db.User.query.filter_by(name=user_name).first()
        if user is not None and user.verify_password(login_password):
            if login_user(user, login_form.remember_me.data):
                flash('登录成功!')
                return redirect(url_for('index'))
        flash('用户名或密码错误')

    return render_template('login.html', form=login_form, siteInfo=site_info)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您的帐号已注销')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/dashboard/approval', methods=['GET', 'POST'])
def approval():
    apply_list = db.get_apply_list()
    return render_template('approval.html', apply_list=apply_list)


@app.route('/images/tools/<tool_id>', methods=['GET'])
@login_required
def tool_image_handler(tool_id):
    tool_info = db.query_tool_infos(tool_id)
    if tool_info["found"]:
        response = make_response(tool_info["picture"])
        return response
    return ""


@app.route('/images/users/<user_id>', methods=['GET'])
@login_required
def user_image_handler(user_id):
    user_info = db.query_user(user_id)
    if user_info['found']:
        response = make_response(user_info["user"].photo)
        return response
    return ""


@app.route('/dashboard/add_user', methods=['GET', 'POST'])
@login_required
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

        user = db.add_user(user_id, password, user_name, sex,
                           photo.read(), duty, department, telephone, admin, remarks)

        if user is not None:
            flash("添加用户成功!")
            return redirect(url_for('dashboard_handler'))
        else:
            flash("添加用户失败!")

    return render_template('add_user.html', form=add_user_form)


@app.route('/dashboard/batch_add_users', methods=['GET', 'POST'])
@login_required
def batch_add_users_handler():
    return render_template('batch_add_users.html')


@app.route('/dashboard/users_list', methods=['GET', 'POST'])
@login_required
def users_list_handler():
    user_info_list = db.get_all_user_infos()
    return render_template('users_list.html', user_list=user_info_list)


@app.route('/dashboard/add_tools', methods=['GET', 'POST'])
@login_required
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

        tool = db.add_tool(tool_id, name, model, picture.read(), position, category, status, 
                           need_check, last_check_date, check_period, vendor, use_bureau, 
                           use_department, use_shift, user, remarks)

        if tool is not None:
            flash('添加工具成功!')
            return redirect(url_for('dashboard_handler'))
        else:
            flash('添加工具失败!')

    return render_template('add_tool.html', form=add_tools_form)


@app.route('/dashboard/batch_add_tools', methods=['GET', 'POST'])
@login_required
def batch_add_tools_handler():
    return render_template('batch_add_tools.html')


@app.route('/dashboard/tools/<tool>', methods=['DELETE'])
@login_required
def delete_tool(tool):
    if current_user.admin == 2:
        if db.delete_tool(tool):
            flash('删除成功!')
        else:
            flash('删除失败!')
    else:
        flash('权限不够')

    return redirect(url_for('index'))


@app.route('/dashboard/tools_list', methods=['GET', 'POST'])
@login_required
def tools_list_handler():
    tools_list = db.get_all_tools()
    return render_template('tools_list.html', tool_infos=tools_list)


@app.route('/dashboard/site_info_edit', methods=['GET', 'POST'])
@login_required
def site_info():
    siteInfoForm = SiteInfoForm()
    if siteInfoForm.validate_on_submit():
        info = db.set_site_info(siteInfoForm.site_name.data,
                                siteInfoForm.welcome_info.data, siteInfoForm.copyright_info.data)
        if info is not None:
            flash('站点信息修改成功!')
            return redirect(url_for('index'))
        else:
            flash('站点信息修改失败!')
    return render_template("siteinfo.html", form=siteInfoForm)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_handler():
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run()
