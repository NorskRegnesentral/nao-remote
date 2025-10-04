# A remote control hosted on a webpage for NAO servered over HTTPS

# Requirements

You will need a computer that is capable of running a browser that
supports websockets and javascript. Most graphical browsers released
in 2012 or later should support this. And a NAO robot for running the
remote. 

On your computer need the following installed.
* qi and qibuild python modules for installing behaviors (or use
  [Choregraphe](https://aldebaran.com/en/support/kb/nao6/downloads/nao6-software-downloads/))
* rsync for copying files over to NAO and editing things 
* ssh as the method of copying over files.

On a NAO6 has a version of Python 3, but we will install our own Python.
NAO 5 or NAO 4, you will need to install Python 3. You will need the python
module pyzmq for both Python 2 and Python 3. You will also need the
tornado module for Python 3. You can use the provided binaries and
modules from the dist directory as a timesaver. However, if you wish
to build them yourself, there are instructions for building Python 3
and pyzmq in the doc directory.

In the past, the remote has run and worked with the Python 3 installed
on NAO6 and modules installed from its pip, but this has not been
tested for a while. You can use
[remote_contrlol/nao_server/requirements.txt](remote_control/nao_server/requirements.txt)
in this case.

If you do not have a NAO, you can use still run the server and
get a webpage up to test, but you will not be able to run the client
part. See [Testing without a NAO](#testing-without-a-nao).


# Optional requirements
* Choregraphe for creating new behaviors
* OpenSSL for generating a self-signed certificate
* The NAO Linux developer tools for your robot if you wish to
  cross-compile pyzmq and Python yourself (link if possible).

# Installation

The remote control runs completely on NAO. The web page is served
using Python 3.10 and the [Tornado
framework](https://www.tornadoweb.org/en/stable/). It communicates
with a Python 2 process to communicate with NAOqi via
[ZeroMQ](https://zeromq.org/). Installation consists of several steps.

1. Installing Python 3, Python modules, and associated libraries
2. Copying over the remote
3. Installing behaviors
4. Installing a TLS certificate

Much of the installation will use ssh, so one should probably have a
public SSH key installed on NAO as well so you don't have to type
passwords all the time.

## Installing Python 3, Python modules, and associated libraries

In the `dist` directory are tarball archives that include the Python
3, pyzmq, and the associated libraries for NAO5 and NAO6. Copy the
tarball over to NAO and unpack the archive.

```
scp dist/remote_control-nao6-python310-and-zmq.tar.xz nao-address:
ssh nao-address tar Jxf remote_control-nao6-python310-and-zmq.tar.xz
```

If you would rather build these libraries yourself, instructions are
included in [the doc directory](doc/cross-build-python.org)

## Copy over the remote

Use the `sync-remote` script top copy over the scripts. This uses
rsync and ssh to copy the bits over.

```
cd remote-control/scripts
./sync-remote.sh
```

that will rsync changed bits over. 

## Installing behaviors

The behaviors for the remote are under nao_server/app. You can install
it using Choregraphe. Alternatively you can use `qipkg` from the
qibuild python module.

```
python3 -mvenv qibuild_env
source qibuild_env/bin/activate
pip install qi qibuild
cd nao-remote/remote-control/nao_server/app
qipkg deploy-package remote.pml --url nao@nao.local
```

## Installing a TLS certificate

You will need a TLS certificate for NAO in order to communicate
properly. The quickest way is to create a self-signed certificate on
NAO (You can use the `openssl` binary from dist if installed Python 3
using that). Assuming that the hostname for the NAO is nao.local,
which is the default when using zeroconf, the command would be.

```
openssl req -x509 -nodes -newkey rsa:2048 -keyout /home/nao/remote_control/nao_server/certs/nao.local.key -out /home/nao/remote_control/nao_server/certs/nao_local_cert.cer -days 365 -subj "/CN=nao.local"
```

Note that a self-signed certificate will generate a warning when
accessing the page in most browsers.

After you have a certificate, modify
`remote_control/nao_server/conf/server.conf` so that the keyfile and
certfile fields point to the full path of these files. By default
server will use look for files like above.

You can also run this command on another computer and copy the files
over, but it is less secure.

If a NAO is getting a more permanent address (say nao.example.com).
The best solution is to generate a certificate signing request and get
a certificate authority to sign the request and issue a certificate
that you can install. That is beyond the scope of this document.

# Running the remote

One you have all the parts installed, you should be able to run the
remote and connect to it. First, you need to start the webserver and
the NAOqi client. Here is a way to start them in the background.

```
/home/nao/remote_control/scripts/run_remote_naoqi.sh &
/home/nao/remote_control/scripts/run_remote_web.sh &
```

The order here is not important, but both must be started. Each script
creates a log file (`remote.log` and `server.log` respectively). That
you can use to check their status.

Assuming you didn't make any other changes to the configuration and
your robot is reachable from nao.local, you should be able to connect
to the robot over HTTPS on port 9526.

https://nao.local:9526

If you robot does not have a host address, use its IP-address instead.
You can use the [index.html in local directory](remote-control/local/index.html) to
make this easier.

## Making things run automatically on NAO

You can add entries under `[program]` in
/home/nao/naoqi/preferences/autoload.ini for the two scripts so that
the remote is ready when NAO starts up.

```
[program]
/home/nao/remote_control/scripts/run_remote_naoqi.sh
/home/nao/remote_control/scripts/run_remote_web.sh
```

# Testing without a NAO

It's not possible to easily test the NAOqi parts without a NAO robot
or a simulator that speaks NAOqi. However, you can run the remote
control locally to see how that looks. Make sure you have a TLS
certificate for localhost (see [Installing a TLS
certificate](#installing-a-tls-certificate)) and that `server.conf`
knows where the certificate and keyfile are. Then, start
`run_remote_web.sh` and point your browser to https://localhost:9526

