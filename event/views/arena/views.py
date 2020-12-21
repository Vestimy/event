from flask import Blueprint, jsonify, request, render_template, redirect
from event import logger, config
from werkzeug.utils import secure_filename
from event import logger, config
from event.models import *
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from blog.base_view import BaseView
# from blog.utils import upload_file
from flask_security import login_required, roles_required, current_user, login_user
import os
from flask import flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from event.forms import *

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
    arena = Arena.query.get(id)
    return render_template('arena/item_arena.html', menu='arenas', item=arena)


@arenas.route('/arena/add', methods=['GET', 'POST'])
@login_required
def add_arena():
    form = ArenaForm()
    # form.city_id.choices = ArenaForm.city_choices()
    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    if request.method == 'POST':

        arena = Arena(name=request.form['name'],
                      description=request.form['description'],
                      city_id=request.form['city_id'],
                      typehall_id=request.form['typehall_id'],
                      address=request.form['address'],
                      phone_admin=request.form['phone_admin'],
                      number_of_seats=request.form['number_of_seats'],
                      hall_size=request.form['hall_size'],
                      razgruzka=request.form['razgruzka'],
                      sound=request.form['sound'],
                      phone_sound=request.form['phone_sound'],
                      light=request.form['light'],
                      phone_light=request.form['phone_light']
                      )

        try:
            db.session.add(arena)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            logger.warning(
                f'arenas - wright action failed with errors: {e}'
            )

        return redirect(url_for('arenas.get_list_arena'))

    return render_template('arena/add_arena.html', menu='arenas', form=form)


@arenas.route('/arena/delete/<int:id>', methods=['GET'])
@roles_required('admin')
def delete_arena(id):
    arena = Arena.query.get(id)
    db.session.delete(arena)
    db.session.commit()
    return redirect(url_for('arenas.get_list_arena'))


@arenas.route('/arena/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def edit_arena(id):
    arena = Arena.query.get(id)
    form = ArenaForm(request.form, obj=arena)
    if request.method == 'POST':
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        print(request.form)
        form.populate_obj(arena)
        db.session.commit()
        return redirect(url_for('arenas.get_list_arena'))

    form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    return render_template('arena/edit_arena.html', menu='arenas', item=arena, form=form)


@arenas.route('/arena/img_add', methods=['GET', 'POST'])
@login_required
def arena_img_upload():
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
            filename = 'img/arena/' + filename
            print(filename)

            item = ImgArena(url=filename)
            db.session.add(item)
            db.session.commit()
            file.save(os.path.join('/home/vestimy/project/python/event/event/static', filename))
            return redirect(url_for('arenas.arena_img_upload',
                                    filename=filename))

    else:
        return render_template('upload.html', menu='arenas')


@arenas.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
