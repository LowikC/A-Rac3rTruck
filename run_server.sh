#!/bin/bash
# This script start the A-Truck Engine server.
# Usage:
# ./run_server.sh </path/to/config/file.conf>

# Execute the .conf file.
. $1

# Add the src directory to the python path
export PYTHONPATH=$ATRUCK_HOME/atruck/:$PYTHONPATH

# Create the log files
touch $ATRUCK_LOGFILE
touch $ATRUCK_ACCESS_LOGFILE

# Start the server with uwsgi
echo -n "Start A-Truck Engine server with uWSGI"
exec uwsgi --http-socket :$ATRUCK_PORT \
           --wsgi-file $ATRUCK_HOME/atruck/EngineServer.py \
           --callable app \
           --set-placeholder log_file=$ATRUCK_LOGFILE \
           --logto $ATRUCK_ACCESS_LOGFILE \
           --logformat "$ATRUCK_LOG_FORMAT"
