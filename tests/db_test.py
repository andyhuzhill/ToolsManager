#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-08-20 14:41:07
# @Author  : ${Your Name} (${you@example.org})
# @Link    :
# @Version : ${1.0.0}

import os
basedir = os.path.abspath(os.path.dirname(__file__))

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(basedir + "/..")

import unittest
import db
import random


class TestDataBase(unittest.TestCase):

    def test_add_user(self):
        user, err = db.add_user(user_id='{0}'.format(
            random.randint(0, 1000)),
            password='12345678',
            name='Test 1',
            sex=0,
            photo=open(os.path.join(
                basedir, 'head.png')).read(),
            duty=u'班员',
            department=u'变电管理二所',
            phone_number='19121525252',
            admin=False,
            remarks='')

        self.assertTrue(err == None)
        if err == None:
            print(user)
        self.assertTrue(user != None)


if __name__ == "__main__":
    unittest.main()
