from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt import JWT, jwt_required

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('password',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('first_name',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('last_name',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('dob',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('gender',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "User already exists!"},400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': "User created successfully."}, 201

class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('password',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('first_name',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('last_name',
            type=str,
            required=True,
            help="This field cannot be blank!"
    )
    parser.add_argument('dob',
            type=str,
            required=False,
            help="This field can be blank!"
    )
    parser.add_argument('gender',
            type=str,
            required=True,
            help="This field cannot be blank!"        
    )

    @jwt_required()
    def get(self, username):
        user = UserModel.find_by_username(username)
        if user:
            return user.json()
        return {'message': "User not found!"}, 404

    def put(self, username):
        data = User.parser.parse_args()

        user = UserModel.find_by_username(username)

        if user is None:
            user = UserModel(username, **data)
        else:
            user.password = data['password']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.dob = data['dob']
            user.gender = data['gender']

        user.save_to_db()

        return user.json()

    def delete(self, username):
        user = UserModel.find_by_username(username)
        if user is None:
            return {'message': 'User not found!'}, 404
        else:
            user.delete_from_db()
            return {'message': 'User deleted!'}


class UserList(Resource):
    def get(self):
        return {'user': [user.json() for user in UserModel.query.all()]}