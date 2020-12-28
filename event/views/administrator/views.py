import os
from flask import Blueprint, jsonify, request, render_template, redirect
from event import logger, config, allowed_photo_profile
from flask_security import login_required, roles_required, current_user, login_user
from flask import flash, request, redirect, url_for
from event.forms import *
from werkzeug.utils import secure_filename

administrator = Blueprint('administrator', __name__)


@administrator.route('/administrator', methods=['GET'])
@roles_required('super_admin')
def index():
    return render_template('administrator/index.html')


@administrator.route('/profile', methods=['GET'])
@roles_required('super_admin')
def profile():
    return render_template('administrator/profile.html')
#
#
# @administrator.route('/administrator', methods=['GET'])
# @roles_required('super_admin')
# def index():
#     return render_template('administrator/index.html')
#
#
# @administrator.route('/administrator', methods=['GET'])
# @roles_required('super_admin')
# def index():
#     return render_template('administrator/index.html')
#
#
# @administrator.route('/administrator', methods=['GET'])
# @roles_required('super_admin')
# def index():
#     return render_template('administrator/index.html')


@administrator.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
