DROP TABLE IF EXISTS appointments;

CREATE TABLE appointments 
(
    sport_id INTEGER NOT NULL,
    sport_name TEXT NOT NULL,
    timeDate DATE NOT NULL,
    timeHM TEST NOT NULL,
    user_id TEXT NOT NULL

);

DROP TABLE IF EXISTS profile;
CREATE TABLE profile 
(
    user_id TEXT NOT NULL,
    act_result TEXT NOT NULL,
    check_date DATE NOT NULL,
    next_check DATE NOT NULL
);


DROP TABLE IF EXISTS users;

CREATE TABLE users 
(
    user_name TEXT NOT NULL,
    user_surname TEXT NOT NULL,
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);
DROP TABLE IF EXISTS sports;

CREATE TABLE sports 
(
    sport_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sport_name TEXT NOT NULL,
    sport_age_min INTEGER NOT NULL,
    sport_age_max INTEGER NOT NULL
);
INSERT INTO sports(sport_name, sport_age_min, sport_age_max)
VALUES ('jumping', 2, 3),
       ('bike riding', 5 ,7),
       ('tennis', 8,9),
       ('climbing', 10, 12),
       (' Working with weights',13,15),
       ('boxing',16, 19),
       ('taekwando',20, 29),
       ('swimming', 30, 39),
       ('regular swimming', 40, 49),
       ('Weight training', 50, 59),
       ('Light weight training', 60, 69),
       ('Golf', 70, 99);


