# RollTogether
## Env Setup
  Create virtual environment...

    python3 -m venv .venv

  Source virtual environment... 

    source .venv/bin/activate

  Install Dependencies to .venv
    
    pip install -r requirements.txt

  If you're using VScode, it should automatically source the .venv virtual environment whenever you open the RollTogether workspace, so you shouldn't have to source every time

## Database setup for testing
  Run the flask app inside `backend/` with .venv sourced with...
  
    flask --app rtArch run --debug

  Now, there should be a file in `instance/` called `rollt.db`. This is the database file, but there is no data in it.

  Now if you run `flask --app rtArch run --debug` again, open your browser and type `http://127.0.0.1:5000/admin` and you should see an admin panel. Here you can add entities as you please and view them without using the api.

## API
  The api is defined under the urls starting with `api/`. These endpoints support both GET and PUSH methods.

  If you wish to do some api testing for frontend dev, you can use cURL or a tool like Postman to make requests. Your request body must contain the fields specified in the route within rtArch as I don't know of any other way to get it done.

  The api are defined as such, you must include the values in the body of the request for each key in the POST section.

  `/api/riders`
  - GET
    - Returns existing rider entities
  - POST
    - `first_name`
    - `last_initial`

  `/api/drivers`
  - GET
    - Returns existing driver entities
  - POST
    - `rider_id`

  `/api/vehicles`
  - GET
    - Returns existing vehicles
  - POST
    - `vin_num`
    - `plate_num`
    - `driver_id`
    - `model`
    - `make`
    - `num_seats`
    - `year`
    - `miles`

  `/api/ride_requests`
  - GET
    - Get ride requests
  - POST
    - `rider_id`
    - `departure_locX`
    - `departure_locY`
    - `arrival_locX`
    - `arrival_locY`
    - `request_time`
    - `pick_up_by`

  `/api/drive_posts`
  - GET
    - Get drive posts
  - POST
    - `driver_id`
    - `current_locX`
    - `current_locY`
    - `arrival_locX`
    - `arrival_locY`
    - `post_time`

  `/api/schedules`
  - GET
    - Returns existing schedules
  - POST
    - `rider_id`
    - `departure_locX`
    - `departure_locY`
    - `arrival_locX`
    - `arrival_locY`
    - `departure_time`
    - `arrival_time`

