from flask_restful import Resource, reqparse
from models.workout import WorkoutModel
from flask_jwt import JWT, jwt_required

class AddWorkout(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item', 
            type=str, 
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('workout_type', 
            type=str, 
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('workout_length', 
            type=str, 
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('workout_date', 
            type=str, 
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('user_id', 
            type=str, 
            required=True,
            help="This field cannot be blank!"
    )
    

    def post(self):
        data = AddWorkout.parser.parse_args()

        workout = WorkoutModel(**data)
        workout.save_to_db()

        return {'message': 'Workout successfully created!'}, 201


class Workout(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item', 
            type=str, 
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('workout_type', 
            type=str, 
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('workout_length', 
            type=str, 
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('workout_date', 
            type=str, 
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('user_id', 
            type=str, 
            required=True,
            help="This field cannot be blank!"
    )
        
    @jwt_required
    def get(self, date):
        workout = WorkoutModel.find_by_date(date)
        if workout:
            return workout.json()
        return {'message': 'Workout not found!'}, 404
    
    def put(self, date):
        data = Workout.parser.parse_args()

        workout = WorkoutModel.find_by_date(date)

        if workout is None:
            workout = WorkoutModel(date, **data)
        else:
            workout.item = data['item']
            workout.workout_type = data['workout_type']
            workout.workout_length = data['workout_length']
            workout.workout_date = date
            workout.user_id = data['user_id']
            
        workout.save_to_db()

        return workout.json()

    def delete(self, date):
        workout = WorkoutModel.find_by_date(date)
        if workout is None:
            return {'message': 'Workout not found!'}, 404
        else:
            workout.delete_from_db()
            return {'message': 'User deleted!'}


class WorkoutList(Resource):
    def get(self):
        return {'workouts': [workout.json() for workout in WorkoutModel.query.all()]}