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
    return render_template('arena/get_list_arena.html', menu='arenas', id=id, typehall=typehall, arena=arena)



@administrator.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
