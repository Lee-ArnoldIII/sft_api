from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    dob = db.Column(db.Text)
    gender = db.Column(db.String(80))

    workouts = db.relationship('WorkoutModel', lazy='dynamic')

    def __init__(self, username, password, first_name, last_name, dob, gender):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender

    def json(self):
        return {'user': self.id, 'username': self.username, 'first_name': self.first_name,
                'last_name': self.last_name, 'dob': self.dob, 'gender': self.gender}

    ## TODO: Determine if the json2 function will be need for something important
    def json2(self):
        pass

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()