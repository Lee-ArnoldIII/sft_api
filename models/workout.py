from db import db

class WorkoutModel(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80))
    workout_type = db.Column(db.String(255))
    workout_length = db.Column(db.Integer)
    workout_date = db.Column(db.DateTime())
    
    user_id = db.Column(db.String(80), db.ForeignKey('users.id'))
    users = db.relationship('UserModel')

    def __init__(self, item, workout_type, workout_length, workout_date, user_id):
        self.item = item
        self.workout_type = workout_type
        self.workout_length = workout_length
        self.workout_date = workout_date
        self.user_id = user_id
    
    def json(self):
        return {'item': self.item, 'workout_type': self.workout_type,
                'workout_lenght': self.workout_length, 'workout_date': self.workout_date
                'user': self.user_id}

    ## TODO: Determine if the json2 function will be need for something important
    def json2(self):
        pass

    @classmethod
    def find_by_item(cls, item):
        return cls.query.filter_by(item=item).all()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(workout_date=date).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()