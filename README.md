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
  Run the rtArch.py file with .venv sourced with either...

    python rtArch.py

  Or...
  
    flask --app rtArch run --debug

  Now, there should be a file in `instance/` called `rollt.db`. This is the database file, but there is no data in it.

  To populate the database with some test data, close out of the running flask app with `ctrl+C` and run `test_populate.py` with .venv sourced...

    python test_populate.py

  Now if you run `python rtArch.py` again, open your browser and type `http://127.0.0.1:5000/` and you should see `Hello, World!`. Make sure the rtArch.py Flask app is still running.

  To access the Admin panel to see the data in the database, navigate to `http://127.0.0.1:5000/admin/` and you should see the Rider, Driver, RideRequest, and DriverVehicles tabs. Click on them to see the data inside.

  You should be able to add Riders to the database from the admin panel, however, I can't figure out how to properly add Driver entities from the admin portal.

  If you wish to change the entities or want to test some different data, delete the `rollt.db` file. Then, change the values in the `db_test_dat.sql` under `instances`. I provided some example data so you can understand the syntax. 
  When you've added the data you want, run `rtArch.py` again and then `test_populate.py` like we did before, and you should see your new data in the admin panel.

