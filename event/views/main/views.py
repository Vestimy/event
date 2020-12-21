from flask import Blueprint, jsonify, request, render_template, redirect
from event import logger, config
from werkzeug.utils import secure_filename
from event import logger, config
# from blog.schemas import VideoSchema, UserSchema, AuthSchema
# from flask_apispec import use_kwargs, marshal_with
from event.models import *
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from blog.base_view import BaseView
# from blog.utils import upload_file
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from event.forms import *

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    return render_template('main/index.html', menu='main')


@main.route('/calendar', methods=['GET'])
def cal():
    return render_template('main/cal.html', menu='cals')

# @main.route('/register', methods=['GET', 'POST'])
# def register_user():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         try:
#
#             user = User(name=name, email=email, password=password)
#             db.session.add(user)
#             db.session.commit()
#         except Exception as e:
#             logger.warning(
#                 f' BD - wright action failed with errors: {e}'
#             )
#             db.session.rollback()
#
#         return redirect(url_for('main.index'))
#     form = RegisterForm()
#     return render_template('main/register.html', form=form)

# docs.register(get_list, blueprint='videos')
# docs.register(update_list, blueprint='videos')
# docs.register(update_tutorial, blueprint='videos')
# docs.register(delete_list, blueprint='videos')
# # docs.register(get_video, blueprint=videos)
# ListView.register(videos, docs, '/main', 'listview')
