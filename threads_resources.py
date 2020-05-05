from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.threads import Thread
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('password', required=True)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('user_id', required=True, type=int)
delete_parser.add_argument('password', required=True)


def abort_if_not_found(thread_id):
    session = db_session.create_session()
    thread = session.query(Thread).get(thread_id)
    if not thread:
        abort(404, message=f"Thread {thread_id} not found")


class ThreadResource(Resource):
    def get(self, thread_id):
        abort_if_not_found(thread_id)
        session = db_session.create_session()
        thread = session.query(Thread).get(thread_id)
        return jsonify({'thread': thread.to_dict(
            only=('title', 'user_id', 'like_count', 'view_count', 'comment_count'))})

    def delete(self, thread_id):
        abort_if_not_found(thread_id)
        args = delete_parser.parse_args()
        session = db_session.create_session()
        thread = session.query(Thread).get(thread_id)
        user = session.query(User).filter(User.id == args['user_id']).first()
        if user.check_password(args['password']):
            session.delete(thread)
            session.commit()
            return jsonify({'success': 'OK'})


class ThreadListResource(Resource):
    def get(self):
        session = db_session.create_session()
        threads = session.query(Thread).all()
        return jsonify({'threads': [item.to_dict(
            only=('title', 'user.name')) for item in threads]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).filter(User.id == args['user_id']).first()
        if user.check_password(args['password']):
            thread = Thread()
            thread.title = args['title']
            thread.user_id = args['user_id']
            thread.like_count = 0
            thread.view_count = 0
            thread.comment_count = 0
            session.add(thread)
            session.commit()
            return jsonify({'success': 'OK'})