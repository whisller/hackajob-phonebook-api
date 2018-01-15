import os

from flask import Flask, jsonify, g, request
from hackajob_phone_book_api import database
from hackajob_phone_book_api.auth import auth
from hackajob_phone_book_api.exceptions import AppException
from hackajob_phone_book_api.repositories import EntryRepository

app = Flask(__name__, instance_path=os.path.dirname(os.path.abspath(__file__)))

if os.environ.get('SENTRY'):
    from raven.contrib.flask import Sentry

    sentry = Sentry(app, dsn=os.environ.get('SENTRY'))


@app.route('/entries', methods=['POST'])
@auth.login_required
def post():
    model = request.get_json(force=True, silent=True)
    if not model:
        return jsonify({'err': 'Please provide payload'}), 400

    return jsonify(EntryRepository.create_one(model))


@app.route('/entries/<entry_id>', methods=['GET'])
@auth.login_required
def get(entry_id):
    return jsonify(EntryRepository.get_one(entry_id))


@app.route('/entries/<entry_id>', methods=['DELETE'])
@auth.login_required
def delete(entry_id):
    EntryRepository.delete_one(entry_id)
    return '', 200


@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.errorhandler(AppException)
def handle_errors(error):
    response = jsonify({'err': error.message})
    response.status_code = error.status_code
    return response


def main():
    with app.app_context():
        app.run('0.0.0.0', 8080, bool(int(os.environ.get('DEBUG', 0))))


if __name__ == '__main__':
    main()
