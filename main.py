#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-08-20 14:24:38
# @Author  : ${Your Name} (${you@example.org})
# @Link    : 
# @Version : ${1.0.0}

from db import db
from app import app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
    