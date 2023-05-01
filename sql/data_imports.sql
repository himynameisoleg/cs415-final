-- enable local infile to be able to load CSV files
SHOW GLOBAL VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = true;

LOAD DATA LOCAL INFILE  '/Users/op/code/cs415-final/sql/datasets/users.csv'
INTO TABLE Users
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE  '/Users/op/code/cs415-final/sql/datasets/movies.csv'
INTO TABLE Movies
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA LOCAL INFILE  '/Users/op/code/cs415-final/sql/datasets/actors.csv'
INTO TABLE Actors
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE  '/Users/op/code/cs415-final/sql/datasets/favorites.csv'
INTO TABLE Actors
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;



