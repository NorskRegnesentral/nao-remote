#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python script for a remote control application for NAO5 and NAO6.
"""

import stk.runner
import stk.events
import stk.services
import stk.logging

import os
import zmq


class Remote(object):
    APP_ID = "no.nr.remote"
    DIR_PATH = os.path.join(os.path.sep, "var", "run", "user", str(os.getuid()), APP_ID)

    def __init__(self, qiapp):
        self.qiapp = qiapp
        self.events = stk.events.EventHelper(qiapp.session)
        self.s = stk.services.ServiceCache(qiapp.session)
        self.current_volume = 50
        self.muted = False
        self.s.ALAudioDevice.setOutputVolume(self.current_volume)
        self.logger = stk.logging.get_logger(qiapp.session, Remote.APP_ID)
        # Nao5 doesn't have /var/run, so use tmp instead.
        if not os.path.exists(os.path.join(os.path.sep, "var", "run" "user")):
            Remote.DIR_PATH = os.path.join(os.path.sep, "tmp", Remote.APP_ID)

    def get_volume(self):
        """
        Getting the current volume of the speakers on the robot.

        Return:
            current_volume (long (float)): current volume
        """
        return self.current_volume

    def increase_volume(self):
        """ Increasing the volume of the robot speakers by 5%. """

        self.muted = False
        self.current_volume += 5
        self.s.ALAudioDevice.setOutputVolume(self.current_volume)

    def decrease_volume(self):
        """ Decreasing the volume of the robot speakers by 5%. """

        self.muted = False
        self.current_volume -= 5
        self.s.ALAudioDevice.setOutputVolume(self.current_volume)

    def text_to_speech(self, behavior_name, language="Norwegian", speed=50.0):
        """
        Making the robot say what is given in the text box on the
        webpage. For now, the robot will pronounce the words in
        Norwegian only and at a fixed speed of 50, but it is possible
        to make the speed and language easily changeable, for example
        from the webpage.
        """

        self.s.ALTextToSpeech.setLanguage(language)

        # Speed must me changed as part of the text. There is a
        # parameter for speed, but that only works for Japanese.

        # then behavior_name contains the string "tts" and the text itself in one string
        # removing "tts " from the string
        to_speak = behavior_name.replace("tts ", "")
        encoded = to_speak.encode("utf-8")
        to_speak = "\RSPD=" + str(speed) + "\  " + encoded + " \RST\ "
        self.s.ALTextToSpeech.say(to_speak)

    def muteRobot(self, mute):
        self.muted = mute
        if self.muted:
            self.s.ALAudioDevice.setOutputVolume(0)
        else:
            self.s.ALAudioDevice.setOutputVolume(self.current_volume)

    def behavior_to_run(self, behavior_name):
        """
        Function that runs the behavior that corresponds to the
        button pressed on the remote webpage. The idea is (for now at
        least) to check what the behavior is and then run it with the
        correct service.

        Args:
            behavior_name (string): the name of the behavior to be run

        """

        if behavior_name == "wake_up":
            self.s.ALMotion.wakeUp()  # the robot wakes up and stands up

        elif behavior_name == "rest":
            self.s.ALMotion.rest()  # the robot sits down in crouch position

        elif behavior_name == "shutdown":
            self.s.ALSystem.shutdown()  # the robot is shut down

        elif behavior_name == "plus":
            self.increase_volume()  # increasing the volume

        elif behavior_name == "minus":
            self.decrease_volume()  # decreasing the volume

        elif behavior_name == "mute" or behavior_name == "unmute":
            self.muteRobot(behavior_name == "mute")

        elif "tts" in behavior_name:  # the robot speaks the given text
            self.text_to_speech(behavior_name)

        # if it's none of the above, it's supposed to be run with the ALBehaviorManager service
        # it is then a choregraphe project that is run
        else:
            self.s.ALBehaviorManager.runBehavior("nr_remote_control/" + behavior_name)

    def connect_behavior_channel(self):
        """
        Creating a subscriber socket for receiving messages from the server and
        connecting to the given address in order to do this. These messages contain the
        robot behavior to be executed.
        """
        connection_address = "ipc://" + os.path.join(Remote.DIR_PATH, "behaviors")
        self.test_and_make_dir()
        self.socket_beh = self.context.socket(zmq.SUB)  # creating a subscriber socket
        self.socket_beh.setsockopt(zmq.SUBSCRIBE, "")  # specifying which topic to subscribe to
        self.socket_beh.connect(connection_address)  # connecting to address

        print("Connected to behavior channel.")

    def connect_confirmation_channel(self):
        """
        Creating a publisher socket for sending messages back to the server and binding
        to the given address. These messages contain a confirmation that the remote has
        received the behavior and the robot has done it.
        """

        binding_address = "ipc://" + os.path.join(Remote.DIR_PATH, "cmd_status")
        self.socket_status = self.context.socket(zmq.PUB)  # making a pair socket
        self.socket_status.bind(binding_address)

        print("Connected to task confirmation channel.")

    def test_and_make_dir(self):
        """
        Making a directory for aiding the communication between the server and
        remote. The method creates the directory in /tmp if it doesn't already exist.
        """

        if not os.path.exists(Remote.DIR_PATH):
            os.makedirs(Remote.DIR_PATH)

    def on_start(self):
        """
        The code that should be run as soon as the script is run. This includes
        creating the neccessary sockets for communication and binding/connecting to
        the correct addresses and then listening for messages from the server.
        Whenever a message is received, the behavior is run on the robot and
        a confirmation message is sent back.
        """

        self.context = zmq.Context()  # creating a context
        self.connect_behavior_channel()
        self.connect_confirmation_channel()

        while True:
            behavior_name = self.socket_beh.recv_string()  # receiving behavior name on the socket

            print("Received behavior to execute: " + behavior_name)
            self.behavior_to_run(behavior_name)

            print("Sending confirmation...\n")
            self.socket_status.send_string("Behavior finished")

        self.stop()

    def stop(self):
        "Standard way of stopping the application."

        self.qiapp.stop()

    def on_stop(self):
        "Cleanup"
        self.context.destroy()
        self.logger.info("Application finished.")
        self.events.clear()


if __name__ == "__main__":
    stk.runner.run_activity(Remote)
