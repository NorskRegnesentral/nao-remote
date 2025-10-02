#!/bin/sh

# for python 3.10 you need something like:
os_ver=$(uname -r)
if [ "$os_ver" = "4.4.185-rt184-aldebaran" ]; then
  # Nao 6 needs this preload (for now)
  export LD_PRELOAD=/usr/lib/libffi.so.6
fi

export LD_LIBRARY_PATH=/home/nao/remote_control/libffi/lib:/home/nao/remote_control/zmq/lib:/home/nao/remote_control/openssl3/lib
export PATH=/home/nao/remote_control/python3.10/bin:$PATH

PYTHONIOENCODING=utf8
export PYTHONIOENCODING

cd /home/nao/remote_control/nao_server && python3 -u ./server.py >& /home/nao/remote_control/scripts/server.log
