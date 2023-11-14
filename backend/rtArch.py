from flask import Flask
from flask import url_for
from markupsafe import escape
from flask import request
from flask import render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import CheckConstraint
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rollt.db'
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
db = SQLAlchemy(app)
admin = Admin(app)

class Rider(db.Model):
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

class Driver(db.Model):
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


class RideRequest(db.Model):
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

# class DriveOffer():

with app.app_context():
  db.create_all()

admin.add_view(ModelView(Rider, db.session))
admin.add_view(ModelView(Driver, db.session))
admin.add_view(ModelView(DriverVehicles, db.session))
admin.add_view(ModelView(RideRequest, db.session))

@app.route('/')
def index():
  return render_template('index.html')
  
  
app.run(debug=True)
