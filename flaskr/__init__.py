import os
from flask import Flask, jsonify, request, abort
from models import setup_db, Plant
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    def paginate_data(request, data):
        page = request.args.get('page', 0, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        start = page * page_size
        end = start + page_size
        plants = [plant.format() for plant in data]
        return plants[start:end]

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/plants', methods=['POST'])
    def create_plant():
        body = request.get_json()

        name = body.get('name', None)
        scientific_name = body.get('scientific_name', None)
        is_poisonous = body.get('is_poisonous', None)
        primary_color = body.get('primary_color', None)
        print(name, scientific_name, is_poisonous, primary_color)

        try:
            plant = Plant(name=name, scientific_name=scientific_name,
                          is_poisonous=is_poisonous, primary_color=primary_color)
            plant.insert()

            selection = Plant.query.order_by(Plant.id).all()
            current_plants = paginate_data(request, selection)

            return jsonify({
                'success': True,
                'created': plant.id,
                'plants': current_plants,
                'total_plants': len(selection)
            })
        except:
            abort(422)

    @app.route('/plants')
    def get_plants():
        search = request.args.get('search')
        plants = []

        if search:
            plants = Plant.query.order_by(Plant.id).filter(
                Plant.name.ilike("%{}%".format(search))
            ).all()
        else:
            # plants = Plant.query.all()
            plants = Plant.query.order_by(Plant.id).all()

        return jsonify({
            'success': True,
            'plants': paginate_data(request, plants),
            'count': len(plants)
        })

    @app.route('/plants/<int:plant_id>')
    def get_plant_by_id(plant_id):
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

        if plant is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'plant': plant.format()
            })

    @app.route('/plants/<int:plant_id>', methods=['PATCH'])
    def update_plant(plant_id):
        body = request.get_json()
        try:
            plant = Plant.query.filter(Plant.id == plant_id).one_or_none()
            if plant is None:
                abort(404)

            if 'name' in body:
                plant.name = body.get('name')

            plant.update()

            return jsonify({
                'success': True,
                'id': plant.id
            })
        except:
            abort(400)

    @app.route('/plants/<int:plant_id>', methods=['DELETE'])
    def delete_plant(plant_id):
        try:
            plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

            if plant is None:
                abort(404)

            plant.delete()

            plants = Plant.query.order_by(Plant.id).all()

            return jsonify({
                'success': True,
                'deleted': plant_id,
                'plants': paginate_data(request, plants),
                'total_plants': len(plants)
            })
        except:
            abort(404)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'resource not found'
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable entity'
        }), 422

    return app
