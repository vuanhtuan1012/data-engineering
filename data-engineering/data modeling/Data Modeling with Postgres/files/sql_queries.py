# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS times;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE songplays(
    songplay_id INT PRIMARY KEY,
    start_time INT,
    user_id INT,
    level INT,
    song_id INT,
    artist_id INT,
    session_id INT,
    location INT,
    user_agent VARCHAR
);
""")

user_table_create = ("""
CREATE TABLE users(
    user_id INT PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    gender VARCHAR,
    level INT
);
""")

song_table_create = ("""
CREATE TABLE songs(
    song_id INT PRIMARY KEY,
    title VARCHAR,
    artist_id INT,
    year INT,
    duration DECIMAL
);
""")

artist_table_create = ("""
CREATE TABLE artists(
    artist_id INT PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    latitude DECIMAL,
    longtitude DECIMAL
);
""")

time_table_create = ("""
CREATE TABLE time(
    start_time DECIMAL,
    hour INT,
    day INT,
    week INT,
    month INT,
    YEAR INT,
    weekday INT
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays(songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level)
VALUES(%s, %s, %s, %s, %s)
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id, year, duration)
VALUES(%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, name, location, latitude, longtitude)
VALUES(%s, %s, %s, %s, %s)
""")


time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekday)
VALUES(%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]