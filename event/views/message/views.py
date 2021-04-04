from flask import Blueprint, jsonify, request, json, render_template, redirect
from flask import abort
from event import logger, config, allowed_photo_profile
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_security import login_required, current_user
from event.decorators import decorated_admin
from event.forms import *

messages = Blueprint('messages', __name__)


@messages.route('/messages/', methods=['GET'])
@login_required
def index():
    messages = PrivateMessages.query.filter(PrivateMessages.recipient_id == current_user.id).order_by(PrivateMessages.create.desc()).all()
    return render_template('mailbox.html', messages=messages)



@messages.route('/api/send_message/<int:id>', methods=['GET', 'POST'])
@login_required
def send_message(id):
    sender = User.query.get(current_user.id)
    recipient = User.query.get(id)
    message = PrivateMessages()
    form = SendMessageForm(request.form, message)
    if request.method == 'POST':
        try:
            form.populate_obj(message)
            message.sender.append(sender)
            message.recipient.append(recipient)
            db.session.commit()
        except Exception:
            db.session.rollback()
    return redirect(request.referrer)
