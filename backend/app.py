from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from models import setup_db, Swimmer, Meet, Result
from auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/')
def get_greeting():
    greeting = "Hello World"
    return greeting


@app.route('/swimmers', methods=['GET'])
@requires_auth('get:swimmers')
def get_swimmers(payload):
    swimmers = Swimmer.query.all()

    response = {
        'success': True,
        'swimmers': [swimmer.format() for swimmer in swimmers]
    }
    return jsonify(response)


@app.route('/swimmers', methods=['POST'])
@requires_auth('create:swimmer')
def create_swimmer(payload):
    data = request.get_json()

    try:
        if 'id' in data and not Swimmer.query.filter(Swimmer.id == data['id']).one_or_none():
            swimmer = Swimmer(
                id=data['id'],
                gender=data['gender'],
                first_name=data['first name'],
                last_name=data['last name'],
                birth_year=data['year of birth']
            )
        else:
            swimmer = Swimmer(
                gender=data['gender'],
                first_name=data['first name'],
                last_name=data['last name'],
                birth_year=data['year of birth']
            )

        swimmer.insert()

        response = {
            'success': True,
            'id': swimmer.id
        }
        return jsonify(response)
    except:
        abort(400)


@app.route('/swimmers/<int:swimmer_id>', methods=['GET'])
@requires_auth('get:swimmer-details')
def get_swimmer_details(payload, swimmer_id):
    swimmer = Swimmer.query.filter(Swimmer.id == swimmer_id).one_or_none()

    if not swimmer:
        abort(404)

    response = {
        'success': True,
        'swimmer': swimmer.format()
    }
    return jsonify(response)


@app.route('/swimmers/<int:swimmer_id>/results', methods=['GET'])
@requires_auth('get:swimmer-results')
def get_swimmer_results(payload, swimmer_id):
    swimmer = Swimmer.query.filter(Swimmer.id == swimmer_id).one_or_none()

    if not swimmer:
        abort(404)

    response = {
        'success': True,
        'results': [result.format() for result in swimmer.results]
    }
    return jsonify(response)


@app.route('/swimmers/<int:swimmer_id>', methods=['PATCH'])
@requires_auth('edit:swimmer')
def edit_swimmer(payload, swimmer_id):
    swimmer = Swimmer.query.filter(Swimmer.id == swimmer_id).one_or_none()

    if not swimmer:
        abort(404)

    data = request.get_json()

    try:
        if 'gender' in data:
            swimmer.gender = data['gender']
        if 'first name' in data:
            swimmer.first_name = data['first name']
        if 'last name' in data:
            swimmer.gender = data['last name']
        if 'year of birth' in data:
            swimmer.birth_year = data['year of birth']

        swimmer.update()

        response = {
            'success': True,
            'swimmer': swimmer.format()
        }
        return jsonify(response)
    except:
        abort(400)


@app.route('/swimmers/<int:swimmer_id>', methods=['DELETE'])
@requires_auth('delete:swimmer')
def delete_swimmer(payload, swimmer_id):
    swimmer = Swimmer.query.filter(Swimmer.id == swimmer_id).one_or_none()

    if not swimmer:
        abort(404)

    swimmer.delete()

    response = {
        'success': True,
        'id': swimmer_id
    }
    return jsonify(response)


@app.route('/meets', methods=['GET'])
@requires_auth('get:meets')
def get_meets(payload):
    meets = Meet.query.all()

    response = {
        'success': True,
        'meets': [meet.format() for meet in meets]
    }
    return jsonify(response)


@app.route('/meets', methods=['POST'])
@requires_auth('create:meet')
def create_meet(payload):
    data = request.get_json()

    try:
        meet = Meet(
            name=data['name'],
            start_date=data['start date'],
            end_date=data['end date'],
            city=data['city'],
            country=data['country']
        )

        meet.insert()

        response = {
            'success': True,
            'id': meet.id
        }
        return jsonify(response)
    except:
        abort(400)


@app.route('/meets/<int:meet_id>', methods=['GET'])
@requires_auth('get:meet-details')
def get_meet_details(payload, meet_id):
    meet = Meet.query.filter(Meet.id == meet_id).one_or_none()

    if not meet:
        abort(404)

    response = {
        'success': True,
        'meet': meet.format()
    }
    return jsonify(response)


@app.route('/meets/<int:meet_id>/results', methods=['GET'])
@requires_auth('get:meet-results')
def get_meet_results(payload, meet_id):
    meet = Meet.query.filter(Meet.id == meet_id).one_or_none()

    if not meet:
        abort(404)

    response = {
        'success': True,
        'results': [result.format() for result in meet.results]
    }
    return jsonify(response)


@app.route('/meets/<int:meet_id>', methods=['PATCH'])
@requires_auth('edit:meet')
def edit_meet(payload, meet_id):
    meet = Meet.query.filter(Meet.id == meet_id).one_or_none()

    if not meet:
        abort(404)

    data = request.get_json()

    try:
        if 'name' in data:
            meet.name = data['name']
        if 'start date' in data:
            meet.start_date = data['start date']
        if 'end date' in data:
            meet.end_date = data['end date']
        if 'city' in data:
            meet.city = data['city']
        if 'country' in data:
            meet.country = data['country']

        meet.update()

        response = {
            'success': True,
            'meet': meet.format()
        }
        return jsonify(response)
    except:
        abort(400)


@app.route('/meets/<int:meet_id>', methods=['DELETE'])
@requires_auth('delete:meet')
def delete_meet(payload, meet_id):
    meet = Meet.query.filter(Meet.id == meet_id).one_or_none()

    if not meet:
        abort(404)

    meet.delete()

    response = {
        'success': True,
        'id': meet_id
    }
    return jsonify(response)


@app.route('/results', methods=['GET'])
@requires_auth('get:results')
def get_results(payload):
    results = Result.query.all()

    response = {
        'success': True,
        'meets': [result.format() for result in results]
    }
    return jsonify(response)


'''
Error handling
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
    }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable entity"
    }), 422


if __name__ == '__main__':
    app.run()
