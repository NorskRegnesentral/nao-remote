
# Set Python path so that Python2 can use PyZMQ on the Nao.  

if [ -n "${PYTHONPATH+1}" ]; then
    PYTHONPATH=$HOME/remote_control/pyzmq-python2/lib/python2.7/site-packages:$PYTHONPATH
else
    PYTHONPATH=$HOME/remote_control/pyzmq-python2/lib/python2.7/site-packages
fi

if [ -n "${LD_LIBRARY_PATH+1}" ]; then
    LD_LIBRARY_PATH=$HOME/remote_control/zmq/lib:$LD_LIBRARY_PATH
else
    LD_LIBRARY_PATH=$HOME/remote_control/zmq/lib
fi

export PYTHONPATH LD_LIBRARY_PATH
