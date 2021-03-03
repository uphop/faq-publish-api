"""Endpoints to manage FAQ users CRUD requests"""
from flask import jsonify, abort, request, Blueprint
from domain.user_manager import UserManager

# Init API blueprint
users_api = Blueprint('users_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return users_api


@users_api.route('/user', methods=['POST'])
def create_user():
    """Creates a new FAQ author.
    @param name: post : the full author's name
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    # Retrive and parse JSON body
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('name'):
        abort(400)

    # Store new user
    user_id = UserManager().create_user(data['name'])

    # HTTP 201 Created
    return jsonify({"user_id": user_id}), 201


@users_api.route('/user', methods=['GET'])
def get_users():
    """Return all active users
    @return: 200: an array of all active users as a \
    flask/response object with application/json mimetype.
    """
    # Retrieve users from data store
    users = UserManager().get_users()

    return jsonify(users)


@users_api.route('/user/<string:_user_id>', methods=['GET'])
def get_record_by_id(_user_id):
    """Get user by identifier
    @param _user_id: author's identifier
    @return: 200: a user as a flask/response object \
    with application/json mimetype.
    @raise 404: if user is not found
    """
    # Retrieve user from data store
    user = UserManager().get_user(_user_id)

    # HTTP 404 Not Found
    if user is None:
        abort(404)

    return jsonify(user)


@users_api.route('/user/<string:_user_id>', methods=['DELETE'])
def delete_record(_user_id):
    """Delete a user record
    @param _user_id: author's identifier
    @return: 204: an empty payload.
    @raise 404: if user is not found
    """
    # Remove user from data store
    deleted_id = UserManager().delete_user(_user_id)

    # HTTP 404 Not Found
    if deleted_id is None:
        abort(404)

    # HTTP 204 Deleted
    return '', 204
