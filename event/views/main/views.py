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
from flask_security import login_required

from event.forms import *

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    return render_template('main/index.html', menu='main')


@main.route('/calendar', methods=['GET'])
def calendar():
    return render_template('main/cal.html', menu='calendars')


@main.route('/get_calendar', methods=['GET', 'POST'])
# @login_required
def get_calendar():
    event = Event.query.all()
    list_json = []
    for item in event:
        # print(type(item.date_event.strftime("%Y-%m-%d ")))
        if item.time_event:
            start = item.date_event.strftime("%Y-%m-%d") + "T" + item.time_event.strftime("%H:%M:%S")
        else:
            start = item.date_event.strftime("%Y-%m-%d")
        list_json.append({
            "title": item.artist.name,
            # "start": item.date_event.strftime("%Y-%m-%d"),
            "start": start,
            "description": item.description,
            "url": url_for("events.get_item_event", id=item.id)
        })
    list_jsons = [
        {
            'title': 'All Day Event',
            "start": '2020-09-01',
        },
        {
            'title': 'Long Event',
            "start": '2020-09-07',
            "end": '2020-09-10'
        },
        {
            "groupId": 999,
            'title': 'Repeating Event',
            "start": '2020-09-09T16:00:00'
        },
        {
            "groupId": 999,
            'title': 'Repeating Event',
            "start": '2020-09-16T16:00:00'
        },
        {
            'title': 'Conference',
            "start": '2020-09-11',
            "end": '2020-09-13'
        },
        {
            'title': 'Meeting',
            "start": '2020-09-12T10:30:00',
            "end": '2020-09-12T12:30:00'
        },
        {
            'title': 'Lunch',
            "start": '2020-09-12T12:00:00'
        },
        {
            'title': 'Meeting',
            "start": '2020-09-12T14:30:00'
        },
        {
            'title': 'Happy Hour',
            "start": '2020-09-12T17:30:00'
        },
        {
            'title': 'Dinner',
            "start": '2020-09-12T20:00:00'
        },
        {
            'title': 'Birthday Party',
            "start": '2020-09-13T07:00:00'
        },
        {
            'title': 'Click for Google',
            "url": 'http://google.com/',
            "start": '2020-09-28'
        }
    ]
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
