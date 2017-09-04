#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-04 22:25:28
# @Author  : ${Your Name} (${you@example.org})
# @Link    : 
# @Version : ${1.0.0}

import os

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import Required, Regexp

class AddUserForm(FlaskForm):
    user_id = StringField('用户名', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    name = StringField('姓名', validators=[Required()])
    sex =  SelectField("性别", validators=[Required()], choices=[(1, "男"), (2, "女")], coerce=int)
    photo = FileField('照片', validators=[Required()])
    duty = StringField('职务', validators=[Required()])
    department = StringField('部门', validators=[Required()])
    telephone = StringField('电话号码', validators=[Required(), Regexp('^\d+$')])
    admin = SelectField('权限', validators=[Required()], choices=[(1, "普通用户"), (2, "管理员")], coerce=int)
    remarks = TextAreaField('备注')
    submit = SubmitField('添加')
