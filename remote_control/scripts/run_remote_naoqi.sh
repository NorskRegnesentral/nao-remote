#!/bin/sh

source /home/nao/remote_control/scripts/activate-py2zqm.sh
# Make sure that the python encoding is utf-8 always.
PYTHONIOENCODING=utf8
export PYTHONIOENCODING

python2 -u /home/nao/remote_control/nao_server/app/scripts/remote.py >& /home/nao/remote_control/scripts/remote.log
