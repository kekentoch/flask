CREATE TABLE IF NOT EXISTS Users
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname varchar(25) NOT NULL UNIQUE,
    password varchar(100) NOT NULL,
    email varchar(100) NOT NULL UNIQUE,
    creation_date date,
    country_id int,
    FOREIGN KEY (country_id) REFERENCES Countries(country_id)
);
CREATE TABLE IF NOT EXISTS Playlists
(
    playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_date date,
    name varchar(100) UNIQUE NOT NULL,
    genre varchar(50),
    access_level int,
    FOREIGN KEY (access_level) REFERENCES Access_level(access_level_id),
    FOREIGN KEY (genre) REFERENCES Genres(genre_id)
);
CREATE TABLE IF NOT EXISTS Countries
(
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country varchar(50)
);
CREATE TABLE IF NOT EXISTS Access_level
(
    access_level_id INTEGER PRIMARY KEY AUTOINCREMENT,
    access_level varchar(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS User_playlist
(
    user_id int NOT NULL,
    playlist_id int NOT NULL,
    CONSTRAINT pk_user_playlist PRIMARY KEY (user_id, playlist_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES Users(user_id),
    CONSTRAINT fk_playlist FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id)
);
CREATE TABLE IF NOT EXISTS Tracks
(
    track_id INTEGER PRIMARY KEY AUTOINCREMENT,
    format_id int,
    name varchar(50) NOT NULL,
    creation_date date,
    total_plays int,
    plays_per_month int,
    plays_per_day int,
    FOREIGN KEY (format_id) REFERENCES Format(format_id)
);
CREATE TABLE IF NOT EXISTS Format
(
    format_id INTEGER PRIMARY KEY AUTOINCREMENT,
    format varchar(50)
);
CREATE TABLE IF NOT EXISTS Track_playlist
(
    track_id int NOT NULL,
    playlist_id int NOT NULL,
    CONSTRAINT pk_track_playlist PRIMARY KEY (track_id, playlist_id),
    CONSTRAINT fk_track FOREIGN KEY (track_id) REFERENCES Tracks(track_id),
    CONSTRAINT fk_playlist FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id)
);
CREATE TABLE IF NOT EXISTS Albums
(
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description varchar(200),
    name varchar(50) NOT NULL,
    genre_id varchar(50),
    creation_date date,
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);
CREATE TABLE IF NOT EXISTS Track_album
(
    track_id int NOT NULL,
    album_id int NOT NULL,
    CONSTRAINT pk_track_album PRIMARY KEY (track_id, album_id),
    CONSTRAINT fk_track FOREIGN KEY (track_id) REFERENCES Tracks(track_id),
    CONSTRAINT fk_album FOREIGN KEY (album_id) REFERENCES Albums(album_id)
);
CREATE TABLE IF NOT EXISTS Genres
(
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genre varchar(50)
);
CREATE TABLE IF NOT EXISTS Track_genre
(
    track_id int NOT NULL,
    genre_id int NOT NULL,
    CONSTRAINT pk_track_genre PRIMARY KEY (track_id, genre_id),
    CONSTRAINT fk_track FOREIGN KEY (track_id) REFERENCES Tracks(track_id),
    CONSTRAINT fk_genre FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);