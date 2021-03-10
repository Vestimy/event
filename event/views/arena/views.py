import os
from flask import Blueprint, jsonify, request, render_template, redirect, abort
from event import logger, config, allowed_photo_profile
from flask_security import login_required, roles_required, current_user, login_user
from flask import flash, request, redirect, url_for
from event.forms import *
from werkzeug.utils import secure_filename
from event import admin_required
arenas = Blueprint('arenas', __name__)


@arenas.route('/arena/', methods=['GET'])
@login_required
def index():
    id = None
    citys = None
    if request.args.get('q'):
        arena = Arena.query.join(City).filter(
            City.name.contains(request.args.get('q')) | Arena.name.contains(request.args.get('q')) | Arena.alias.contains(request.args.get('q'))).all()
    else:
        arena = Arena.query.order_by('name').all()
        if request.args.get('type'):
            try:
                id = int(request.args.get('type'))
            except Exception as e:
                logger.warning(
                    f'arenas -  action failed with errors: {e}'
                )
            if isinstance(id, int):
                arena = Arena.query.filter(
                    Arena.typehall_id == id).order_by('name').all()
        if request.args.get('city'):
            try:
                city = int(request.args.get('city'))

            except Exception as e:
                logger.warning(
                    f'arenas -  action failed with errors: {e}'
                )
            if isinstance(city, int):
                arena = Arena.query.filter(
                    Arena.city_id == city).order_by('name').all()
                city_query = City.query.filter(City.id == city).one()
                citys = city_query.name
        if request.args.get('region'):
            try:
                region = int(request.args.get('region'))

            except Exception as e:
                logger.warning(
                    f'arenas -  action failed with errors: {e}'
                )
            if isinstance(region, int):
                arena = Arena.query.join(City).filter(City.region_id == region)

    typehall = TypeHall.query.order_by('name').all()
    return render_template('arena.html', menu='arenas', id=id, typehall=typehall, arena=arena, citys=citys)


@arenas.route('/arena/<int:id>', methods=['GET', 'POST'])
@login_required
def arena_detail(id):
    try:
        arena = Arena.query.get(id)
        if not arena:
            return redirect(request.root)
        if request.method == 'POST':
            file = request.files['file']
            print(file)
    except Exception as e:
        logger.warning(
            f"{current_user.last_name} - Ошибка при загрузке одной площадки: {e}"
        )
        return redirect(url_for('main.index'))
    return render_template('arena_detail.html', menu='arenas', arena=arena)


@arenas.route('/test/', methods=['GET', 'POST'])
@login_required
def test():
    form = TestForm()
    return render_template('test.html', form=form)


@arenas.route('/arena/add', methods=['GET', 'POST'])
@login_required
def add():
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
                    file.save(os.path.join(
                        config.Config.UPLOAD_PHOTO_ARENA, filename))
                    form.populate_obj(arena)
                    db.session.add(arena)
                    db.session.commit()
                    arena.img = filename
                    db.session.commit()
                    return redirect(url_for('arenas.arena_detail', id=arena.id))
            except Exception as e:
                logger.warning(
                    f"{filename}-Ошибка файла: {e}"
                )
                abort(404)
        form.populate_obj(arena)
        try:
            db.session.add(arena)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.warning(
                f'{current_user.id}-{current_user.last_name} - Ошибка при добавлении площадки: {e}'
            )

        return redirect(url_for('arenas.arena_detail', id=arena.id))

    return render_template('add_arena.html', menu='arenas', form=form)


@arenas.route('/arena/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    arena = Arena.query.get(id)
    form = ArenaForm(request.form, obj=arena)
    if arena.city_id:
        form.city_id.choices = [(arena.city.id, arena.city.name)]
    if request.method == 'POST':
        # if request.files['img']:
        #     file = request.files['img']
        #     if file.filename == '':
        #         flash('No selected file')
        #         return redirect(request.url)
        #     try:
        #         if file and allowed_photo_profile(file.filename):
        #             filename = secure_filename(file.filename)
        #             file.save(os.path.join(config.Config.UPLOAD_PHOTO_ARENA, filename))
        #     except Exception as e:
        #         logger.warning(
        #             f"{filename}-Ошибка файла: {e}"
        #         )
        #         return 404
        if arena.name == request.form['name']:
            form.populate_obj(arena)
            # if request.files['img']:
            #     arena.img = filename
            db.session.commit()
            return redirect(url_for('arenas.arena_detail', id=arena.id))
        if form.validate():
            form.populate_obj(arena)
            # if request.files['img']:
            #     arena.img = filename
            db.session.commit()
            return redirect(url_for('arenas.arena_detail', id=arena.id))

    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    return render_template('arena_edit.html', menu='arenas', arena=arena, form=form)


@arenas.route('/arena/delete/<int:id>', methods=['GET'])
@login_required
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
