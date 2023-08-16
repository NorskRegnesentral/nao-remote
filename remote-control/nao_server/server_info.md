# Simple test of a "Hello World" Tornado Server using TLS certificates

This repo has a very simple Tornado server. All it does is print
"hello world" upon getting a connection. The point is to get this to
run on a Nao6. The repo contains several certificates that we created
for testing in the `certs` directory. There is also a
`ca-chain.cert.pem` file for installing into an OS or browser to get
rid of warnings.

Here are the steps:

1. Copy an archive of the repo over Nao.
2. Install the required libraries: `pip install -r required.txt`
3. Edit server.py to match the correct hostname and certificate (done
   for robbie1.nr.no). Optionally, adjust the port for connection
   (currently 9526).
4. ./server.py and see if you can connect from your browser (e.g.,
   https://robbie1.nr.no:9526 )

If all this works, you have a starting point for going further. If you
want to interact with Nao, you probably (I hope) can `import naoqi`
and do it via python. Alternatively, you can use a websocket setup
that we used for the LanguageShower (check the services directory) and
have a Choreographe project that reads the json and does stuff with
it.

# TLS set up (in general)

This is more the basics of what we are doing here. You should be able
to use the included certificates and certificate chain without too
much trouble (depending on how strict hostname matching is).

It **is** possible to use transport security layer (TLS) connections
(previously known as SSL connections) on Nao. With NAO6, it is no
longer possible to become root, so you have to create it for users.
Here is the basic outline about how this would work.

1.  Agree on a well-known port that will be used on the NAO (it must
    be over 1000).
2.  Create a Python virtual environment and install tornado.
3.  Create certificates for Nao and copy them over into the virtual
    environment
4.  Create a simple tornado server, that creates an SSL context with
    the key and certificate and start listening with the server.
5.  Ensure that your client has the certificate authority for the
    certificates issued in step 3.

That really is all there is to it. Granted, creating (or buying)
certificates can be a chore.

For development, it doesn't make sense to be constantly buying
certificates. Further, self-signed certificates causes scary warning
messages as well. The best solution is to create a certificate
authority and create your own certificates. You add the certificate
from your certificate authority and then all the certificates are
trusted.

[Jamie
Nguyen](https://jamielinux.com/docs/openssl-certificate-authority/index.html)
has somewhat outdated (doesn't support Subject Alternative Names), but
correct information about how to create a certificate authority, an
intermediate certificate authority and generate certificates to your
heart's content. Another solution is to use OpenVPN's
[easy-rsa](https://github.com/OpenVPN/easy-rsa). Both require
[OpenSSL](https://www.openssl.org/) to be installed on the computer.
You will also have to add the certificate authority's certificate to
your browser's or operating system's certificate store.

# TLS certificate from NR and placement at schools.

NR can provide certificates for the ad.nr.no domain (e.g.
nao1.ad.nr.no), but this does require making a corresponding DNS A
record for the NAO's IP address, or alternatively putting an entry for
the robot's IP in the computers hosts file (/etc/hosts on Unix-like
systems or C:\Windows\System32\drivers\etc on Windows). When the NAO
is placed in a more permanent location, we quickly ask NR to update
its A record, assuming we get the same IP every time. This may mean we
will need to talk to the school and make sure that the NAO gets the
same IP every time it connects.
