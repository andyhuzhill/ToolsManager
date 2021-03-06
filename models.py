#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-08-19 11:06:55
# @Author  : ${Your Name} (${you@example.org})
# @Link    :
# @Version : ${1.0.0}

from sqlalchemy import Column, Integer, String, Date, Boolean, LargeBinary

from app import app, login_manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin


db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    else:
        return None

class User(UserMixin, db.Model):
    """
        System user informations
    """
    # Table Name
    __tablename__ = 'users'

    # 用户名
    user_id = Column(String, primary_key=True, nullable=False, unique=True)

    def get_id(self):
        return self.user_id

    # 密码
    password_hash = Column(String, nullable=False)

    @property
    def password(self):
        return ''
        # raise AttributeError("login_password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 姓名
    name = Column(String, nullable=False)

    # 性别
    sex = Column(Integer, nullable=False)

    # 照片
    photo = Column(LargeBinary, nullable=False)

    # 职务
    duty = Column(String, nullable=False)

    # 部门
    department = Column(String, nullable=False)

    # 电话号码
    phone_number = Column(String, nullable=False)

    # 管理员权限 1 普通用户 2 管理员
    admin = Column(Integer, nullable=False)

    # 备注
    remarks = Column(String, nullable=True)

    def __repr__(self):
        return "<User(user_id={0}, password={1}, name={2}, sex={3}, duty={4}, department={5}, phone_number={6}, admin={7}, remarks={8}) >".format(
    self.user_id, self.password, self.name, self.sex, self.duty, self.department, self.phone_number,  self.admin, self.remarks)


class Tools(db.Model):
    """
        Tools
    """

    __tablename__ = "tools"

    # 工具二维码编号
    tool_id = Column(Integer, primary_key=True, nullable=False)

    # 名称
    name = Column(String, nullable=False)

    # 型号
    model = Column(String, nullable=False)

    # 图片
    picture = Column(LargeBinary, nullable=False)

    # 定置号
    position = Column(String, nullable=False)

    # 类别
    category = Column(String, nullable=False)

    # 状态
    # 1 在库　2 审批中　3 借出 4 申请归还 5 送检中
    status = Column(Integer, nullable=False)

    # 是否需要定检
    need_check = Column(Boolean, nullable=False)

    # 上次定检时间
    last_check_date = Column(Date, nullable=True)

    # 定检周期
    # 单位: 月
    check_period = Column(Integer, nullable=True)

    # 厂家
    vendor = Column(String, nullable=False)

    # 使用局
    use_bureau = Column(String, nullable=False)

    # 使用部门
    use_department = Column(String, nullable=False)

    # 使用班组
    use_shift = Column(String, nullable=False)

    # 使用人
    user = Column(String, nullable=False)

    # 借用人
    borrow_user = Column(String, nullable=True)

    # 备注
    remarks = Column(String, nullable=True)


    def __repr__(self):
        return "<Tools(tool_id={0}, name={1}, model={2}, position={3}, category={4}, status={5}, need_check={6}, last_check_date={7}, check_period={8}, vendor={9}, use_bureau={10}, use_department={11}, use_shift={12}, user={13}, borrow_user={14} remarks={15})>".format(
        self.tool_id, self.name, self.model, self.position, self.category, self.status, self.need_check, self.last_check_date, self.check_period, self.vendor, self.use_bureau, self.use_department, self.use_shift, self.borrow_user, self.user, self.remarks)


class BorrowRecord(db.Model):
    """
       BorrowRecord
    """

    id = Column(Integer, primary_key=True, nullable=False)

    # 工具二维码编号
    tool_id = Column(String, nullable=False)

    # 借用人
    user_id = Column(String, nullable=False)

    # 借出时间
    borrow_date = Column(Date, nullable=False)

    # 借出审批人
    borrow_check_user = Column(String, nullable=True)

    # 归还时间
    return_date = Column(Date, nullable=True)

    # 归还审批人
    return_check_user = Column(String, nullable=True)

    # 备注
    remarks = Column(String, nullable=False)


    def __repr__(self):
        return "<BorrowRecord(id={0}, tool_id={1}, user_id={2}, borrow_date={3},  borrow_check_user={4}, return_date ={4}, return_check_user={5}, remarks={6})>".format(
        self.id, self.tool_id, self.user_id, self.borrow_date, self.borrow_check_user, self.return_date, self.return_check_user, self.remarks)


class SiteInfo(db.Model):
    """
        site copyright informations
    """
    __tablename__ = "site_info"

    site_name = Column(String, nullable=False, primary_key=True)

    welcome_info = Column(String, nullable=False)

    copyright_info = Column(String, nullable=False)
