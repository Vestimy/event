import os
from flask import Blueprint, jsonify, request, render_template, redirect, json
from event import logger, config, allowed_photo_profile
from flask_security import login_required, roles_required, current_user, login_user
from flask import flash, request, redirect, url_for
from event.forms import *
from werkzeug.utils import secure_filename

api = Blueprint('api', __name__)


@api.route('/api/event_calendar', methods=['GET', 'POST'])
# @login_required
def api_event_calendar():
    event = Event.query.all()
    list_json = []

    for item in event:
        list_json.append({"date": item.date_event.strftime("%Y-%m-%d ") + item.time_event.strftime("%H:%M:%S"),
                          "title": item.artist.last_name + item.artist.first_name,
                          "description": item.description,
                          "url": url_for("events.get_item_event", id=item.id)})

    return json.dumps(list_json)


@api.route('/api/arena_choices', methods=('GET', 'POST'))
@login_required
def api_arena_choices():
    city_id = request.form['city_id']
    print(city_id)
    print(request.form)
    item_list = Arena.query.filter_by(city_id=city_id).all()
    result_list = dict()
    for item in item_list:
        result_list[item.id] = item.name
    return json.dumps(result_list)


@api.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
