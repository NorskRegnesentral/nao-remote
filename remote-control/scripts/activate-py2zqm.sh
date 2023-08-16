
# Set Python path so that Python2 can use PyZMQ on the Nao.  

if [ -n "${PYTHONPATH+1}" ]; then
    PYTHONPATH=$HOME/rosa/pyzmq-python2/lib/python2.7/site-packages:$PYTHONPATH
else
    PYTHONPATH=$HOME/rosa/pyzmq-python2/lib/python2.7/site-packages
fi

if [ -n "${LD_LIBRARY_PATH+1}" ]; then
    LD_LIBRARY_PATH=$HOME/rosa/zmq/lib:$LD_LIBRARY_PATH
else
    LD_LIBRARY_PATH=$HOME/rosa/zmq/lib
fi

export PYTHONPATH LD_LIBRARY_PATH
