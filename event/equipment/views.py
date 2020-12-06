from flask import Blueprint, jsonify
from blog import logger, session, docs
from blog.schemas import VideoSchema, UserSchema, AuthSchema, EquimentsSchema
from flask_apispec import use_kwargs, marshal_with
# from blog.models import Equipment, Event
from flask_jwt_extended import jwt_required, get_jwt_identity
from blog.base_view import BaseView

equipments = Blueprint('equipments', __name__)


@equipments.route('/catalog', methods=['GET'])
# @jwt_required
@marshal_with(EquimentsSchema(many=True))
def get_list():
    try:
        user_id = get_jwt_identity()
        eq = Equipment.query.all()
    except Exception as e:
        logger.warning(
            f'user: {user_id} tutorials - read action failed with errors: {e}'
        )
        return {'message': str(e)}, 400
    return eq
@equipments.route('/catalog/<int:light>', methods=['GET'])
# @jwt_required
@marshal_with(EquimentsSchema(many=True))
def get_list_light(light):
    try:
        user_id = get_jwt_identity()
        eq = Equipment.query.filter(Equipment.catalogeqs_id==light).all()
    except Exception as e:
        logger.warning(
            f'user: {user_id} tutorials - read action failed with errors: {e}'
        )
        return {'message': str(e)}, 400
    return eq




@equipments.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(get_list, blueprint='equipments')
# docs.register(update_list, blueprint='videos')
# docs.register(update_tutorial, blueprint='videos')
# docs.register(delete_list, blueprint='videos')
# docs.register(get_video, blueprint=videos)
# ListView.register(videos, docs, '/main', 'listview')