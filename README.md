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
  Run the init.py file with .venv sourced.

    python init.py

  This will create the database in `instance/rollt.db` and populate the database with some test data specified in `instance/db_test_dat.sql`

