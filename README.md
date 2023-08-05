
<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />

<h3 align="center">Beer Dispenser API</h3>

  <p align="center">
    A solution for the
    <a href="https://github.com/code-sherpas/product-developer-challenge_beer-tap-dispenser"> Beer dispenser API challenge</a>
  </p>
</div>


## About The Project

The goal of the project is to create an beer dispensing API! Admins can create dispensers with specific `flow_volumes` and `prices`. The challenge did not mention anything about the dispenser beer price, but it did mention amount of money spent so it was added as a requirement for each dispenser. Attendees can open the dispenser tap to get the beer into their glass (starting a new transaction), and close it when they want to (ending the transaction). The API calculates and stores the `amount` of beer poured and `revenue` generated in each transaction based on the `flow_volume`, `price`, and the time the tap was open.

Admins can request statistics for any or all dispensers, which includes the basic information about dispensers along with all of their transactions (including ones that are currently open). Attendees can only request basic information about any or all the dispensers.

### Sequence diagram
The flow of the application can be summarised with the following sequence diagram:
![App sequence diagram](static/sequence_diagram.png)

### API Endpoints
The API provides the following endpoints:

#### Login
* POST /auth/login: Endpoint for admin login. Returns a JWT access token upon successful authentication.

#### Admin endpoints
* POST /api/dispenser: Create a new dispenser. Requires authentication.
* GET /api/statistics: Get statistics about usage and revenue of all dispensers. Requires authentication.
* GET /api/statistics/{dispenser_id}: Get statistics about usage and revenue of a specific dispenser. Requires authentication.

#### Attendee endpoints
* GET /api/dispenser: Retrieve basic information about all dispensers.
* GET /api/dispenser/{dispenser_id}: Retrieve basic information about a specific dispenser.
* POST /api/dispenser/{dispenser_id}/open: Open a dispenser tap.
* POST /api/dispenser/{dispenser_id}/close: Close a dispenser tap.


### Authentication
The API uses JWT (JSON Web Tokens) for admin authentication. To access authenticated endpoints, admins must include a valid JWT token in the request headers.

To obtain a JWT token, send a POST request to the /auth/login endpoint with valid admin credentials. The response will include the JWT access token, which should be included in the headers of subsequent requests to authenticated endpoints.


### Built With

This project is built using the following technologies:

* Flask: A lightweight Python web framework used for building the API.
* SQLAlchemy: An Object-Relational Mapping (ORM) library for working with the database.
* PostgreSQL: A relational database used for storing dispenser and transaction data, as well as the admin credentials. Used for the production environment only.
* SQLite3: Simple database for the development environment.
* Flask-JWT-Extended: A Flask extension for handling JSON Web Tokens (JWT) for authentication.
* Pytest: A testing framework for writing unit tests.
* Gunicorn: A Python WSGI HTTP Server for production.
* Bash: A Unix shell language for a tiny dispenser monitoring script.
* Render: A cloud platform for hosting and deploying the API and the database in production.


#### Database Design
The database schema includes two main tables: `Dispenser` and `Transaction`. The Dispenser table stores information about each dispenser, including `flow_volume`, `price`, and `is_open` status. The `Transaction` table tracks dispenser usage, recording the `start_time`, `end_time`, `total_amount`, and `revenue` for each transaction.

The `Admin` table stores the `username` and `password_hash`. The actual password is hashed with the `bcrypt` library not to store clear text passwords in the database for security reasons.

![Database design diagram](static/database_design.png)

## Getting Started

### Development
To run the API locally in a development environment, you can use the provided Docker image.
The `Dockerimage` file defines some environment variables that you can change to your liking.
Build and start the container with the following commands:
```
docker build -t beer-dispenser-api .
docker run -p 5000:5000 beer-dispenser-api
```

You can access the Docker container with:
`docker exec -it <CONTAINER_ID> /bin/bash`
You can find the `CONTAINER_ID` by listing all running containers:
`docker ps`

You can also use run the project without Docker in a virtual environment
with the provided `run_dev.py` script.
Note: [Python](https://www.python.org/downloads/) is required for this option!

You will need to create a `.env` file first. To get started you can simply copy the example file provided:
`cp .env.example .env`

You can change the environment variables in `.env` file to your liking.

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 run_dev.py
```

To generate a strong JWT secret, you can run the following:
```
openssl rand -hex 32
```
Replace the `JWT_SECRET` in the `.env` file (or `Dockerimage` for Docker) with the output of the above command.

### Unit Tests
The project includes a comprehensive suite of unit tests using the pytest framework. To run the tests, execute: `python3 -m pytest` in the project root directory (either inside the Docker container or the virtual environment).

#### Test Coverage
To generate a test coverage report, first run:
`coverage run -m pytest`, and then for a terminal view of the report:
`coverage report -m`, or to generate an HTML report:
`coverage html`

```
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
app/__init__.py                     18      0   100%
app/models.py                       64      1    98%   18
app/routes/__init__.py               0      0   100%
app/routes/api.py                   88     13    85%   34-36, 65, 80-82, 90, 103, 126-128, 137
app/routes/auth.py                  14      0   100%
tests/conftest.py                   28      0   100%
tests/test_auth.py                  17      0   100%
tests/test_dispenser.py            124      0   100%
tests/test_invalid_endpoint.py       7      0   100%
tests/test_statistics.py            99      0   100%
--------------------------------------------------------------
TOTAL                              459     14    97%
```

### Example requests

Example requests can be found in the `example_requests.http` file, which comform to the VSCode [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client). You can use them as a guide for making API requests with `curl` as well. Some examples:

Login:
```
curl -X POST "http://localhost:5000/auth/login" -H 'Content-Type: application/json' -d '{"username": "dispenser", "password": "admin"}'

{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5MTEzOTAyNiwianRpIjoiM2YwNTgzODItN2EyNS00ZDk2LThjZjYtYWYyZjc3YjhiNDdjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjkxMTM5MDI2LCJleHAiOjE2OTExMzk5MjZ9.fJFB1bwBus_InMS-0NxkOTl_KrzIOMqRHwrNYEqZsxA"}
```
Create dispenser:
```
curl -X POST "http://localhost:5000/api/dispenser" -H 'Content-Type: application/json' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5MTEzOTAyNiwianRpIjoiM2YwNTgzODItN2EyNS00ZDk2LThjZjYtYWYyZjc3YjhiNDdjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjkxMTM5MDI2LCJleHAiOjE2OTExMzk5MjZ9.fJFB1bwBus_InMS-0NxkOTl_KrzIOMqRHwrNYEqZsxA' -d '{"flow_volume": 0.5, "price": 2.5}'

{"flow_volume":0.5,"id":5,"price":2.5}
```

### Monitoring
A small bash script is available to continously monitor the available dispensers in the terminal. It could be used as a simple display for attendees to see all the dispensers on offer. To start the script, run: `./monitoring/monitor.sh`. Here is the sample output:
```
                            Dispenser Monitoring
==============================================================================================
Dispenser ID: 1        | Flow Volume: 0.5     L/s | Price: $1      | Status: Closed
----------------------------------------------------------------------------------------------
Dispenser ID: 2        | Flow Volume: 0.5     L/s | Price: $1      | Status: Closed
----------------------------------------------------------------------------------------------
Dispenser ID: 3        | Flow Volume: 0.5     L/s | Price: $1      | Status: Closed
----------------------------------------------------------------------------------------------
Dispenser ID: 4        | Flow Volume: 0.5     L/s | Price: $1      | Status: Closed
----------------------------------------------------------------------------------------------
Dispenser ID: 5        | Flow Volume: 0.5     L/s | Price: $2.5    | Status: Closed
----------------------------------------------------------------------------------------------
```

### Production
To run a production-ready setup, you should use a Gunicorn with a postgreSQL database. In short, all you need to do is set your `DB_URI` environment variable to point to your postgres instance, for example:
`DB_URI=postgresql://username:password@host:port/database_name`

If you want to set up a local postgres instance, you can follow the official [installation instructions](https://www.postgresql.org/download/). Once you have postgres running locally, you can create a new user for this project, and set up the database:

```
psql postgres

postgres=# CREATE USER dispenser WITH PASSWORD 'your_password' CREATEDB;
CREATE ROLE
postgres=# CREATE DATABASE dispenser_db OWNER dispenser;
CREATE DATABASE
```

Your local database is ready to be used by the app. For this example, you would set the `DB_URI` environment variable to:

`DB_URI=postgresql://dispenser:your_password@127.0.0.1:5432/dispenser_db`

Because the project uses SQLAlchemy, everything will work with different databases (SQLite3, postgreSQL, MySQL...). Once your `DB_URI` is set, start a production-ready web server with Gunicorn by running:
`gunicorn wsgi:app`

That's it!

### CI/CD
This project uses a GitHub workflow integrated with [Render](https://render.com/) for CI/CD. The workflow is a simple `build-and-test` -> `deploy`. Render was chosen because it provides a free postgreSQL database and a free web worker. Here are the general steps in order to make this work for your project:

1. Register on [Render](https://render.com/)
2. Create a new postgreSQL resource -> find the `DB_URI` for this database
3. Create a new Web Service resource and configure it with build and start commands and environment variables (in addition to our projects' variables set the `PYTHON_VERSION` to `3.8.10`):
```
pip3 install --upgrade pip && pip install -r requirements.txt
```
```
gunicorn wsgi:app
```
4. Turn auto-deploy on -> this gives you a *deploy hook* from which you can find your `service-id` (e.g. `srv-97tasd...`)
5. Create your `RENDER_API_KEY` from the Render Account settings page.
6. Add secrets to your GitHub repo:
```
RENDER_API_KEY=your_render_API_key
RENDER_SERVICE_ID=your_render_service_id
``` 
That's it, the pipeline will trigger on every push to the `master` branch.

This deployment is available at https://beer-dispenser-api.onrender.com/api/docs.
You can use the following credentials to play around as an admin:

Username: `dispenser`
Password: `admin`

## Considerations / Possible features

1. Currently, the app creates one admin once started from the enviroment variables `ADMIN_USERNAME` and `ADMIN_PASSWORD`. Any additional admins would have to be added to the database manually. A possible extension to the project would be admin management, but for this iteration it is considered out of scope.

2. Why Flask? It's simple, flexible and lightweight which suits this project. Besides that, I have not used Flask in a while so I considered it a good exercise.

3. Why PostgreSQL for production? SQLite3 is great for development purposes as it is light and requires no configuration. However, if we think about this application at scale, we must use postgres for its robustness and stability, as we could easily imagine an event with thousands of dispensers and millions of transactions!

4. JWT is a simple and fitting solution for this task. However, for added security at scale, it could be replaced or complemented with other advanced authentication methods.

5. Every dispenser only has the technical properties `flow_volume` and `price`. Where are the beer descriptions!? Some attendees might want to know what they are going to be drinking!

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[contributors-shield]: https://img.shields.io/github/contributors/dostrelith678/beer-dispenser-api.svg?style=for-the-badge
[contributors-url]: https://github.com/dostrelith678/beer-dispenser-api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dostrelith678/beer-dispenser-api.svg?style=for-the-badge
[forks-url]: https://github.com/dostrelith678/beer-dispenser-api/network/members
[stars-shield]: https://img.shields.io/github/stars/dostrelith678/beer-dispenser-api.svg?style=for-the-badge
[stars-url]: https://github.com/dostrelith678/beer-dispenser-api/stargazers
[issues-shield]: https://img.shields.io/github/issues/dostrelith678/beer-dispenser-api.svg?style=for-the-badge
[issues-url]:https://github.com/dostrelith678/beer-dispenser-api/issues
[license-shield]: https://img.shields.io/github/license/dostrelith678/beer-dispenser-api.svg?style=for-the-badge
[license-url]: https://github.com/dostrelith678/beer-dispenser-api/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/damjan-ostrelic

