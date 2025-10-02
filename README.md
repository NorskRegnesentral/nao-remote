# A remote control hosted on a webpage for NAO servered over HTTPS

# Requirements

You will need a computer that is capable of running a browser that
supports websockets and javascript. Most graphical browsers released
in 2012 or later should support this. And a NAO robot for running the
remote. 

On your computer need the following installed.
* qipkg (or Choreographe) for installing behaviors
* rsync for copying files over to NAO and editing things 
* ssh as the method of copying over files

On a NAO6, you will already have Python 2 and Python 3 installed. For a 
NAO 5 or NAO 4, you will need to install Python 3. You will need the python
module pyzmq for both Python 2 and Python 3. You will also need the
tornado module for Python 3. You can use the provided binaries and
modules from the dist directory as a timesaver. However, if you wish
to build them yourself, there are instructions for building Python 3
and pyzmq in the doc directory.

If you do not have a NAO, you can use still run the server and
get a webpage up to test, but you will not be able to run the client
part. See [Testing without a NAO](#testing-without-a-nao).


# Optional requirements
* Choreographe for creating new behaviors
* OpenSSL for generating a self-signed certificate
* The NAO SDK for your robot if you wish to cross-compile pyzmq and Python yourself (link if possible).

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
scp dist/nao6/remote_control-nao6-python310-and-zmq.tar.xz nao-address:
ssh nao-address tar Jxf remote_control-nao6-python310-and-zmq.tar.xz
```

You should then be able to import pyzmq in Python 2. For Python 3.5
that is already installed on the NAO6, use pip to install pyzmq. They
seem to interoperate well, even though they use different libraries. A
future task may be to make sure that both use Python 2 and Python 3
use the same library.

For using a newer Python 3 than what is on the robot, see external
documentation from the ROSA project.



# Making things run automatically on NAO

You can add entries in /home/nao/naoqi/preferences/autoload.ini for the two scripts.

Looking something like:
```
[program]
/home/nao/rosa/scripts/run_remote_naoqi.sh
/home/nao/rosa/scripts/run_remote_web.sh
```



# TLS certificate

You will need a TLS certificate for NAO in order to communicate
properly. The quickest way is to create a self-signed certificate on
NAO. Assuming that the hostname for the NAO is nao.local, which is the
default when using zeroconf, the command would be.

```
openssl req -x509 -nodes -newkey rsa:2048 -keyout /home/nao/remote_control/nao_server/certs/nao_local.key -out /home/nao/remote_control/nao_server/certs/nao.local.cer -days 365 -subj "/CN=nao.local"
```

Note that a self-signed certificate will generate a warning when
accessing the page in most browsers.

After you have a certificate, modify server.conf so that the keyfile and
certfile fields point to the full path of these files.

You can also run this command on another computer and copy the files
over, but it is less secure.

If NAO is getting a more permanent address (say nao.example.com). The
best solution is to generate a certificate signing request and get a
certificate authority to sign the request and issue a certificate that
you can install. That is beyond the scope of this document.


# Testing without a NAO

