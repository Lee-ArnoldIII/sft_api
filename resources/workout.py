from flask_restful import Resource, reqparse
from models.workout import WorkoutModel
from flask_jwt import JWT, jwt_required

class AddWorkout(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item',
            type=str,
            required=True,
            help="This field cannot be left blank!"
    )
    parser.add_argument('wkt_type',
            type=str,
            required=True,
            help="This field cannot be left blank!"
    )
    parser.add_argument('duration',
            type=int,
            required=True,
            help="This field cannot be left blank!"
    )
    parser.add_argument('date',
            type=str,
            required=True,
            help="This field cannot be left blank!"
    )
    parser.add_argument('user_id',
            type=int,
            required=True,
            help="This field cannot be left blank!"
    )

    def post(self):
        data = AddWorkout.parser.parse_args()

        workout = WorkoutModel(**data)
        workout.save_to_db()

        return {'message': "Workout created succefully."}, 201


class Workout(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('wkt_type',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('duration',
            type=int,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('date',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('user_id',
            type=int,
            required=True,
            help="This field cannot be blank!"
    )

    def get(self, item):
        workout = WorkoutModel.find_by_item(item)

        if workout:
            return workout.json()
        return {'message': "No workout found!"}, 404

    def put(self, item):
        data = Workout.parser.parse_args()

        workout = WorkoutModel.find_by_item(item)

        if workout is None:
            workout = WorkoutModel(item, **data)
        else:
            workout.wkt_type = data['wkt_type']
            workout.duration = data['duration']
            workout.date = data['date']
            workout.user_id = data['user_id']

        workout.save_to_db()

        return workout.json()

    def delete(self, item):
        workout = WorkoutModel.find_by_item(item)
        if workout is None:
            return {'message': 'Workout not found!'}, 404
        else:
            workout.delete_from_db()
            return {'message': 'Workout deleted!'}


class WorkoutList(Resource):
    def get(self):
        return {'workout': [workout.json() for workout in WorkoutModel.query.all()]}
