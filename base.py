from manage import app, db

from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from event.model import *
from event.model.equipment import *
from event.model.menu import *
from event.model.city import *

if __name__ == '__main__':
    manager.run()