# Running the App Locally

## Generating the Database
Ensure that local instance of MySQL is running on 
localhost:3306

Run the individual table create scripts under:

```
\sql\table_creeate_statements.sql
```

Import each dataset using the scripts under:
```
\sql\data_imports.sql
```

> **Note:** you may need to run the script to enable the 'local infile' permission in order to import from .csv files.


## With Docker \[optional\]
You can optionally spin up a docker container with the MySQL instance as well as default root user configs. 

Run the docker-compose command in the project root
```
docker-compose up
``` 

Once the container is running, create your database and run the table create sctipts. 

## Running the  Web Server
To start flask server locally with hot-reloading run the following:
```
source venv/bin/activate
flask run -p 5001 --debug
```

To view the app, go to your browseer and access [localhost:5001](http://localhost:5001)