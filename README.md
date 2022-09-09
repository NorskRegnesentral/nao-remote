# A place for NAO stuff in ROSA

## Contents
This includes

* some work on a Nao simulator
* Nao remote
* ZeroMQ built to work on Nao 6


## Using pyzmq

The ZeroMQ and Python 2 bindings are the `rosa` directory. Rsync this
over to Nao. 

This is a script in `scripts` to set the proper environment variables
so it works with the Nao. Assuming it is in the same place on the Nao,
simply source it in:

```
source scripts/activate-py2zqm.sh
```

You should then be able to import pyzmq in Python 2. For Python 3, use
pip to install pyzmq. They seem to interoperate well, even though they
use different libraries. A future task may be to make sure that both
use Python 2 and Python 3 use the same library.


## Making things run automatically on NAO

You can add entries in /home/nao/naoqi/preferences/autoload.ini
