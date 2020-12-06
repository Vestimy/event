from flask import Blueprint, jsonify, request, render_template, redirect
from event import logger, config
from werkzeug.utils import secure_filename
from event import logger, config
from event.models import *
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from blog.base_view import BaseView
# from blog.utils import upload_file
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_security import login_required, roles_required
from event.forms import *

artists = Blueprint('artists', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

UPLOAD_FOLDER = 'uploads'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@artists.route('/artist/', methods=['get', 'post'])
@login_required
# @roles_required('users')
def get_artist():
    artist = Artist.query.order_by(Artist.name).all()
    return render_template('artist/get_artist.html', menu='artists', artist=artist)


@artists.route('/artist/<int:id>', methods=['GET'])
def get_item_artist(id):
    artist = Artist.query.get(id)
    return render_template('artist/item_artist.html', menu='artists', item=artist)


@artists.route('/artists/add', methods=['get', 'post'])
def add_artist():
    form = ArtistForm()
    # form.arena.choices = [(g.id, g.name) for g in Arena.query.order_by('name')]
    if request.method == 'POST':
        try:
            artist = Artist(name=request.form['name'],
                            administrator=request.form['administrator'],
                            phone_administrator=request.form['phone_administrator'],
                            sound_engineer=request.form['sound_engineer'],
                            phone_sound=request.form['phone_sound'],
                            monitor_engineer=request.form['monitor_engineer'],
                            phone_monitor=request.form['phone_monitor'],
                            light=request.form['light'],
                            phone_light=request.form['phone_light']
                            )
            db.session.add(artist)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return redirect(url_for('artists.get_artist'))

        return redirect(url_for('artists.get_artist'))
    return render_template('artist/add_artist.html', menu='artists', form=form)


@artists.route('/artists/edit/<int:id>', methods=['get', 'post'])
def edit_artist(id):
    artist = Artist.query.get(id)
    form = ArtistForm(request.form, obj=artist)
    if artist is None:
        raise 'Ошибка в поиске'
    if request.method == 'POST':
        form.populate_obj(artist)
        db.session.commit()
        return redirect(url_for('artists.get_artist'))

    # form.arena.choices = [(g.id, g.name) for g in Arena.query.order_by('name')]
    return render_template('artist/edit_artist.html', menu='artists', item=artist, form=form)


@artists.route('/artists/delete/<int:id>', methods=['GET', 'POST'])
def delete_artist(id):
    artist = Artist.query.get(id)
    db.session.delete(artist)
    db.session.commit()
    return redirect(url_for('artists.get_artist'))


@artists.route('/artist/add_photo', methods=['GET', 'POST'])
def artist_img_upload():
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
            filename = 'img/artist/' + filename
            print(filename)

            item = PhotoArtist(url=filename)
            db.session.add(item)
            db.session.commit()
            file.save(os.path.join('/home/vestimy/project/python/event/event/static', filename))
            return redirect(url_for('artists.artist_img_upload',
                                    filename=filename))

    else:
        return render_template('artist/photo_artist_upload.html', menu='artists')


@artists.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
