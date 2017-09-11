#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-08-20 14:15:33
# @Author  : ${Your Name} (${you@example.org})
# @Link    :
# @Version : ${1.0.0}

from flask_sqlalchemy import SQLAlchemy

from models import db, User, Tools, BorrowRecord


def init_database():
    db.create_all()


def add_user(user_id, password, name, sex, photo, duty, department, phone_number, admin, remarks):
    find = User.query.filter_by(user_id=user_id).first()

    if find is None:
        try:
            user = User(user_id=user_id,
                password=password,
                name=name,
                sex=sex,
                photo=photo,
                duty=duty,
                department=department,
                phone_number=phone_number,
                admin=admin,
                remarks=remarks)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print('Exception!', e)
            return None
    else:
        return None

    return user


def get_all_user_infos():
    return User.query.all()


def query_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    result = dict()
    result["found"] = False
    if user is not None:
        result["found"] = True
        result["user"] = user
    return result


def delete_user(user_id, admin_id, admin_password):
    pass


def add_tool(tool_id, name, model, picture, position, category, status, need_check, last_check_date, check_period, vendor, use_bureau, use_department, use_shift, user, remarks):
    tool = Tools(tool_id=tool_id,
                 name=name,
                 model=model,
                 picture=picture,
                 position=position,
                 category=category,
                 status=status,
                 need_check=need_check,
                 last_check_date=last_check_date,
                 check_period=check_period,
                 vendor=vendor,
                 use_bureau=use_bureau,
                 use_department=use_department,
                 use_shift=use_shift,
                 user=user,
                 remarks=remarks)

    find = Tools.query.filter_by(tool_id=tool_id).first()

    if find is None:
        try:
            db.session.add(tool)
            db.session.commit()
        except Exception as e:
            print('Exception!', e)
            return None
    else:
        return None

    return tool


def get_all_tools():
    return Tools.query.all()


def query_tool_infos(tool_id):
    tool = Tools.query.filter_by(tool_id=tool_id).first()
    result = dict()
    result["found"] = False
    if tool is not None:
        result["found"] = True
        result["tool_id"] = tool.tool_id
        result["name"] = tool.name
        result["model"] = tool.model
        result["picture"] = tool.picture
        result["position"] = tool.position
        result["category"] = tool.category
        result["status"] = tool.status
        result["need_check"] = tool.need_check
        result["last_check_date"] = tool.last_check_date
        result["check_period"] = tool.check_period
        result["vendor"] = tool.vendor
        result["use_bureau"] = tool.use_bureau
        result["use_department"] = tool.use_department
        result["use_shift"] = tool.use_shift
        result["user"] = tool.user
        result["remarks"] = tool.remarks
    return result
