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

@dataclass
class Rider(db.Model):
  __tablename__ = "rider"

  rider_id: int
  first_name: str
  last_initial: str
  safety_coef: int
  rider_rating: int
  phone_num: str

  rider_id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(80), nullable=False)
  last_initial = db.Column(db.String(4), nullable=False)
  safety_coef = db.Column(db.Integer, nullable = False, default=6)
  rider_rating = db.Column(db.Integer, nullable = True)
  phone_num = db.Column(db.String(10), nullable=False)
  driver = db.relationship('Driver', backref='rider', uselist=False)
  __table_args__ = (
    CheckConstraint('safety_coef>=1 AND safety_coef<=10', name='safety_coef_ckeck'),
    CheckConstraint('rider_rating>=1 AND rider_rating<=5', name='rating_check')
  )

  def __repr__(self):
    return self.first_name + ' ' + self.last_initial + ' ' + self.phone_num

@dataclass
class Driver(db.Model):
  __tablename__ = "driver"

  driver_id: int
  rider_id: int
  driver_rating: int

  driver_id = db.Column(db.Integer, primary_key=True)
  rider_id = db.Column(db.Integer, db.ForeignKey('rider.rider_id'), nullable=False, unique=True)
  driver_rating = db.Column(db.Integer, nullable = True)
  __table_args__ = (
    CheckConstraint('driver_rating>=1 AND driver_rating<=10', name='driver_rating_check'),
  )

  def __repr__(self):
    return '<%r>' % self.driver_id

@dataclass
class DriverVehicles(db.Model):
  vin_num: str
  plate_num: str
  driver_id: int
  model: str
  make: str
  num_seats: int
  year: int
  miles: float

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

@dataclass
class DrivePost(db.Model):
  d_post_id: int
  driver_id: int
  current_locX: float
  current_locY: float
  arrival_locX: float
  arrival_locY: float
  post_time: datetime

  d_post_id = db.Column(db.Integer, primary_key=True)
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

@dataclass
class CommuteSchedule(db.Model):
  cs_id: int
  rider_id: int
  departure_locX: float
  departure_locY: float
  arrival_locX: float
  arrival_locY: float
  departure_time: datetime
  arrival_time: datetime

  cs_id = db.Column(db.Integer, primary_key=True)
  rider_id = db.Column(db.Integer, db.ForeignKey('rider.rider_id'))
  departure_locX = db.Column(db.Float, nullable=False)
  departure_locY = db.Column(db.Float, nullable=False)
  arrival_locX = db.Column(db.Float, nullable=False)
  arrival_locY = db.Column(db.Float, nullable=False)
  departure_time = db.Column(db.DateTime, nullable=False)
  arrival_time = db.Column(db.DateTime, nullable=False)
  __table_args__ = (
    CheckConstraint('departure_locX>=-180.00 AND departure_locX<=180.00 AND arrival_locX>=-180.00 AND arrival_locX<=180.00'),
    CheckConstraint('departure_locY>=-90.00 AND departure_locY<=90 AND arrival_locY>=-90.00 AND arrival_locY<=90.00')
  )

  def __repr__(self):
    return f"Rider: {self.rider_id}"


# class DriveOffer():

class DriverModelView(ModelView):
  column_display_pk = True
  form_columns = ('rider_id', 'driver_rating')

class RiderModelView(ModelView):
  column_display_pk = True
  form_columns = ('first_name', 'last_initial', 'safety_coef', 'rider_rating', 'phone_num')

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

class CommuteScheduleModelView(ModelView):
  column_auto_select_related = True
  column_display_pk = True
  form_columns = ('rider_id', 'departure_locX', 'departure_locY', 'arrival_locX', 'arrival_locY', 'departure_time', 'arrival_time')

with app.app_context():
  db.create_all()

admin.add_view(RiderModelView(Rider, db.session))
admin.add_view(DriverModelView(Driver, db.session))
admin.add_view(VehiclesModelView(DriverVehicles, db.session))
admin.add_view(RideRequestModelView(RideRequest, db.session))
admin.add_view(RidePostModelView(DrivePost, db.session))
admin.add_view(CommuteScheduleModelView(CommuteSchedule, db.session))

@app.route('/rides')
def ride_requests():
  ride_requests = RideRequest.query.all()
  return render_template('ride_requests.html', ride_requests=ride_requests)

@app.route('/drives')
def ride_posts():
  ride_posts = RidePost.query.all()
  return render_template('ride_posts.html', ride_posts=ride_posts)

@app.route('/recommend/<int:rider_id>')
def rec(rider_id):
  from rtLib import rt_pool

  schedules = db.session.query(CommuteSchedule, Rider).join(CommuteSchedule).all()
  print(schedules)
  # schedules = CommuteSchedule.query.all()
  # print(schedules)
  # for row in schedules:
  #   print(row[0])


  group = rt_pool(schedules, rider_id=rider_id)
  return jsonify(group)


@app.route('/api/riders', methods=['POST', 'GET'])
def serve_riders():
  if (request.method == 'GET'):

    riders = Rider.query.all()
    return jsonify(riders)

  elif (request.method == 'POST'):
    first_name = request.form['first_name']
    last_initial = request.form['last_initial']
    phone_num = request.form['phone_num']

    rider = Rider(first_name=first_name, last_initial=last_initial, phone_num=phone_num)
    db.session.add(rider)
    db.session.commit()

    return jsonify(rider)

@app.route('/api/drivers', methods=['POST', 'GET'])
def serve_drivers():
  if (request.method == 'GET'):

    drivers = Driver.query.all()
    return jsonify(drivers)

  elif (request.method == 'POST'):
    rider_id = request.form['rider_id']

    driver = Driver(rider_id=rider_id)
    db.session.add(driver)
    db.session.commit()

    return jsonify(driver)

@app.route('/api/vehicles', methods=['POST', 'GET'])
def serve_vehicles():
  if (request.method == 'GET'):
    vehicles = DriverVehicles.query.all()
    return jsonify(vehicles)

  elif (request.method == 'POST'):
    vin_num = request.form['vin_num']
    plate_num = request.form['plate_num']
    driver_id = request.form['driver_id']
    model = request.form['model']
    make = request.form['make']
    num_seats = request.form['num_seats']
    year = request.form['year']
    miles = request.form['miles']

    vehicle = DriverVehicles(vin_num=vin_num, plate_num=plate_num, driver_id=driver_id,
                             model=model, make=make, num_seats=num_seats, year=year,
                             miles=miles)
    db.session.add(vehicle)
    db.session.commit()

    return jsonify(vehicle)

@app.route('/api/ride_requests', methods=['POST', 'GET'])
def serve_ride_requests():
  if (request.method == 'GET'):
    ride_requests = RideRequest.query.all()
    return jsonify(ride_requests)

  elif (request.method == 'POST'):
    rider_id = request.form['rider_id']
    departure_locX = request.form['departure_locX']
    departure_locY = request.form['departure_locY']
    arrival_locX = request.form['arrival_locX']
    arrival_locY = request.form['arrival_locY']
    request_time = request.form['request_time']
    pick_up_by = request.form['pick_up_by']

    ride_request = RideRequest(rider_id=rider_id, departure_locX=departure_locX,
                               departure_locY=departure_locY, arrival_locX=arrival_locX,
                               arrival_locY=arrival_locY, request_time=request_time,
                               pick_up_by=pick_up_by)
    db.session.add(ride_request)
    db.session.commit()

    return jsonify(ride_request)

@app.route('/api/drive_posts', methods=['POST', 'GET'])
def serve_drive_posts():
  if (request.method == 'GET'):
    drive_posts = DrivePost.query.all()
    return jsonify(drive_posts)

  elif (request.method == 'POST'):
    driver_id = request.form['driver_id']
    current_locX = request.form['current_locX']
    current_locY = request.form['current_locY']
    arrival_locX = request.form['arrival_locX']
    arrival_locY = request.form['arrival_locY']
    post_time = request.form['post_time']

    drive_post = DrivePost(driver_id=driver_id, current_locX=current_locX, current_locY=current_locY,
                           arrival_locX=arrival_locX, arrival_locY=arrival_locY, post_time=post_time)

    db.session.add(drive_post)
    db.session.commit()

    return jsonify(drive_post)
    

@app.route('/api/schedules', methods=['POST', 'GET'])
def schedule():
  if (request.method == 'GET'):
    schedules = CommuteSchedule.query.all()
    return jsonify(schedules)

  elif (request.method == 'POST'):
    rider_id = request.form['rider_id']
    departure_locX = request.form['departure_locX']
    departure_locY = request.form['departure_locY']
    arrival_locX = request.form['arrival_locX']
    arrival_locY = request.form['arrival_locY']
    departure_time = datetime.strptime(request.form['departure_time'], "%Y-%m-%dT%H:%M:%S")
    arrival_time = datetime.strptime(request.form['arrival_time'], "%Y-%m-%dT%H:%M:%S")

    schedule = CommuteSchedule(rider_id=rider_id, departure_locX=departure_locX,
                               departure_locY=departure_locY, arrival_locX=arrival_locX,
                               arrival_locY=arrival_locY, departure_time=departure_time,
                               arrival_time=arrival_time)

    db.session.add(schedule)
    db.session.commit()

    return jsonify(schedule)

# class rideRequests(Resource):
#   def get

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
