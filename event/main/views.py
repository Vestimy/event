from flask import Blueprint, jsonify, request
from blog import logger, session, docs
from blog.schemas import VideoSchema, UserSchema, AuthSchema
from flask_apispec import use_kwargs, marshal_with
from blog.models import Video
from flask_jwt_extended import jwt_required, get_jwt_identity
from blog.base_view import BaseView
from blog.utils import upload_file

videos = Blueprint('videos', __name__)


class ListView(BaseView):
    @marshal_with(VideoSchema(many=True))
    def get(self):
        try:
            videos = Video.get_list()
        except Exception as e:
            logger.warning(
                f'tutorials - read action failed with errors: {e}'
            )
            return {'message': str(e)}, 400
        return videos


@videos.route('/tutorials', methods=['GET'])
@jwt_required
@marshal_with(VideoSchema(many=True))
def get_list():
    try:
        user_id = get_jwt_identity()
        videos = Video.get_user_list(user_id=user_id)
    except Exception as e:
        logger.warning(
            f'user: {user_id} tutorials - read action failed with errors: {e}'
        )
        return {'message': str(e)}, 400
    return videos


@videos.route('/tutorials', methods=['POST'])
@jwt_required
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_list(**kwargs):
    # file = request.files.getlist('media[]')
    # if not file:
    #     return '', 204
    try:
        user_id = get_jwt_identity()
        video = Video(user_id=user_id, **kwargs)
        video.save()

        # upload_file(file[0], user_id, video.id)
        # if len(files) > 1:
        #     upload_file(file[1], user_id, video.id, field='cover')
    except Exception as e:
        logger.warning(f'user:{user_id} tutorials - read action failed with errors: {e}')
        return {'message': str(e)}, 400
    return video


@videos.route('/tutorials/<int:video_id>', methods=['GET'])
@marshal_with(VideoSchema)
def get_video(video_id):
    try:
        item = Video.query.get(video_id)
        if not item:
            raise Exception('No video with this id')
    except Exception as e:
        logger.warning(
            f'video:{video_id} - get action failed with errors: {e}'
        )
    return item


@videos.route('/tutorials/<int:tutorial_id>', methods=['PUT'])
@jwt_required
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_tutorial(tutorial_id, **kwargs):
    try:
        user_id = get_jwt_identity()
        item = Video.get(tutorial_id, user_id)
        item.update(**kwargs)
    except Exception as e:
        logger.warning(
            f'user:{user_id} tutorial:{tutorial_id} - update action failed with errors: {e}')
        return {'message': str(e)}, 400
    return item


@videos.route('/tutorials/<int:tutorial_id>', methods=['DELETE'])
@jwt_required
@marshal_with(VideoSchema)
def delete_list(tutorial_id):
    try:
        user_id = get_jwt_identity()
        search = Video.get(tutorial_id, user_id)
        search.delete()
    except Exception as e:
        logger.warning(f'user:{user_id} tutorials - read action failed with errors: {e}')
        return {'message': str(e)}, 400
    return '', 204


@videos.errorhandler(422)
def error_handler(err):
    headers = err.data.get('headers', None)
    messages = err.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400


docs.register(get_list, blueprint='videos')
docs.register(update_list, blueprint='videos')
docs.register(update_tutorial, blueprint='videos')
docs.register(delete_list, blueprint='videos')
# docs.register(get_video, blueprint=videos)
ListView.register(videos, docs, '/main', 'listview')
