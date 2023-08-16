#!/bin/sh

# for python 3.10 you need something like:
os_ver=$(uname -r)
if [ "$os_ver" = "4.4.185-rt184-aldebaran" ]; then
  # Nao 6 needs this preload (for now)
  export LD_PRELOAD=/usr/lib/libffi.so.6
fi

export LD_LIBRARY_PATH=/home/nao/rosa/libffi/lib:/home/nao/rosa/zmq/lib:/home/nao/rosa/openssl3/lib
export PATH=/home/nao/rosa/python3.10/bin:$PATH

PYTHONIOENCODING=utf8
export PYTHONIOENCODING

cd /home/nao/rosa/nao_server && python3 -u ./server.py >& /home/nao/rosa/scripts/server.log
