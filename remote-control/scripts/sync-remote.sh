#!/bin/sh

# Script to sync between git repo and the robot

if [ $# -lt 1 ]; then
    echo "Usage $0 <host>"
    exit 2
fi

ROBOT_ADDRESS=$1
ROBOT_USERNAME=nao

SCRIPT_DIR=$(cd $(dirname "$0") && pwd)
SRC_DIR=$(dirname $SCRIPT_DIR)
SSH_BASE=$ROBOT_USERNAME@$ROBOT_ADDRESS
DEST_DIR=$SSH_BASE:



RSYNC=$(which rsync)

SYNC_ARGS="-avz"

${RSYNC:?"rysnc not found!"} $SYNC_ARGS -f '- *.pyc' \
			     -f '- server.conf' \
			     -f '- app/b*' \
			     -f '- app/dance_*' \
			     -f '- app/c*' \
			     -f '- app/g*' \
			     -f '- app/m*' \
			     -f '- app/next_task' \
			     -f '- app/raise_hand' \
			     -f '- app/remote.pml' \
			     -f '- app/small_cheer' \
                             -f '- app/exciting_fun' \
			     -f '- .mypy_cache' \
			     -f '- app/t*' \
			     -f '- app/icon.png' \
			     -f '- app/.metadata' \
			     -f '- app/manifest.xml' \
 "$SRC_DIR/nao_server/" "${DEST_DIR}rosa/nao_server"

# $RSYNC $SYNC_ARGS "$SRC_DIR/rosa/" "${DEST_DIR}rosa"

ssh $SSH_BASE mkdir -p rosa/scripts
$RSYNC $SYNC_ARGS "$SRC_DIR/scripts/activate-py2zqm.sh" "${DEST_DIR}rosa/scripts"
$RSYNC $SYNC_ARGS "$SRC_DIR/scripts/run_remote_web.sh" "${DEST_DIR}rosa/scripts"
$RSYNC $SYNC_ARGS "$SRC_DIR/scripts/run_remote_naoqi.sh" "${DEST_DIR}rosa/scripts"
