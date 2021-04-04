from flask import Blueprint, jsonify, request, json, render_template, redirect
from flask import abort
from event import logger, config, allowed_photo_profile
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_security import login_required, current_user
from event.decorators import decorated_admin
from event.forms import *

friends = Blueprint('friends', __name__)


@friends.route('/friends/', methods=['GET'])
@login_required
def index():
    return render_template('mailbox.html')


