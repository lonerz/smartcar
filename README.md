# smartcar

## Installation

Make sure to run `pip3 install -r requirements.txt` to install all necessary requirements.

## Running the server

Just run `python3 server.py` to start up the server. The server boots up on port 5000, so you can access
the GET commands via the browser by going to, for example, `http://localhost:5000/vehicles/1000`.

## Running tests

Run `pytest -v` to run tests. This will automatically run tests for the Smartcar API and makes sure we
are calling the right things to the GM API also.
