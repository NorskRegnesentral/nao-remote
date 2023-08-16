# A place for NAO stuff in ROSA

## Contents
This includes

* some work on a Nao simulator (in ros_simulation)
* Nao remote (under rosa)
* ZeroMQ library built to work on Nao 6 (under rosa/pyzmq-python2)

# Nao remote

See the separate README.md in the rosa nao_server directory for more
information.

There also is a `sync-remote` script that will rsync changed bits
over. This is much easier to use than remembering to copy all the bits
over yourself. You need to be able to ssh to NAO for this to work, so
one should probably have a public SSH key installed on NAO as well so
you don't have to type passwords all the time.

## Using pyzmq

The ZeroMQ and Python 2 bindings are the `rosa` directory. Rsync this
over to Nao. 

There are scripts in `rosa/scripts` to set the proper environment variables
so it works with the Nao. Assuming it is in the same place on the Nao,
simply source it in:

```
source scripts/activate-py2zqm.sh
```

You should then be able to import pyzmq in Python 2. For Python 3.5
that is already installed on the NAO6, use pip to install pyzmq. They
seem to interoperate well, even though they use different libraries. A
future task may be to make sure that both use Python 2 and Python 3
use the same library.

For using a newer Python 3 than what is on the robot, see external
documentation from the ROSA project.
