from flask import Blueprint, jsonify, request, json, render_template, redirect
from event import logger, config
from werkzeug.utils import secure_filename
from event import logger, config
# from event import logger, config, mail
# from blog.schemas import VideoSchema, UserSchema, AuthSchema
# from flask_apispec import use_kwargs, marshal_with
from event.models import *
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from blog.base_view import BaseView
# from blog.utils import upload_file
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_mail import Message
from flask_security import login_required, current_user, roles_required, roles_accepted

from event.forms import *

events = Blueprint('events', __name__)

# class ListView(BaseView):
#     @marshal_with(VideoSchema(many=True))
#     def get(self):
#         try:
#             videos = Video.get_list()
#         except Exception as e:
#             logger.warning(
#                 f'tutorials - read action failed with errors: {e}'
#             )
#             return {'message': str(e)}, 400
#         return videos
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

UPLOAD_FOLDER = 'uploads'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @jwt_required
# @marshal_with(VideoSchema(many=True))
@events.route('/events/', methods=['GET'])
def get_event():
    try:
        event = Event.query.order_by(Event.date_event.desc())
        type_event = TypeEvent.query.order_by('name').all()
        id = None
    except Exception as e:
        logger.warning(
            f'user: {current_user.last_name} Events - read action failed with errors: {e}'
        )
        return {'message': str(e)}, 400
    if request.args.get('id'):
        try:
            id = int(request.args.get('id'))
        except Exception as e:
            logger.warning(
                f'arenas -  action failed with errors: {e}'
            )
        if isinstance(id, int):
            event = Event.query.filter(Event.typeevent_id == id).order_by('name').all()
    return render_template('event/get_event.html', id=id, menu='events', events=event, type_event=type_event)


@events.route('/events/<int:id>', methods=['GET'])
def get_item_event(id):
    try:
        # user_id = get_jwt_identity()
        # events = Event.get_list()
        event = Event.query.get(id)
    except Exception as e:
        logger.warning(
            f'user: {current_user.last_name} tutorials - read action failed with errors: {e}'
        )
        return {'message': str(e)}, 400
    # return videos
    return render_template('event/item_event.html', menu='events', item=event)


@events.route('/events/add', methods=['GET', 'POST'])
@roles_accepted('admin ', 'manager')
def add_event():
    form = EventForm()
    if request.method == "POST":
        try:
            name = request.form['name']
            artist_id = request.form['artist_id']
            date_event = request.form['date_event']
            time_event = request.form['time_event']
            typeevent_id = request.form['typeevent_id']
            description = request.form['description']
            city_id = request.form['city_id']

            arena_id = request.form['arena_id']
            user_id = request.form['user_id']
            print(date_event)

            event = Event(name=name,
                          artist_id=artist_id,
                          date_event=date_event,
                          time_event=time_event,
                          typeevent_id=typeevent_id,
                          description=description,
                          city_id=city_id,
                          arena_id=arena_id,
                          user_id=user_id
                          )
            print(request.form)

            db.session.add(event)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    # form.artist_id.choices = [(g.id, g.name) for g in Artist.query.order_by('name')]
    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    # form.arena_id.choices = [(g.id, g.name) for g in Arena.query.order_by('name')]
    # form.manager_id.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]
    # form..choices = [(g.id, g.name) for g in City.query.order_by('name')]
    # form.managers.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]
    # form.arenas.choices = [(g.id, g.title) for g in Arena.query.order_by('title')]
    return render_template('event/add_event.html',menu='events', form=form)


@events.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'manager')
def edit_event(id):
    event = Event.query.filter(Event.id == id).first()
    form = EventForm(obj=event)
    print(current_user.id)
    print(event.user_id)
    if current_user.id == event.user_id or "admin" in current_user.roles:
        # print(form.date_event)
        if event is None:
            raise Exception('Ошибка нет такого поста')
        if request.method == 'POST':
            form = EventForm(formdata=request.form, obj=event)
            print(form.time_event)
            form.populate_obj(event)
            db.session.commit()

            return redirect(url_for('events.get_item_event', menu='events', id=event.id))

    # form.artist_id.choices = [(g.id, g.name) for g in Artist.query.order_by('name')]
    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    # form.arena_id.choices = [(g.id, g.name) for g in Arena.query.order_by('name')]
    # form.manager_id.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]

        return render_template('event/edit_event.html', menu='events', form=form, item=event)
    return redirect(url_for("events.get_event"))

@events.route('/events/delete/<int:id>', methods=['GET'])
@roles_accepted('admin', 'manager')
def delete_event(id):
    event = Event.query.get(id)
    if current_user.id == event.user_id or "admin" in current_user.roles:
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('events.get_event'))


@events.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            item = Rider(name=filename, url=filename)
            session.add(item)
            session.commit()
            file.save(os.path.join('/home/vestimy/video_blog/blog/uploads', filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    else:
        return render_template('upload.html', menu='events')


@events.route('/contact/', methods=['get', 'post'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        print(name)
        print(email)
        print(message)
        # здесь логика базы данных
        print("\nData received. Now redirecting ...")
        return redirect(url_for('contact'))

    return render_template('contact.html', menu='events', form=form)


@events.route('/events/mail', methods=['GET'])
def send_mail():
    msg = Message("Hello",
                  sender="vestimyandrey@gmail.com",
                  recipients=["dyadya_ko@mail.ru", "vestimyandrey@yandex.ru"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)
    return redirect(url_for('events.get_event'))


@events.route('/events/event_month', methods=['GET', 'POST'])
# @login_required
def get_json_event():
    event = Event.query.all()
    list_json = []

    for item in event:
        list_json.append({"date": item.date_event.strftime("%Y-%m-%d ")+item.time_event.strftime("%H:%M:%S"),
                          "title": item.artist.last_name+item.artist.first_name,
                          "description": item.description,
                          "url": url_for("events.get_item_event", id=item.id)})

    return json.dumps(list_json)


@events.route('/events/get_city_all', methods=('GET', 'POST'))
def get_city_all():
    city_id = request.form['city_id']
    item_list = Arena.query.filter_by(city_id=city_id).all()
    result_list = dict()
    for item in item_list:
        result_list[item.id] = item.name
    return json.dumps(result_list)

# docs.register(get_list, blueprint='videos')
# docs.register(update_list, blueprint='videos')
# docs.register(update_tutorial, blueprint='videos')
# docs.register(delete_list, blueprint='videos')
# # docs.register(get_video, blueprint=videos)
# ListView.register(videos, docs, '/main', 'listview')
