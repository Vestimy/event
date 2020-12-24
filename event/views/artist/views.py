import os
from flask import Blueprint, jsonify, request, render_template, redirect
from event import logger, config, allowed_photo_profile
from flask import flash, request, redirect, url_for
from flask_security import login_required, roles_required, current_user
from event.forms import *
from werkzeug.utils import secure_filename

artists = Blueprint('artists', __name__)


@artists.route('/artist/', methods=['get', 'post'])
@login_required
def get_artist():
    artist = Artist.query.order_by(Artist.last_name).all()
    return render_template('artist/get_artist.html', menu='artists', artist=artist)


@artists.route('/artist/<int:id>', methods=['GET'])
@login_required
def get_item_artist(id):
    artist = Artist.query.get(id)
    return render_template('artist/item_artist.html', menu='artists', item=artist)


@artists.route('/artist/add', methods=['GET', 'POST'])
@login_required
def add_artist():
    artist = Artist()
    form = ArtistForm(request.form, obj=artist)
    if request.method == 'POST' and form.validate():
        if request.files['img']:
            file = request.files['img']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            try:
                if file and allowed_photo_profile(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(config.Config.UPLOAD_PHOTO_ARTIST, filename))
                    form.populate_obj(artist)
                    db.session.add(artist)
                    db.session.commit()
                    artist.img = filename
                    db.session.commit()
                return redirect(url_for('artists.get_artist'))
            except Exception as e:
                db.session.rollback()
                logger.warning(
                    f"{filename}-Ошибка файла: {e}"
                )
                return 404
        try:
            form.populate_obj(artist)
            db.session.add(artist)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.warning(
                f'{e}'
            )
            return redirect(url_for('artists.get_artist'))
        return redirect(url_for('artists.get_artist'))
    return render_template('artist/add_artist.html', menu='artists', form=form)


@artists.route('/artist/edit/<int:id>', methods=['get', 'post'])
@login_required
def edit_artist(id):
    artist = Artist.query.get(id)
    form = ArtistForm(request.form, obj=artist)
    if request.method == 'POST':
        if request.files['img']:
            file = request.files['img']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            try:
                if file and allowed_photo_profile(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(config.Config.UPLOAD_PHOTO_ARTIST, filename))
            except Exception as e:
                logger.warning(
                    f"{filename}-Ошибка файла: {e}"
                )
                return 404
        if artist.last_name == form.last_name.data:
            form.populate_obj(artist)
        elif form.validate():
            form.populate_obj(artist)
        else:
            return render_template('artist/edit_artist.html', menu='artists', item=artist, form=form)
        if request.files['img']:
            artist.img = filename

        db.session.commit()
        return redirect(url_for("artists.get_item_artist", id=artist.id))
        # return redirect(url_for('arenas.get_list_arena'))
    return render_template('artist/edit_artist.html', menu='artists', item=artist, form=form)


@artists.route('/artists/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required("admin")
def delete_artist(id):
    artist = Artist.query.get(id)
    db.session.delete(artist)
    db.session.commit()
    return redirect(url_for('artists.get_artist'))


@artists.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
