"""Endpoints to manage FAQ topic CRUD requests"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
from data.data_store import DataStore

# Init API blueprint
users_api = Blueprint('users_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return users_api

USER_STORE = {
    "8c36e86c-13b9-4102-a44f-646015dfd981": {
        'name': u'John Smith',
        'created': (datetime.today() - timedelta(1)).timestamp()
    }
}

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
    data_store = DataStore()
    user_id = data_store.create_user(data['name'])

    # HTTP 201 Created
    return jsonify({"user_id": user_id}), 201

@users_api.route('/user', methods=['GET'])
def get_users():
    """Return all active users
    @return: 200: an array of all active users as a \
    flask/response object with application/json mimetype.
    """
    # TODO: retrieve users from data store
    users = USER_STORE
    return jsonify(users)

@users_api.route('/user/<string:_user_id>', methods=['GET'])
def get_record_by_id(_user_id):
    """Get user by identifier
    @param _user_id: author's identifier
    @return: 200: a user as a flask/response object \
    with application/json mimetype.
    @raise 404: if user is not found
    """
    # TODO: retrieve users from data store
    if _user_id not in USER_STORE:
        abort(404)
    return jsonify(USER_STORE[_user_id])

@users_api.route('/user/<string:_user_id>', methods=['DELETE'])
def delete_record(_user_id):
    """Delete a user record
    @param _user_id: author's identifier
    @return: 204: an empty payload.
    @raise 404: if user is not found
    """
    # TODO: remove user from data store
    if _user_id not in USER_STORE:
        abort(404)

    del USER_STORE[_user_id]
    return '', 204