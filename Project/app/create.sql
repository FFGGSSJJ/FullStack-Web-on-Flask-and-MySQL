CREATE TABLE movie_info(
    movie_id INT NOT NULL,
    title VARCHAR(50),
    imdb_id VARCHAR(15),
    release_date DATETIME,
    overview VARCHAR(255),
    tagline VARCHAR(255),
    homepage VARCHAR(255),
    poster_path VARCHAR(255),
    popularity REAL,
    revenue INT,
    PRIMARY KEY (movie_id)
);

CREATE TABLE account_info(
    userID INT NOT NULL,
    account_name VARCHAR(20),
    account_passwd VARCHAR(255),
    age INT,
    account_type INT,
    tag1 INT,
    tag2 INT,
    tag3 INT,
    PRIMARY KEY (userID)
);

CREATE TABLE comments(
    comment_id INT NOT NULL,
    userID INT NOT NULL,
    movie_id INT NOT NULL,
    rating REAL,
    adding_date DATETIME,
    msg VARCHAR(255),
    PRIMARY KEY (comment_id),
    FOREIGN KEY (userID) REFERENCES account_info(userID),
    FOREIGN KEY (movie_id) REFERENCES movie_info(movie_id)
);

CREATE TABLE watch_list(
    watch_id INT NOT NULL,
    movie_id INT NOT NULL,
    userID INT NOT NULL,
    watch_add_date DATETIME,
    PRIMARY KEY (watch_id),
    FOREIGN KEY (userID) REFERENCES account_info(userID),
    FOREIGN KEY (movie_id) REFERENCES movie_info(movie_id)
);

CREATE TABLE genre(
    genre_id INT NOT NULL,
    genre_name VARCHAR(20),
    PRIMARY KEY (genre_id)
);

CREATE TABLE movie_genre(
    movie_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (genre_id) REFERENCES genre(genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie_info(movie_id)
);