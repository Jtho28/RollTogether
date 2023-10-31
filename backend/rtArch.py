from dataclasses import dataclass
from flask import Flask, request, url_for, render_template, jsonify
from flask_restful import Resource, Api
from datetime import datetime
from markupsafe import escape
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import CheckConstraint
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rollt.db'
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
db = SQLAlchemy(app)
admin = Admin(app, name='RollTogether')

class Rider(db.Model):
  __tablename__ = "rider"

  rider_id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(80), nullable=False)
  last_initial = db.Column(db.String(4), nullable=False)
  safety_coef = db.Column(db.Integer, nullable = False, default=6)
  rider_rating = db.Column(db.Integer, nullable = True)
  driver = db.relationship('Driver', backref='rider', uselist=False)
  __table_args__ = (
    CheckConstraint('safety_coef>=1 AND safety_coef<=10', name='safety_coef_ckeck'),
    CheckConstraint('rider_rating>=1 AND rider_rating<=5', name='rating_check')
  )

  def __repr__(self):
    return '<%r>' % self.first_name + self.last_initial

  def serialize(self):
    """Return object in json-friendly format"""
    return {
      'rider_id'    : self.rider_id,
      'first_name'  : self.first_name,
      'last_initial': self.last_initial,
      'safety_coef' : self.safety_coef,
      'rider_rating': self.rider_rating
    }

class Driver(db.Model):
  __tablename__ = "driver"

  driver_id = db.Column(db.Integer, primary_key=True)
  rider_id = db.Column(db.Integer, db.ForeignKey('rider.rider_id'), nullable=False, unique=True)
  driver_rating = db.Column(db.Integer, nullable = True)
  __table_args__ = (
    CheckConstraint('driver_rating>=1 AND driver_rating<=10', name='driver_rating_check'),
  )

  def __repr__(self):
    return '<%r>' % self.driver_id

class DriverVehicles(db.Model):
  vin_num = db.Column(db.String(100), primary_key=True)
  plate_num = db.Column(db.String(20), primary_key=True)
  driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'), nullable=False)
  model = db.Column(db.String(80), nullable=False)
  make = db.Column(db.String(80), nullable=False)
  num_seats = db.Column(db.Integer, default = 4, nullable=False)
  year = db.Column(db.Integer, nullable=False)
  miles = db.Column(db.Float, nullable=False)

  def __repr__(self):
    return '<%r>' % f"{self.driver_id}'s {self.year} {self.make} {self.model}"

@dataclass
class RideRequest(db.Model):
  r_req_id: int
  rider_id: int
  departure_locX: float
  departure_locY: float
  arrival_locX: float
  arrival_locY: float
  request_time: datetime
  pick_up_by: datetime

  r_req_id = db.Column(db.Integer, primary_key=True)
  rider_id = db.Column(db.Integer, db.ForeignKey('rider.rider_id'))
  departure_locX = db.Column(db.Float, nullable=False)
  departure_locY = db.Column(db.Float, nullable=False)
  arrival_locX = db.Column(db.Float, nullable=False)
  arrival_locY = db.Column(db.Float, nullable=False)
  request_time = db.Column(db.DateTime, nullable=False)
  pick_up_by = db.Column(db.DateTime, nullable=False)
  __table_args__ = (
    CheckConstraint('departure_locX>=-180.00 AND departure_locX<=180.00 AND arrival_locX>=-180.00 AND arrival_locX<=180.00'),
    CheckConstraint('departure_locY>=-90.00 AND departure_locY<=90 AND arrival_locY>=-90.00 AND arrival_locY<=90.00')
  )

class RidePost(db.Model):
  r_post_id = db.Column(db.Integer, primary_key=True)
  driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'))
  current_locX = db.Column(db.Float, nullable=False)
  current_locY = db.Column(db.Float, nullable=False)
  arrival_locX = db.Column(db.Float, nullable=False)
  arrival_locY = db.Column(db.Float, nullable=False)
  post_time = db.Column(db.DateTime, nullable=False)
  __table_args__ = (
    CheckConstraint('current_locX>=-180.00 AND current_locX<=180.00 AND arrival_locX>=-180.00 AND arrival_locX<=180.00'),
    CheckConstraint('current_locY>=-90.00 AND current_locY<=90 AND arrival_locY>=-90.00 AND arrival_locY<=90.00')
  )

# class DriveOffer():

class DriverModelView(ModelView):
  column_display_pk = True
  form_columns = ('rider_id', 'driver_rating')

class RiderModelView(ModelView):
  column_display_pk = True
  form_columns = ('first_name', 'last_initial', 'safety_coef', 'rider_rating')

class VehiclesModelView(ModelView):
  column_display_pk = True
  form_columns = ('vin_num', 'plate_num', 'driver_id', 'model', 'make', 'num_seats', 'year', 'miles')

class RideRequestModelView(ModelView):
  column_display_pk = True
  form_columns = ('rider_id', 'departure_locX', 'departure_locY', 'arrival_locX', 'arrival_locY', 
                  'request_time', 'pick_up_by')

class RidePostModelView(ModelView):
  column_display_pk = True
  form_columns = ('driver_id', 'current_locX', 'current_locY', 'arrival_locX', 'arrival_locY', 'post_time')

with app.app_context():
  db.create_all()

admin.add_view(RiderModelView(Rider, db.session))
admin.add_view(DriverModelView(Driver, db.session))
admin.add_view(VehiclesModelView(DriverVehicles, db.session))
admin.add_view(RideRequestModelView(RideRequest, db.session))
admin.add_view(RidePostModelView(RidePost, db.session))

@app.route('/rides')
def ride_requests():
  ride_requests = RideRequest.query.all()
  return render_template('ride_requests.html', ride_requests=ride_requests)

@app.route('/drives')
def ride_posts():
  ride_posts = RidePost.query.all()
  return render_template('ride_posts.html', ride_posts=ride_posts)

@app.route('/api/rides', methods=['GET'])
def serve_rides():
  if (request.method == 'GET'):

    rides = RideRequest.query.all()
    return jsonify(rides)

class rideRequests(Resource):
  def get


  # app.run(debug=True)

