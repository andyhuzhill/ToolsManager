#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-04 22:25:28
# @Author  : ${Your Name} (${you@example.org})
# @Link    :
# @Version : ${1.0.0}

import os

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField, IntegerField, BooleanField, DateField
from wtforms.validators import Required, Regexp

class LoginForm(FlaskForm):
    user_name = StringField('用户名', validators=[Required()])
    login_password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')

    submit = SubmitField('登录')

class AddUserForm(FlaskForm):
    user_id = StringField('用户名', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    name = StringField('姓名', validators=[Required()])
    sex = SelectField("性别", validators=[Required()], choices=[
            (1, "男"), (2, "女")], coerce=int)
    photo = FileField('照片', validators=[Required()])
    duty = StringField('职务', validators=[Required()])
    department = StringField('部门', validators=[Required()])
    telephone = StringField('电话号码', validators=[Required(), Regexp('^\d+$')])
    admin = SelectField('权限', validators=[Required()], choices=[
            (1, "普通用户"), (2, "管理员")], coerce=int)
    remarks = TextAreaField('备注')
    submit = SubmitField('添加')


class AddToolsForm(FlaskForm):
    tool_id = IntegerField('工具编号', validators=[Required()])
    name = StringField('名称', validators=[Required()])
    model = StringField('型号', validators=[Required()])
    picture = FileField('图片', validators=[Required()])
    position = StringField('定置点', validators=[Required()])
    category = StringField('类别', validators=[Required()])
    status = SelectField('状态', validators=[Required()],
                         choices=[(1, "在库"), (2, "审批中"), (3, "借出"), (4, "送检中")], coerce=int)
    need_check = BooleanField('是否需要定检', validators=[Required()])
    last_check_date = DateField('上次定检时间', format='%Y-%m-%d')
    check_period = IntegerField('定检周期(月)')
    vendor = StringField('厂家', validators=[Required()])
    use_bureau = StringField('使用局', validators=[Required()])
    use_department = StringField('使用部门', validators=[Required()])
    use_shift = StringField('使用班组', validators=[Required()])
    user = StringField('使用人', validators=[Required()])
    remarks = StringField('备注')
    submit = SubmitField('添加')
