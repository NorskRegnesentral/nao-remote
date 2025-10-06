Put your certificates in this directory. You can generate a
self-signed certificate on NAO by running openssl from a SSH session.

openssl req -x509 -nodes -newkey rsa:2048 -keyout /home/nao/remote_control/nao_server/certs/nao.local.key -out /home/nao/remote_control/nao_server/certs/nao_local_cert.cer -days 365 -subj "/CN=nao.local"
