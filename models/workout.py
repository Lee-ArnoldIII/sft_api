from db import db

class WorkoutModel(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80))
    wkt_type = db.Column(db.String(255))
    duration = db.Column(db.Integer)
    date = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship('UserModel')

    def __init__(self, item, wkt_type, duration, date, user_id):
        self.item = item
        self.wkt_type = wkt_type
        self.duration = duration
        self.date = date
        self.user_id = user_id
    
    def json(self):
        return {'item': self.item, 'wkt_type': self.wkt_type,
                'duration': self.duration, 'date': self.date,
                'user': self.user_id}

    ## TODO: Determine if the json2 function will be need for something important
    def json2(self):
        pass

    @classmethod
    def find_by_item(cls, item):
        return cls.query.filter_by(item=item).first()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(workout_date=date).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()