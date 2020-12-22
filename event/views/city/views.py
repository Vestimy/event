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
from flask_security import current_user

from event.forms import *

citys = Blueprint('citys', __name__)


@citys.route('/city/', methods=['get', 'post'])
def get_city():
    citys = City.query.order_by(City.name)
    return render_template('city/get_city.html', menu='citys', citys=citys)


@citys.route('/city/<int:id>', methods=['GET'])
def get_city_arena(id):
    arena = Arena.query.filter(Arena.city_id == id).order_by(Arena.name).all()
    return render_template('arena/get_list_arena.html', arena=arena)


@citys.route('/city/add', methods=['get', 'post'])
def add_city():
    city = City()
    form = CityForm(request.form, obj=city)
    if request.method == 'POST' and form.validate():
        # city = City(name=request.form['name'])
        form.populate_obj(city)
        db.session.add(city)
        db.session.commit()

    return render_template('city/add_city.html', menu='citys', form=form)


@citys.route('/city/edit/<int:id>', methods=['get', 'post'])
def edit_city(id):
    try:
        city = City.query.get(id)
        form = CityForm(request.form, obj=city)
        if request.method == 'POST':
            if city.name == request.form['name']:
                form.populate_obj(city)
                db.session.commit()
                return redirect(url_for('citys.get_city'))
            if form.validate():
                form.populate_obj(city)
                db.session.commit()
                return redirect(url_for('citys.get_city'))

        return render_template('city/edit_city.html', menu='citys', form=form)
    except Exception as e:
        db.session.rollback()
        logger.warning(
            f"{current_user.id}-{current_user.name} - Ошибка в обновлении города: {e} "

        )

@citys.route('/city/delete/<int:id>', methods=['GET', 'POST'])
def delete_city(id):
    city = City.query.get(id)
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for('citys.get_city'))


@citys.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400
