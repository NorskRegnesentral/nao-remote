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

ssh $SSH_BASE mkdir -p remote_control/scripts
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
 "$SRC_DIR/nao_server/" "${DEST_DIR}remote_control/nao_server"

# $RSYNC $SYNC_ARGS "$SRC_DIR/remote_control/" "${DEST_DIR}remote_control"

$RSYNC $SYNC_ARGS "$SRC_DIR/scripts/activate-py2zqm.sh" "${DEST_DIR}remote_control/scripts"
$RSYNC $SYNC_ARGS "$SRC_DIR/scripts/run_remote_web.sh" "${DEST_DIR}remote_control/scripts"
$RSYNC $SYNC_ARGS "$SRC_DIR/scripts/run_remote_naoqi.sh" "${DEST_DIR}remote_control/scripts"
