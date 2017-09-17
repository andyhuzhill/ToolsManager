#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-08-20 14:15:33
# @Author  : ${Your Name} (${you@example.org})
# @Link    :
# @Version : ${1.0.0}

from flask_sqlalchemy import SQLAlchemy

from models import db, User, Tools, BorrowRecord, SiteInfo

from datetime import date


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
    admin = User.query.filter_by(user_id=admin_id).first()
    if admin is not None:
        if admin.verify_password(admin_password):
            user = User.query.filter_by(user_id=user_id).first()
            if user is not None:
                db.session.delete(user)
                db.session.commit()
                return True

    return False


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
                 borrow_user=None,
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


def delete_tool(tool_id):
    tool = Tools.query.filter_by(tool_id=tool_id).first()
    if tool is not None:
        db.session.delete(tool)
        db.session.commit()
        return True
    return False


def request_borrow_tool(tool_id, user_id):
    tool = Tools.query.filter_by(tool_id=tool_id).first()
    if tool is not None:
        tool.borrow_user = user_id
        tool.status = 2

        db.session.add(tool)
        db.session.commit()
        return True

    return False


def send_tool_to_check(tool_id):
    tool = Tools.query.filter_by(tool_id=tool_id).first()
    if tool is not None:
        tool.status = 5

        db.session.add(tool)
        db.session.commit()
        return True
    return False


def approve_borrow(tool_id, current_user, remarks):
    tool = Tools.query.filter_by(tool_id=tool_id).first()
    if tool is not None:
        tool.status = 3
        db.session.add(tool)

        borrow_record = BorrowRecord(tool_id=tool_id, user_id=tool.borrow_user,
         borrow_date=date.today(), borrow_check_user=current_user.user_id, remarks=remarks)

        db.session.add(borrow_record)

        db.session.commit()

        return True

    return False


def deny_borrow(tool_id):
    tool = Tools.query.filter_by(tool_id=tool_id).first()
    if tool is not None:
        tool.status = 1

        db.session.add(tool)
        db.session.commit()
        return True
    return False


def request_return(tool_id):
    tool = Tools.query.filter_by(tool_id=tool_id).first()
    if tool is not None:
        tool.status = 4

        db.session.add(tool)
        db.session.commit()
        return True
    return False


def approve_return(tool_id, current_user):
    tool = Tools.query.filter_by(tool_id=tool_id).first()
    if tool is not None:
        tool.status = 1

        borrow_user_id = tool.borrow_user
        borrow_user = User.query.filter_by(user_id=borrow_user_id).first()

        db.session.add(tool)

        borrow_record = BorrowRecord.query.filter_by(
            tool_id=tool_id, user_id=borrow_user_id).first()

        if borrow_record is not None:
            borrow_record.return_date = date.today()
            borrow_record.return_check_user = current_user.user_id

            db.session.add(borrow_record)
        db.session.commit()

        return True

    return False


def deny_return(tool_id, current_user, remark):
    tool = Tools.query.filter_by(tool_id=tool_id).first()
    if tool is not None:
        tool.status = 3

        db.session.add(tool)
        db.session.commit()
        return True
    return False


def check_finished(tool_id):
    tool = Tools.query.filter_by(tool_id=tool_id).first()
    if tool is not None:
        tool.status = 1

        db.session.add(tool)
        db.session.commit()
        return True
    return False


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
        result["borrow_user"] = tool.borrow_user
        result["remarks"] = tool.remarks
    return result


def set_site_info(site_name, welcome_info, copyright_info):
    siteInfo = SiteInfo.query.first()
    if siteInfo is None:
        siteInfo = SiteInfo(
            site_name=site_name, welcome_info=welcome_info, copyright_info=copyright_info)
    else:
        siteInfo.site_name = site_name
        siteInfo.welcome_info = welcome_info
        siteInfo.copyright_info = copyright_info

    try:
        db.session.add(siteInfo)
        db.session.commit()
    except Exception as e:
        print('Exception!', e)
        return None
    return siteInfo


def get_site_info():
    siteInfo = SiteInfo.query.first()
    return siteInfo


def get_apply_list():
    borrow_request_list = Tools.query.filter_by(status = 2).all()
    return_request_list = Tools.query.filter_by(status = 4).all()

    result = {}
    result["borrow_list"] = borrow_request_list
    result["return_list"] = return_request_list

    return result
