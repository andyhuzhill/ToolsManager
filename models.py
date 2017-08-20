#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-19 11:06:55
# @Author  : ${Your Name} (${you@example.org})
# @Link    :
# @Version : ${1.0.0}

from sqlalchemy import Column, Integer, String, Date, Boolean, LargeBinary
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class User(Base):
    """
        System user informations
    """
    # Table Name
    __table__ = 'users'

    # 用户名
    user_id = Column(String, primary_key=True, nullable=False, unique=True)

    # 密码
    password = Column(String, nullable=False)

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

    # 管理员权限
    admin = Column(Boolean, nullable=False)

    # 备注
    remarks = Column(String, nullable=True)


class Tools(Base):
    """
        Tools
    """

    __table__ = "tools"

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
    # 0 在库　1 审批中　2 借出 3 送检中
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

    # 备注
    remarks = Column(String, nullable=True)


class BorrowRecord(Base):
    """
       BorrowRecord
    """

    id = Column(Integer, primary_key=True, nullable=False)

    # 工具二维码编号
    tool_id = Column(String, nullable=False)

    # 借用人
    user_id = Column(String, nullable=False)

    # 借出时间
    borrow_date = Column(Date, nullable=True)

    # 借出审批人
    borrow_check_user = Column(String, nullable=False)

    # 归还时间
    return_data = Column(Date, nullable=True)

    # 归还审批人
    return_check_user = Column(String, nullable=False)

    # 备注
    remarks = Column(String, nullable=False)
