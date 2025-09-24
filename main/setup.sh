#!/bin/bash
export UM_PORT=9815 

source ./venv/bin/activate

gunicorn -w 3 -b 0.0.0.0:$UM_PORT app:app &
gunicorn_server_id=$!
#flask run --host=0.0.0.0 --port $PORT

# Wait for either of the processes to finish
wait