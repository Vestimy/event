from flask import Blueprint, jsonify, request, render_template, redirect
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
from flask_security import login_required, roles_required, current_user, login_user
from event.forms import *

tours = Blueprint('tours', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

UPLOAD_FOLDER = 'uploads'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @jwt_required
# @marshal_with(VideoSchema(many=True))
@tours.route('/tour/', methods=['GET'])
def get_tour():
    try:
        tour = Tour.query.order_by('name').all()
        # event = Event.query.order_by(Event.date_event)
    except Exception as e:
        logger.warning(
            f'user: {current_user} tours - read action failed with errors: {e}'
        )
        # return {'message': str(e)}, 400
    return render_template('tour/get_tour.html', menu='tours', tours=tour)


@tours.route('/tour/<int:id>', methods=['GET'])
def get_item_tour(id):
    try:
        tour = Tour.query.get(id)
    except Exception as e:
        logger.warning(
            f'user: {user_id} tutorials - read action failed with errors: {e}'
        )
        return {'message': str(e)}, 400
    return render_template('tour/item_tour.html', menu='tours', item=tour)


@tours.route('/tour/add', methods=['GET', 'POST'])
def add_tour():
    form = TourForm()
    if request.method == "POST":
        try:
            # name = request.form['name']
            # artist_id = request.form['artist_id']
            # date_event = request.form['date_event']
            # description = request.form['description']
            # city_id = request.form['city_id']
            # arena_id = request.form['arena_id']
            # manager_id = request.form['manager_id']
            # print(date_event)
            name = request.form['name']
            print(request.form.getlist('event_id'))
            tour = Tour(name=name)
            db.session.add(tour)
            db.session.commit()
            print(tour.id)
            for i in request.form.getlist('event_id'):
                tour.event.append(Event.query.get(i))

            db.session.commit()




            # for i in request.form:

            # event = Tour(name=name,
            #               artist_id=artist_id,
            #               date_event=date_event,
            #               description=description,
            #               city_id=city_id,
            #               arena_id=arena_id,
            #               manager_id=manager_id
            #               )
            # print(request.form)
            #
            # db.session.add(event)
            # db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    # form.artist_id.choices = [(g.id, g.name) for g in Artist.query.order_by('name')]
    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    # form.arena_id.choices = [(g.id, g.name) for g in Arena.query.order_by('name')]
    # form.manager_id.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]
    # form..choices = [(g.id, g.name) for g in City.query.order_by('name')]
    # form.managers.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]
    # form.event_id.choices = [(g.id, g.title) for g in Event.query.order_by('name')]
    return render_template('tour/add_tour.html', form=form)


@tours.route('/tour/edit/<int:id>', methods=['GET', 'POST'])
def edit_tour(id):
    tour = Tour.query.get(id)
    form = TourForm(obj=tour)
    if tour is None:
        raise Exception('Ошибка нет такого поста')
    if request.method == 'POST':
        form = EventForm(formdata=request.form, obj=tour)
        form.populate_obj(tour)
        db.session.commit()

        return redirect(url_for('tours.get_item_tour', menu='tours', id=tour.id))
    # form.event.choices = [(g.id, g.artist) for g in Event.query.order_by('artist_id')]
    # form.artist_id.choices = [(g.id, g.name) for g in Artist.query.order_by('name')]
    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    # form.arena_id.choices = [(g.id, g.name) for g in Arena.query.order_by('name')]
    # form.manager_id.choices = [(g.id, g.name) for g in Manager.query.order_by('name')]

    return render_template('tour/edit_tour.html', menu='tours', form=form)


@tours.route('/tour/delete/<int:id>', methods=['GET'])
def delete_tour(id):
    event = Event.query.get(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('tours.get_tour'))


@tours.route('/upload', methods=['GET', 'POST'])
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



