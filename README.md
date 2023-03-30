# Running the App Locally

## Database Setup
### With Local MySql instance
* Ensure that local instance of MySQL is running on localhost:3306
* Run migration scripts to populate with dummy data


### With Docker
Run the docker-compose command in the project root
```
docker-compose up
``` 

## Running the Server
To start flask server locally with hot-reloading run the following:
```
source venv/bin/activate
python app.py
```
or 
```
flask run -p 5001 --debug
```