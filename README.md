# A place for NAO stuff in ROSA

## Contents
This includes

* some work on a Nao simulator (in ros_simulation)
* Nao remote (under rosa)
* ZeroMQ library built to work on Nao 6 (under rosa/pyzmq-python2)

## Requirements
* qipkg (or Choreographe) for installing behaviors
* ssh for copying files over to NAO and editing things


## Optional
* Choreographe for creating new behaviors
* OpenSSL for generating a self-signed certificate

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


# TLS certificate

You will need a TLS certificate for NAO in order to communicate properly. The quickest way is to create a self-signed certificate on NAO. Assuming that the hostname for the NAO is nao.local, which is the default when using zeroconf, the command would be.

```
openssl req -x509 -nodes -newkey rsa:2048 -keyout nao_local.key -out nao.local.cer -days 365 -subj "/CN=nao.local"
```

Modify the server.conf so that keyfile and certfile point to the full
path of these files.

You can also run this command on another computer and copy the files
over, but it is less secure.

If NAO is getting a more permanent address (say nao.example.com). The
best solution is to generate a certificate signing request and get a
certificate authority to sign the request and issue a certificate that
you can install. That is beyond the scope of this document.
