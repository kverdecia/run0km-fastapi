#!/bin/bash
PROJECT_NAME="run0km-fastapi"
PROJECT_DIR=$(pwd)
FASTAPI_NAME=${PROJECT_NAME} # Name of the application
if [[ -z "$FASTAPI_DIR" ]]; then
    FASTAPI_DIR=${PROJECT_DIR}/${FASTAPI_NAME} # Django project directory
fi
if [[ -z "$FASTAPI_SOCKFILE" ]]; then
    FASTAPI_SOCKFILE=${PROJECT_DIR}/uvicorn.sock
fi
if [[ -z "$FASTAPI_ASGI_APP" ]]; then
    FASTAPI_ASGI_APP=main:app
fi

echo "Starting $FASTAPI_NAME as ${FASTAPI_USER}"
# Activate the virtual environment
cd $FASTAPI_DIR
# Create the run directory if it doesn't exist
RUNDIR=$(dirname $FASTAPI_SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

exec /home/ubuntu/.local/bin/pipenv run uvicorn ${FASTAPI_ASGI_APP} \
    --uds=${FASTAPI_SOCKFILE} \
    --log-level=debug
