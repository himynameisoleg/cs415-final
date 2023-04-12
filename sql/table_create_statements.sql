CREATE TABLE Movies (
    Poster_Link VARCHAR(255) NOT NULL,
    Title VARCHAR(255) NOT NULL,
    Released_Year INT NOT NULL,
    Certificate VARCHAR(30) NULL,
    Runtime VARCHAR(30) NULL,
    Genre VARCHAR(255) NULL,
    IMDB_Rating DECIMAL(2, 1) NULL,
    Overview VARCHAR(255) NULL,
    Meta_score INT NULL,
    Director VARCHAR(30) NULL,
    Star1 VARCHAR(30) NULL,
    Star2 VARCHAR(30) NULL,
    Star3 VARCHAR(30) NULL,
    Star4 VARCHAR(30) NULL,
    No_of_Votes INT NULL,
    Gross BIGINT NULL,
    PRIMARY KEY (Title)
);


CREATE TABLE Actors (
	Name VARCHAR(30) NULL,
    Title VARCHAR(255) NULL,
    Released_Year INT NULL,
    Votes BIGINT NULL,
    Rating DECIMAL(2, 1) NULL
);

CREATE TABLE Users (
    UserID VARCHAR(255) NOT NULL,
	Password VARCHAR(30) NOT NULL,
    Age INT NOT NULL,
    City VARCHAR(30) NOT NULL,
    PRIMARY KEY (UserID)
);

CREATE TABLE Favorites (
    UserID   VARCHAR(255) NOT NULL,
    Title VARCHAR(255) NOT NULL,
    Date_Added DATE NOT NULL,
	FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (Title) REFERENCES Movies(Title)
)