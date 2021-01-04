from flask import Blueprint, jsonify, request, json, render_template, redirect
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
from flask_security import login_required, current_user

from event.forms import *

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
@login_required
def mains():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))


@main.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', menu='index')


@main.route('/profile/', methods=['GET'])
def profile_all():
    if current_user.is_authenticated:
        id = current_user.id
        user = User.query.get(id)
        return redirect(url_for('main.profile', id=id))
    return redirect(url_for('security.login'))


@main.route('/profile/<int:id>', methods=['GET'])
def profile(id, page=1):
    per_page = 10
    user = User.query.get(id)
    page = request.args.get('page', type=int, default=1)
    events = Event.query.filter(Event.user_id == user.id).order_by(Event.date_event.desc()).paginate(page, per_page,
                                                                                                     error_out=False)
    # all_events = Event.query.join(event_staff_users).filter(event_staff_users == user.id).all()
    # all_events = Event.query.filter(Event.users_staff.any(User.id.in_([user.id]))).all()
    # chat.query.join(user.chats).filter(user.id == 1).all()
    # User.query.filter(User.roles.any(Role.name.in_(["manager"]))
    # print(all_events)
    sum_event = len(user.event_staff)
    admin_event = len(user.event)
    return render_template('profile.html', menu="team", user=user, events=events, sum_event=sum_event,
                           admin_event=admin_event)


@main.route('/managers', methods=['GET'])
def managers():
    try:
        managers = User.query.filter(User.roles.any(Role.name.in_(['manager']))).order_by(User.last_name).all()
    except Exception as e:
        logger.warning(
            f'{current_user.last_name} - reads action failed with errors: {e}'
        )
    return render_template('team.html', menu="managers", managers=managers)


@main.route('/team', methods=['GET'])
def team():
    try:
        managers = User.query.filter(User.roles.any(Role.name.in_(['users']))).order_by(User.last_name).all()
    except Exception as e:
        logger.warning(
            f'managers - reads action failed with errors: {e}'
        )
    return render_template('team.html', menu="team", managers=managers)


@main.route('/city', methods=['GET', 'POST'])
def city():
    form = CitysForm()
    try:
        city = City()
    except Exception as e:
        logger.warning(
            f'managers - reads action failed with errors: {e}'
        )
    return render_template('form_basic.html', form=form)


@main.route('/calendar', methods=['GET'])
def calendar():
    return render_template('main/cal.html', menu='calendars')


@main.route('/get_calendar', methods=['GET', 'POST'])
# @login_required
def get_calendar():
    event = Event.query.all()
    list_json = []
    for item in event:
        title = f'{item.artist.last_name}'
        start = item.date_event.strftime("%Y-%m-%d")
        if item.artist.first_name:
            title = f'{item.artist.last_name} {item.artist.first_name}'
        if item.time_event:
            start = item.date_event.strftime("%Y-%m-%d") + "T" + item.time_event.strftime("%H:%M:%S")
        list_json.append({
            "title": title,
            "start": start,
            "description": item.description,
            "url": url_for("events.get_item_event", id=item.id)
        })

    return json.dumps(list_json)


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400

# docs.register(get_list, blueprint='videos')
# docs.register(update_list, blueprint='videos')
# docs.register(update_tutorial, blueprint='videos')
# docs.register(delete_list, blueprint='videos')
# # docs.register(get_video, blueprint=videos)
# ListView.register(videos, docs, '/main', 'listview')
