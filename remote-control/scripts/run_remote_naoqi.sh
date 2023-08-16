#!/bin/sh

source /home/nao/rosa/scripts/activate-py2zqm.sh
# Make sure that the python encoding is utf-8 always.
PYTHONIOENCODING=utf8
export PYTHONIOENCODING

python2 -u /home/nao/rosa/nao_server/app/scripts/remote.py >& /home/nao/rosa/scripts/remote.log
