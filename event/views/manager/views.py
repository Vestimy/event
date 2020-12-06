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

from event.forms import *

managers = Blueprint('managers', __name__)

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = 'static'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@managers.route('/manager/', methods=['GET'])
def get_list_manager():
    manager = Manager.query.order_by('name').all()
    return render_template('manager/get_manager.html', menu='managers', managers=manager)


@managers.route('/manager/<int:id>', methods=['GET'])
def get_item_manager(id):
    manager = Manager.query.get(id)
    return render_template('manager/item_manager.html', menu='managers', item=manager)


@managers.route('/manager/add', methods=['GET', 'POST'])
def add_manager():
    form = ManagerForm()
    # form.city_id.choices = ArenaForm.city_choices()
    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    if request.method == 'POST':

        # print(request.form)
        arena = Manager(name=request.form['name'],
                      phone=request.form['phone']
                      )

        try:
            db.session.add(arena)
            db.session.commit()

        except Exception as e:
            db.session.rollback()

        return redirect(url_for('arenas.get_list_arena'))

    return render_template('manager/add_manager.html', menu='managers', form=form)


@managers.route('/manager/delete/<int:id>', methods=['GET'])
def delete_manager(id):
    arena = Manager.query.get(id)
    db.session.delete(arena)
    db.session.commit()
    return redirect(url_for('managers.get_list_manager'))


@managers.route('/manager/edit/<int:id>', methods=['GET', 'POST'])
def edit_manager(id):
    manager = Manager.query.get(id)
    form = ManagerForm(request.form, obj=manager)
    if request.method == 'POST':
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        print(request.form)
        form.populate_obj(manager)
        db.session.commit()
        return redirect(url_for('managers.get_list_manager'))

    # form.city_id.choices = [(g.id, g.name) for g in City.query.order_by('name')]
    return render_template('manager/edit_manager.html', menu='managers', item=manager, form=form)


@managers.route('/arena/img_add', methods=['GET', 'POST'])
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
            item = ImgArena(url=filename)
            db.session.add(item)
            db.session.commit()
            file.save(os.path.join('/home/vestimy/project/python/event/event/static', filename))
            return redirect(url_for('arenas.arena_img_upload',
                                    filename=filename))

    else:
        return render_template('upload.html', menu='arenas')

@managers.route('/manager/add', methods=['POST'])
def add_photo_manager():
    form = request.form
    print(form)


@managers.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
