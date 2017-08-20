#!/usr/bin/env python
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
    user = User(user_id = user_id,
                password = password,
                name = name,
                sex = sex,
                photo = photo,
                duty = duty,
                department = department,
                phone_number =  phone_number,
                admin = admin,
                remarks = remarks)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception, e:
        print('Exception:', e)
        return None, e

    return user, None


def delete_user(user_id, admin_id, admin_password):
    pass

    
