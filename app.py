from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from db import db

from security import authenticate, identity
from resources.user import UserRegister, UserList, User
from resources.workout import AddWorkout, WorkoutList, Workout
# from resources.meal import AddMeal, MealList, Meal

# TODO: Figure out how to set up a postgres server for instead of a sqlite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/sft_api'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# TODO: Turn this on when connected to FE
# config = {
#     'ORIGINS': [
#         'http://localhost:3000', # React
#     ],

#     'SECRET_KEY': '...'
# }

app.secret_key = 'lee'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

# TODO: create all the routes below
api.add_resource(UserRegister, '/register')
api.add_resource(AddWorkout, '/addwrkt')


api.add_resource(UserList, '/users')
api.add_resource(User, '/user/<string:username>')

# TODO: Determine if ^ will need to change and in what way if so

# api.add_resource(MealList, '/meals')
# api.add_resource(AddMeal, '/addmeal')
# api.add_resource(Meal, '/meal/<string:name>')
# TODO: Determine if ^ will need to change and in what way if so

api.add_resource(WorkoutList, '/workouts')
api.add_resource(Workout, '/workout/<string:item>')
# TODO: Determine if ^ will need to change and in what way if so


# TODO: Turn this on when you set up the FE
## CORS(app, resources={r'/.*': {'origins': config['ORIGINS']}}, supports_credentials=True)

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)