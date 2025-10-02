#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: BSD-2-Clause

"""
Python script for hosting a remote control for NAO v6. The script renders the
web page and communicates with the remote.py script through ZMQ sockets in order to send commands
to the NAO robot and make it execute the specified behaviours.
"""

import zmq
from zmq.eventloop import zmqstream

import configparser

import sys

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections
    setattr(collections, "MutableMapping", collections.abc.MutableMapping)

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
import ssl
import os
import typing

class RemoteApplication(tornado.web.Application):
    APP_ID = "no.nr.remote"
    BASE_DIR = os.path.join(os.path.sep, "var", "run", "user", str(os.getuid()))
    DIR_PATH = os.path.join(BASE_DIR, APP_ID) if os.path.exists(BASE_DIR) else os.path.join(os.path.sep, "tmp", APP_ID)

    def __init__(self, public_root: str):
        self.context = zmq.Context()  # Create a context (containter for all sockets in a process)
        self._test_and_make_dir()  # making directory for socket bindings
        self._connect_behavior_channel()  # binding to the behavior channel
        self._connect_confirmation_channel()  # binding to the confirmation channel
        self._connect_oob_channel()
        self.socket_clients = set()
        self.oob_clients = set()

        handlers = [
            (r'/', HelloWorldHandler),
            (r'/websocket', WebSocketHandler),
            (r'/oob', OobSocketHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': public_root}),
        ]

        settings = dict(
            debug=True,
            template_path=public_root,
            default_handler_class=NotFoundHandler
        )
        super(RemoteApplication, self).__init__(handlers, **settings)

    def cleanup(self):
        self.stream_sub.close()
        self.context.destroy()

    def _test_and_make_dir(self):
        """
        Making a directory for aiding the communication between the server and
        remote. The method creates the directory in /tmp if it doesn't already exist.
        """
        print(f"does {RemoteApplication.DIR_PATH} exist?")

        if not os.path.exists(RemoteApplication.DIR_PATH):
            print("No, make it")
            os.makedirs(RemoteApplication.DIR_PATH)

    def _connect_oob_channel(self):
        """ Creating a out-of-band publishing socket and binding it to the given address. """

        binding_address = "ipc://" + os.path.join(RemoteApplication.DIR_PATH, "oob")
        print("bind on {}", binding_address)

        self.socket_oob = self.context.socket(zmq.PUB)  # Creating a publisher socket
        self.socket_oob.bind(binding_address)  # Bind the socket to given address

        print("Connected to oob channel.")            
            
    def _connect_behavior_channel(self):
        """ Creating a publishing socket and binding it to the given address. """

        binding_address = "ipc://" + os.path.join(RemoteApplication.DIR_PATH, "behaviors")
        print(f"bind on {binding_address}")

        self.socket_beh = self.context.socket(zmq.PUB)  # Creating a publisher socket
        self.socket_beh.bind(binding_address)  # Bind the socket to given address

        print("Connected to behavior channel.")

    def _connect_confirmation_channel(self):
        """
        Creating a subscriber socket for receiving confirmation messages
        from the remote and connecting to the given address in order to
        communicate with the remote.

        We also create a stream for listening for messages from the remote. When
        the remote sends a message it is received and the "process_message"
        method is invoked.
        """

        self._test_and_make_dir()
        connection_address = "ipc://" + os.path.join(RemoteApplication.DIR_PATH, "cmd_status")
        print(f"connect on {connection_address}")
        self.socket_status = self.context.socket(zmq.SUB)  # subscriber socket
        self.socket_status.connect(connection_address)  # connecting to the correct address
        self.socket_status.setsockopt_string(zmq.SUBSCRIBE, "")  # specifying topic it should listen to

        self.stream_sub = zmqstream.ZMQStream(self.socket_status)
        self.stream_sub.on_recv(self._process_message)  # starts listening for messages on this channel

        print("Connected to task confirmation channel.")

    def _process_message(self, msg: list[bytes]):
        """
        Message handler: when a confirmation message is sent from the remote,
        this method is invoked and prints out a message to the user.

        Args:
            msg (list): the message sent by the remote
        """

        decoded_msg = msg[0].decode("utf-8")
        if decoded_msg == "Behavior finished":
            print("Successfully completed task :)\n")
        else:
            print("The task failed for some reason :(\n")

        

class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
    def put(self):
        self.write("Called put!")


class NotFoundHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_status(404)

    def get(self):
        self.write("Not Found.")

    def post(self):
        self.write("Not Found.")


class OobSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        """ Function running as soon as the webpage is opened/refreshed. """

        print("Connection opened...")
        self.application.oob_clients.add(self)  # adding this as a client

    def on_message(self, msg):
        """
        Processes the message sent from the webpage. When the user has pressed a
        button, the corresponding message is sent to the server. The server then
        sends the message to the remote in order to execute the wanted behavior.

        Args:
            msg (str): a text describing the behaviour to be executed
        """
        """
            encoded = msg.encode("utf-8")
            print(encoded)
            decoded = str(encoded.decode("utf-8"))
            print(decoded)
        """
        print("Sending oob: " + msg)
        self.application.socket_oob.send_string(msg)  # sending a message on the socket to remote-script

    def on_close(self):
        """ Method to execute when the connection to the webpage is closed. """
        self.application.oob_clients.remove(self)
        print("Connection closed...")

        
class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True


    def open(self):
        """ Function running as soon as the webpage is opened/refreshed. """

        print("Connection opened...")
        self.application.socket_clients.add(self)  # adding this as a client

    def on_message(self, msg):
        """
        Processes the message sent from the webpage. When the user has pressed a
        button, the corresponding message is sent to the server. The server then
        sends the message to the remote in order to execute the wanted behavior.

        Args:
            msg (str): a text describing the behaviour to be executed
        """
        """
            encoded = msg.encode("utf-8")
            print(encoded)
            decoded = str(encoded.decode("utf-8"))
            print(decoded)
        """
        print("Sending behavior: " + msg)
        self.application.socket_beh.send_string(msg)  # sending a message on the socket to remote-script

    def on_close(self):
        """ Method to execute when the connection to the webpage is closed. """
        self.application.socket_clients.remove(self)
        print("Connection closed...")


def read_config() -> tuple[str, int, str, str, str]:
    real_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    config_path = os.path.join(real_file_path, "conf", "server.conf")
    if not os.path.exists(config_path):
        print(f"No configuration file found at {config_path}. Using defaults.")

    config_parser = configparser.ConfigParser()
    config_parser.read(config_path)
    section_name = "nao-remote-server"
    hostname = config_parser.get(section_name, "hostname", fallback="nao1.ad.nr.no")
    port = config_parser.getint(section_name, "port", fallback=9526)
    keyfile = config_parser.get(section_name, "keyfile",
                                fallback=os.path.join(real_file_path, "certs", hostname+".key"))

    if not os.path.exists(keyfile):
        print(f"Could not find certificate key file at {keyfile}. "
              "Script will likely end in error.")
    certfile = config_parser.get(section_name, "certfile",
                                 fallback=os.path.join(real_file_path, "certs",
                                                       hostname.replace('.', '_') + "_cert.cer"))
    if not os.path.exists(certfile):
        print(f"Could not find certificate file at {certfile}. "
              "Script will likely end in error.")

    public_root = config_parser.get(section_name, "public_root",
                                    fallback=os.path.join(real_file_path, "public"))

    return hostname, port, keyfile, certfile, public_root

    # print(f"I got these values: host {hostname}, port {port}, keyfile {keyfile}, certfile {certfile}"
          #)


def main():
    # Collect the configuration from the config file
    _, port_number, keyfile, certfile, public_root = read_config()

    # print(f"  sorted! got these values: port {port_number}, keyfile {keyfile}, certfile {certfile}"
          #)

    application = RemoteApplication(public_root)
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # I assume that you don't have all complete chain. So, I use the
    # "chain" file. If you do have the CA in your OS's, you can just
    # use the single certificate.
    ssl_ctx.load_cert_chain(certfile, keyfile)

    server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_ctx)
    server.listen(port_number)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
