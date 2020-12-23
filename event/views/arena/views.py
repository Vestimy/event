import os
from flask import Blueprint, jsonify, request, render_template, redirect
from event import logger, config, allowed_photo_profile
from flask_security import login_required, roles_required, current_user, login_user
from flask import flash, request, redirect, url_for
from event.forms import *
from werkzeug.utils import secure_filename

arenas = Blueprint('arenas', __name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = 'static'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@arenas.route('/arena', methods=['GET'])
@login_required
def get_list_arena():
    arena = Arena.query.order_by('name').all()
    typehall = TypeHall.query.order_by('name').all()
    id = None
    if request.args.get('id'):
        try:
            id = int(request.args.get('id'))
        except Exception as e:
            logger.warning(
                f'arenas -  action failed with errors: {e}'
            )
        if isinstance(id, int):
            arena = Arena.query.filter(Arena.typehall_id == id).order_by('name').all()
    return render_template('arena/get_list_arena.html', menu='arenas', id=id, typehall=typehall, arena=arena)


@arenas.route('/arena/<int:id>', methods=['GET'])
@login_required
def get_item_arena(id):
    try:
        arena = Arena.query.get(id)
    except Exception as e:
        logger.warning(
            f"{current_user.last_name} - Ошибка при загрузке всех площадок: {e}"
        )
    return render_template('arena/item_arena.html', menu='arenas', item=arena)


@arenas.route('/arena/add', methods=['GET', 'POST'])
@login_required
def add_arena():
    arena = Arena()
    form = ArenaForm(request.form, obj=arena)
    if request.method == 'POST' and form.validate():
        if request.files['img']:
            file = request.files['img']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            try:
                if file and allowed_photo_profile(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(config.Config.UPLOAD_PHOTO_ARENA, filename))
                    form.populate_obj(arena)
                    db.session.add(arena)
                    db.session.commit()
                    arena.img = filename
                    db.session.commit()
                    return redirect(url_for('arenas.get_list_arena'))
            except Exception as e:
                logger.warning(
                    f"{filename}-Ошибка файла: {e}"
                )
                return 404
        form.populate_obj(arena)
        try:
            db.session.add(arena)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.warning(
                f'{current_user.id}-{current_user.name} - Ошибка при добавлении площадки: {e}'
            )

        return redirect(url_for('arenas.get_list_arena'))

    return render_template('arena/add_arena.html', menu='arenas', form=form)


@arenas.route('/arena/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_arena(id):
    arena = Arena.query.get(id)
    form = ArenaForm(request.form, obj=arena)
    if request.method == 'POST':
        if request.files['img']:
            file = request.files['img']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            try:
                if file and allowed_photo_profile(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(config.Config.UPLOAD_PHOTO_ARENA, filename))
            except Exception as e:
                logger.warning(
                    f"{filename}-Ошибка файла: {e}"
                )
                return 404
        if arena.name == request.form['name']:
            form.populate_obj(arena)
            if request.files['img']:
                arena.img = filename
            db.session.commit()
            return redirect(url_for('arenas.get_list_arena'))
        if form.validate():
            form.populate_obj(arena)
            if request.files['img']:
                arena.img = filename
            db.session.commit()
            return redirect(url_for('arenas.get_list_arena'))

    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    return render_template('arena/edit_arena.html', menu='arenas', item=arena, form=form)


@arenas.route('/arena/delete/<int:id>', methods=['GET'])
@roles_required('admin')
def delete_arena(id):
    arena = Arena.query.get(id)
    db.session.delete(arena)
    db.session.commit()
    return redirect(url_for('arenas.get_list_arena'))


@arenas.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
