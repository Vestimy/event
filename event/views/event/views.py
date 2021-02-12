from flask import Blueprint, jsonify, request, abort, json, render_template, redirect
from event import logger, config
from werkzeug.utils import secure_filename
from event import logger, config
from event.models import *
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
@events.route('/event', methods=['GET'])
def index():
    type_event = TypeEvent.query.order_by('name').all()
    id = None
    if request.args.get('q'):
        event = Event.query.join(Arena).join(Artist).filter(
            Arena.name.contains(
                request.args.get('q')) | Event.date_event.contains(
                request.args.get('q')) | Event.time_event.contains(
                request.args.get('q')) | Arena.alias.contains(
                request.args.get('q')) | Artist.last_name.contains(
                request.args.get('q')) | Artist.alias.contains(
                request.args.get('q')) | Artist.first_name.contains(
                request.args.get('q'))).all()
    else:

        if request.args.get('id'):
            event = Event.query.get_or_404(request.args.get('id'))
            return render_template('event.html', id=id, menu='events', events=event, type_event=type_event)
        try:
            event = Event.query.order_by(Event.date_event.desc())
            if request.args.get('type'):
                try:
                    id = int(request.args.get('type'))
                except Exception as e:
                    logger.warning(
                        f'arenas -  action failed with errors: {e}'
                    )
                if isinstance(id, int):
                    event = Event.query.filter(Event.typeevent_id == id).order_by(Event.date_event.desc()).all()

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
                return redirect(request.url)
            if isinstance(id, int):
                event = Event.query.filter(Event.typeevent_id == id).order_by(Event.date_event.desc()).all()
    return render_template('event.html', id=id, menu='events', events=event, type_event=type_event)


@events.route('/event/<int:id>', methods=['GET'])
def detail(id):
    event = Event.query.get_or_404(id)
    return render_template('event_detail.html', menu='events', event=event)


@events.route('/add_event/', methods=['GET', 'POST'])
@roles_accepted('admin ', 'manager')
def add():
    event = Event()
    form = EventForm(request.form, obj=event)
    if request.method == "POST":
        try:
            form.populate_obj(event)
            db.session.add(event)
            db.session.commit()
            if request.form.getlist('users_staffs'):
                for i in request.form.getlist('users_staffs'):
                    event.users_staff.append(User.query.get(i))
                db.session.commit()
        except Exception as e:
            print(e)
            logger.warning(
                f'Ошибка при добавлении мерроприятия: {e}'
            )
            db.session.rollback()

    # form.artist_id.choices = [(g.id, g.name) for g in Artist.query.order_by('name')]
    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    # form.arena_id.choices = [(g.id, g.name) for g in Arena.query.order_by('name')]
    # form.manager_id.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]
    # form..choices = [(g.id, g.name) for g in City.query.order_by('name')]
    # form.managers.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]
    # form.arenas.choices = [(g.id, g.title) for g in Arena.query.order_by('title')]
    return render_template('event_add.html', menu='events', form=form)


@events.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@roles_accepted('admin', 'manager')
def edit(id):
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
def delete(id):
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

# ListView.register(videos, docs, '/main', 'listview')
