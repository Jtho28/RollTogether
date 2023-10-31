

-- Use the ▷ button in the top right corner to run the entire file.

INSERT INTO "rider" ("first_name", "last_initial", "safety_coef", "rider_rating") 
VALUES ("Rider", "1", 3, 3);

INSERT INTO "rider" ("first_name", "last_initial", "safety_coef", "rider_rating") 
VALUES ("Rider", "2", 5, 5);

INSERT INTO "rider" ("first_name", "last_initial", "safety_coef", "rider_rating") 
VALUES ("Rider", "3", 1, 3);

INSERT INTO "rider" ("first_name", "last_initial", "safety_coef", "rider_rating") 
VALUES ("Rider", "4", 1, 1);

INSERT INTO "driver" ("rider_id")
VALUES (0);

INSERT INTO "driver" ("rider_id")
VALUES (1);

INSERT INTO "ride_request" ("rider_id", "departure_locX", "departure_locY", "arrival_locX", "arrival_locY",
                            "request_time", "pick_up_by")
VALUES (2, 78.50, 78.50, 34.5, 56.8, "2022-02-21 05:25:00", "2022-02-21 05:30:00");