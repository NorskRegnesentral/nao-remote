# Creating a remote control hosted on a webpage for NAO v6

## List of libraries and python versions you need to have installed for this project:
- pip
- python2 and python3
- pyzmq: pip install pyzmq (install in virtual environment on nao - more info below)
- git: sudo apt install git
- tornado (installed using the requirements file, in the virtual environment - more info below)
- virtualenv: pip install virtualenv

## To run this project, follow these steps:

1. Clone the repo from this link: https://code.nr.no/scm/git/nao-ros

2. Ssh into your robot, for example ssh nao@156.116.9.87.

3. Use `scripts/sync-remote` to sync the different bits over.

4. Create a virtual environment (more info below if needed) and activate it.

5. Go to the nao_server folder and install the requirements: pip install -r requirements.txt

6. Install the ZeroMQ library for python: pip install pyzmq

7. Set the encoding to utf8 in this session (best solution so far...): 
```
export PYTHONIOENCODING=utf8 # Add to .profile
```
8. In the terminal you are in, go to the nao-folder and run the server script: python3 server.py.

9. Open another terminal, activate the environment you just made, and export the encoding variable as above. In addition, you have to run: source scripts/activate-py2zmq.sh. 

10. In the second terminal, go to nao/app/scripts and run the remote script: python2 remote.py.


## To recreate this project, follow these steps:

SETUP:
PS: 

1. Clone the "Robot jumpstarter" github repository from this link: https://github.com/pepperhacking/robot-jumpstarter.git.
This repo helps you make a NAOqi application and contains all the necessary stuff. All you have to do is to decide on a template to use and then customize it after your needs. In my project i used the pythonapp-template. Follow these steps in order to create a pythonapp project:
```
    python jumpstart.py pythonapp *your-app-name*
```
This will create a project with your chosen name in the output folder of the robot-jumpstarter repo. PS: You can do this on your own computer, not necessarily on Nao.

2. Clone the template for the server from this github repository: https://code.nr.no/scm/git/rosa-tls-example

This repo consists of an example of how to create a tornado web server that is supposed to run on Nao. Follow these steps in order to get this basic server up and running on nao (you first have to ssh into Nao and you can transfer files from your machine using rsync).

1. Create a python3 environment on nao, like so:
```
        pip install virtualenv # (if you don't already have it)
        virtualenv -p /usr/bin/python3 *virtualenv_name* # (to create an environment for a specific version of python)
        source virtualenv_name/bin/activate # (to activate environment)
```
2. Install the required libraries for the server. Note these libraries will only be available inside the environment. Run this command:
```
        pip install -r requirements.txt
```    
3. Install the ZMQ library:
```	
	pip install pyzmq
```
4. Edit the server.py file to match the correct hostname (this is done for nao1.ad.nr.no) and certificate, and eventually change port for connection (it is currently 9526).
5. Run the server in a terminal:
```	
	./server.py
```
5. Check if you can connect from a browser: https://nao1.ad.nr.no:9526
(Note that nao1.ad.nr.no needs to be in DNS or your hosts file.)

If this works, you are ready to make changes to the server.py file and create a server suitable for your needs.

PS: If you want more info about this, read the server_info.txt file.
 
4. Combine these to repositories to make your application. This entails moving the application you made using the robot-jumpstarter out of the output folder and into the folder where the server is located (which is currently named rosa-tls-example).

The file structure should be something like this:

    - rosa-tls-example (give this folder a more suitable name...)
        - app -> from the robot-jumpstarter
            - folders with Choregraphe behavior files ... -> ADD YOUR OWN BEHAVIOR FILES
            - manifest.xml
            - remote.pml
            - scripts
                - main.py -> FILE THAT YOU HAVE TO ADAPT
                - stk -> contains helper files for the NAOqi application
        - certs -> contains certificates 
        - public -> contains front-end stuff
        - README.md
        - requirements.txt
        - server.py 

3. Clone the github repository: https://code.nr.no/scm/git/nao-ros

Here you will find two folders: rosa and scripts. You will have a script wirtten in python2 (the remote script) and another written in python3 (the server script), so the activate py2zqm.sh script will help you with this.

ACTUAL APPLICATION: 

Now that you have the skeleton of the project, it is time to code and develop the remote. I will walk you through the steps of what i did in the rest of this document.

The idea behind this project is to have a remote control on a webpage. Once you click on a button on the remote control, the robot has to perform that respective behavior. Behind the scenes, the webpage communicates with the server through a WebSocket (for more info: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API). When clicking on a button, a JavaScript function is called, which sends a message on this socket. This message is just a string describing what behavior the robot should do. The server then receives this message. Furthermore, the server communicates with the remote script through ZMQ sockets (for more info: https://zguide.zeromq.org/). On the server side we create a publisher sockets which the server uses to publish the messages sent over the WebSocket. On the remote side we create a subscriber socket that listens to messages from the server. When it receives a message, it uses the correct NAOqi service in order to make the robot perform that action. In addition, we create publisher socket on the remote side too. This socket is used to send back a confirmation message to the server after the action is done. On the server side we have a subscriber socket too, where we catch the confirmation message and print out a success message. So, this is how this project is wired together and how the multiple parts of it communicate together.

5. To create the remote application:

In the app-folder, the behaviors of the robot and the remote itself should be located. At this moment the app contains an example file for a NAOqi application, so you will need to customise it. This file is located in app/scripts and is named main.py. Here comes an explanation of the most important things in this file:

- This is a python2 script, as the NAOqi only works with python2. 
- main.py imports some other files located in app/scripts/stk that perform some magic, so if you intend to keep things simple, you don't have to worry about them. 
- There is an on_start() method which is called when the file is run. What this method should do is to create a ZMQ subscriber socket for receiving messages from the server and another ZMQ publisher socket to send messages back to the server. It should receive the message from the server which contains which behaviour we want to run on the robot and then actually run it on the robot using NAOqi services. The method should then send a confirmation back to the server on the publishing socket.
- The on_stop() method is called when the file is stopped. Here, we it is important that we destroy the ZMQ context in order to close all sockets in this process.

You can decide what the robot should do using specific NAOqi services. For instance, we can use the ALMotion service to make the robot wake up or rest using the wakeUp() and rest() functions respectively. This works fine for simple robot behaviors, but not for more complex behaviors. For the more complex behaviors like the dances, greetings etc. I have used Choregraphe to design the robots movements and what it should say. All these behaviors should be located inside the app-folder, where each behavior has its own folder containing a behavior.xar file. In the remote python file you can then use the ALBehaviorManager service to run the runBehavior() function to run the behavior files made with Choregraphe.
- The runBehavior() function takes the application ID and behavior name as an argument:"application_id/behavior_name". The application ID can be found in Choregraphe under the properties button to the left of the Choregraphe page. The names of the behaviors is also found to the left on the page.

6. To create the server:

The server is located in what is now called rosa-tls-example. It does some web magic that is not too important for us. What you should focus on is the WebSocketHandler class. Here is an explanation of the most important components:

- The make_dir() function should create a directory (which i called "nao_remote") inside the /tmp folder. On the server side we will bind the socket to an address, for instance "ipc:///tmp/nao_remote/behaviors", and on the remote side we will connect to the same address, allowing for communication between these two processes. Behavior messages will be posted and read on the behaviors "channel". We will do the same for the confirmation messages sent from the remote to the server. We let the publisher socket on the remote side bind to an address like "ipc:///tmp/nao_remote/cmd_status", while the server will connect to the same address. This means that confirmation messages will be posted and read on the cmd_status "channel".

- The open() function will be called once the server starts running. On opening the server, we should create a publisher socket for publishing behavior messages and a subscriber socket for receiving confirmation messages. The subscriber socket will start listening for messages from the remote. When a message is received, a function will be called, printing out a success message for the user.

- The on_message() function is called once the server receives a message on the WebSocket (so once a button is pressed). This message is passed on the publisher socket for the remote to receive.

- The on_close() function is called once the server is closed. Its task should be to close the stream (which is used to receive the confirmation messages) and destroy the context and thus close the sockets too.

Once you have written the remote script, server script, have the robot behaviors done, and the front-end part done, you are ready to start testing the project on Nao.

7. Connect to Nao and transfer project:
    - Connect to your Nao over ssh. For instance: ssh nao@156.116.9.87.
    - Transfer the project over to Nao. This can easily be done using rsync (https://phoenixnap.com/kb/how-to-rsync-over-ssh):
```    
        rsync ~/source_directory/ username@ip.address:~/destination_directory (for transferring directories)
        rsync ~/source_directory/filename username@ip.address:~/destination_directory (for transferring files).
```
    - Remember to also transfer the rosa folder and the scripts folder.

8. Run the project:

    - Open a terminal. This terminal will be devoted to running the server. There are a couple of things to do before actually running the file:
        - Activate the python3 environment: source ~/*virtualenv_name*/bin/activate
        - You need to set the encoding in this session to utf-8 in order to avoid problems: export PYTHONIOENCODING=utf8
        - Run the server: python3 server.py

    - Open another terminal. This one will be devoted to running the remote. There are some things you have to do here too:
        - Activate the python3 environment: source ~/*virtualenv_name*/bin/activate
        - Set the encoding in this session to utf-8 in order to avoid problems: export PYTHONIOENCODING=utf8
        - Source the python2 helper script: source ~/scripts/activate-py2zmq.sh
        - Run the remote: python2 remote_script_name.py

9. Connect to the web page, for instance by "https://nao1.ad.nr.no:9526", and start controlling your Nao.

## Improvement potential:

- More effective code
- The styling of the website 
- Battery and volume display on the website
FIXED Fix long delay after (Choregraphe) behavior (it is unclear whether the behavior just takes a long time or if there's some sort of problem)
- After clicking on "say now" button, the connection to the server opens and then closes - so this needs fixing eventually
- Maybe add a way of changing the language Nao speaks from the remote
- Add a way to change the speed when Nao talks
- Add more dances, movements and sayings that Nao can perform when clicking on a button on the remote
- Add functionality for the children to play with the remote as well



## Notes from Trenton

### 2022-09-01

Added a sync_remote.sh script to make it easier to copy code over.

Note about the remote from Choreographe. If there are changes done in
Choreographe. One needs to build this and install it on the Nao. We
should probably automate this as part of the sync script (using qipkg)[http://doc.aldebaran.com/2-8/dev/tutos/create_a_new_service.html?highlight=qipkg], but it can
also be done directly from Choreographe.

Also looked at cleaning up the repository a little. The older versions
of things have now been deleted. Look back in the history of you want
anything there again (which could be likely).

### Making things run automatically on NAO

You can add entries in /home/nao/naoqi/preferences/autoload.ini for the two scripts.

Looking something like:
```
[program]
/home/nao/rosa/scripts/run_remote_naoqi.sh
/home/nao/rosa/scripts/run_remote_web.sh
```
