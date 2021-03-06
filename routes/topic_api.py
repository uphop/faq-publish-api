"""Endpoints to manage FAQ topic CRUD requests"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint

# Init API blueprint
topic_api = Blueprint('topic_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return topic_api

TOPIC_STORE = {
    "8c36e86c-13b9-4102-a44f-646015dfd981": {
        'user_id': u'04cfc704-acb2-40af-a8d3-4611fab54ada',
        'question': u'What are you planning to have for a lunch?',
        'answer': u'I''d love some spaghetti bolognese.',
        'created': (datetime.today() - timedelta(1)).timestamp()
    }
}

@topic_api.route('/user/<string:_user_id>/topic', methods=['POST'])
def create_topic(_user_id):
    """Creates a new FAQ topic.
    @param _user_id: author's identifier
    @param question: post : the question to expect from requesters
    @param answer: post : the response which should be provided back to requesters
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    # Retrive and parse JSON body
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('question'):
        abort(400)
    if not data.get('answer'):
        abort(400)

    # Store new question / answer pair
    new_uuid = str(uuid.uuid4())
    topic = {
        'user_id': _user_id,
        'question': data['question'],
        'answer': data['answer'],
        'created': datetime.now().timestamp()
    }
    
    # TODO: put topic into data store
    TOPIC_STORE[new_uuid] = topic

    # HTTP 201 Created
    return jsonify({"topic_id": new_uuid}), 201

@topic_api.route('/user/<string:_user_id>/topic', methods=['GET'])
def get_topics(_user_id):
    """Return all active topics
    @param _user_id: author's identifier
    @return: 200: an array of all captured topics as a \
    flask/response object with application/json mimetype.
    """
    # TODO: retrieve topics from data store
    topics = TOPIC_STORE
    return jsonify(topics)

@topic_api.route('/user/<string:_user_id>/topic/<string:_topic_id>', methods=['GET'])
def get_record_by_id(_user_id, _topic_id):
    """Get topic by it's identifier
    @param _user_id: author's identifier
    @param _topic_id: topic identifier
    @return: 200: a topic as a flask/response object \
    with application/json mimetype.
    @raise 404: if topic is not found
    """
    # TODO: retrieve topics from data store
    if _topic_id not in TOPIC_STORE:
        abort(404)
    return jsonify(TOPIC_STORE[_topic_id])

@topic_api.route('/user/<string:_user_id>/topic/<string:_topic_id>', methods=['DELETE'])
def delete_record(_user_id, _topic_id):
    """Delete a topic record
    @param _user_id: author's identifier
    @param _topic_id: topic identifier
    @return: 204: an empty payload.
    @raise 404: if topic is not found
    """
    # TODO: remove topic from data store
    if _topic_id not in TOPIC_STORE:
        abort(404)

    del TOPIC_STORE[_topic_id]

    return '', 204