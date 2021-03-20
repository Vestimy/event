from flask import Blueprint, jsonify, request, abort, json, render_template
from event import logger, config, weather
from werkzeug.utils import secure_filename
from event import logger, config
from event.models import *
from event.model.city import *
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_mail import Message
from flask_security import login_required, current_user, roles_required, roles_accepted
from event.forms import *
from datetime import datetime
events = Blueprint('events', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

UPLOAD_FOLDER = 'uploads'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@events.route('/event', methods=['GET'])
@login_required
def index():
    company_id = current_user.settings.company_default_id
    type_event = TypeEvent.query.order_by('name').all()
    id = None
    if request.args.get('q'):
        event = Event.query.join(Arena).join(City).join(Artist).filter(Event.company_id == company_id).filter(
            Arena.name.contains(
                request.args.get('q')) | Event.date_event.contains(
                request.args.get('q')) | Event.time_event.contains(
                request.args.get('q')) | Arena.alias.contains(
                request.args.get('q')) | Artist.last_name.contains(
                request.args.get('q')) | Artist.alias.contains(
                request.args.get('q')) | Artist.first_name.contains(
                request.args.get('q')) | City.name.contains(
                request.args.get('q'))).all()
    else:

        if request.args.get('id'):
            event = Event.query.get_or_404(request.args.get('id'))
            return render_template('event.html', id=id, menu='events', events=event, type_event=type_event)
        try:
            event = Event.query.filter(Event.company_id == company_id).filter(Event.date_event >= datetime.now().date()).order_by(Event.date_event.desc())
            if request.args.get('all'):
                try:
                    id = str(request.args.get('all'))
                except Exception as e:
                    logger.warning(
                        f'arenas -  action failed with errors: {e}'
                    )
                if isinstance(id, str):
                    event = Event.query.filter(Event.company_id == company_id).order_by(Event.date_event.desc())
            if request.args.get('type'):
                try:
                    id = int(request.args.get('type'))
                except Exception as e:
                    logger.warning(
                        f'arenas -  action failed with errors: {e}'
                    )
                if isinstance(id, int):
                    event = Event.query.filter(Event.company_id == company_id).filter(Event.typeevent_id == id).order_by(
                        Event.date_event.desc()).all()

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
                event = Event.query.filter(Event.typeevent_id == id).order_by(
                    Event.date_event.desc()).all()
    return render_template('event.html', id=id, menu='events', events=event, type_event=type_event)


@events.route('/event/<int:id>', methods=['GET'])
@login_required
def detail(id):
    data = None
    event = Event.query.get_or_404(id)
    arena = Arena.query.get(event.arena_id)
    if event.city:
        name = event.city.name
        if '(' in name:
            name = name.split('(')[0].strip()
        try:
            data = weather.get(q=name)
        except Exception:
            pass
            data = None
    return render_template('event_detail.html', menu='events', event=event, weathers=data, arena=arena)


@events.route('/add_event/', methods=['GET', 'POST'])
@login_required
# @roles_accepted('admin ', 'manager')
def add():
    default_id = current_user.settings.company_default_id
    event = Event()
    form = EventForm(request.form, obj=event)
    if request.method == "POST":
        try:
            form.populate_obj(event)
            db.session.add(event)
            event.company_id = default_id
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

    form.users_staffs.choices = [(g.id, g) for g in
                                 User.query.filter(
                                     User.company.any(
                                         Company.id.in_(
                                             [current_user.settings.company_default_id]
                                         )
                                     )
                                 )
                                 ]
    return render_template('event_add.html', menu='events', form=form)


@events.route('/events/edit/<int:id>', methods=['GET', 'POST'])
@login_required
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
@login_required
def delete(id):
    event = Event.query.get(id)
    if current_user.id == event.user_id or "admin" in current_user.roles:
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('events.get_event'))


@events.route('/upload', methods=['GET', 'POST'])
@login_required
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
            file.save(os.path.join(
                '/home/vestimy/video_blog/blog/uploads', filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    else:
        return render_template('upload.html', menu='events')

