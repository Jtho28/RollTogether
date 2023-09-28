-- database: rollt.db
CREATE TABLE "Riders"(
	rider_id INTEGER PRIMARY KEY,
  first_name VARCHAR(20),
  last_initial CHAR(1),
	departure_locX REAL,
	departure_locY REAL,
	arrival_locX REAL,
	arrival_locY REAL,
	safety_coef REAL,
	user_rating REAL DEFAULT 3.0
)