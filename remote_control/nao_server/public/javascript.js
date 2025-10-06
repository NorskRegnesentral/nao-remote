var volumeOutput;
var session;


var hostname = window.location.hostname;
var socket = new WebSocket("wss://" + hostname + ":9526/websocket");
var oobsocket = new WebSocket("wss://" + hostname + ":9526/oob");

function addToggleFunction(document, elementID, command1, command2, messageSocket = socket) {
    let button = document.getElementById(elementID);
    button.addEventListener('click', event => {
	if (button.getAttribute('aria-pressed') === 'true') {
	    button.removeAttribute('aria-pressed');
	    messageSocket.send(command1);
	} else {
	    button.setAttribute('aria-pressed', 'true');
	    messageSocket.send(command2);
	}
    });
}

window.onload = function () { // a function that is done as soon as the page loads
    addToggleFunction(document, "muteButton", "unmute", "mute", oobsocket);
    addToggleFunction(document, "autoButton", "no_autonomous_life", "autonomous_life");
};

function sendButtonMessage(value, messageSocket = socket) {
    messageSocket.send(value);
}

/*
function getVolume() { // function to get the volume from the robot
    QiSession(function (session) {
        session.service("ALAudioDevice").then(function (ALAudioDevice) {
            var promiseA = ALAudioDevice.getOutputVolume();
            promiseB = promiseA.then(function (value) {
                var volume = value;
                document.getElementById("volume").innerHTML = "Volume: " + volume + "%";
                volumeOutput = volume;
                console.log("Volume: " + volume + "%");
            });
        });
    });
}
*/

function clearMuteButton() {
    // If the volume buttons are pressed, remove the mute status
    // the mute is cleared on the server, so this just syncs the UI.
    // It should be OK to remove the attribute even when it isn't there.
    let muteButton = document.getElementById("muteButton");
    muteButton.removeAttribute('aria-pressed');
}

function onBtnLMinus() { // function to lower the volume
    clearMuteButton();
    sendButtonMessage("minus", oobsocket);
    
}

function onBtnLPlus() { // function to increase the volume
    clearMuteButton();
    sendButtonMessage("plus", oobsocket);
}

// function to submit the text written by the user and that the robot has to say

function onBtnSend(){
    const behavior = "tts ";
    var to_speak = document.getElementById("speechText").value;
    sendButtonMessage(behavior.concat(to_speak), socket);
}

function textEntered(event) {
    if (event.isComposing || event.keyCode === 229) {
	return;
    }
    if (event.keyCode === 13) {
	onBtnSend();
    }
}
