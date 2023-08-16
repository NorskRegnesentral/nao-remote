var volumeOutput;
var session;


var hostname = window.location.hostname;
var socket = new WebSocket("wss://" + hostname + ":9526/websocket");

window.onload = function () { // a function that is done as soon as the page loads
    let muteButton = document.getElementById("muteButton");
    muteButton.addEventListener('click', event => {
	if (muteButton.getAttribute('aria-pressed') === 'true') {
	    muteButton.removeAttribute('aria-pressed');
	    socket.send("unmute");
	} else {
	    muteButton.setAttribute('aria-pressed', 'true');
	    socket.send("mute");
	}
    });
};


function onBtnPlaySound(){
    socket.send("check_connection");
};


function onBtnGreet() { // function that greets you
    socket.send("greet");
}

function onBtnBye() { // function that decides tells you to try again
    socket.send("goodbye");
}

function onBtnNextTask() { // function that decides the next task
    socket.send("next_task");
}

function onBtnTryAgain() { // function for a big celebration
    socket.send("try_again");
}

function onBtnSmallCheer() { // function that tells you to try again
    socket.send("small_cheer");
}

function onRobotDance() { // function for a big celebration
    socket.send("dance_robot");
}

function onChickenDance() { // function for a big celebration
    socket.send("dance_chicken");
}

function onDiscoDance() { // function for a big celebration
    socket.send("dance_disco");
}

function onMarcarena() { // function for a big celebration
    socket.send("dance_marcarena");
}

function onThinking() {
    socket.send("thinking");
}

function onInteresting() {
    socket.send("exciting_fun");
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
    socket.send("minus");
    
}

function onBtnLPlus() { // function to increase the volume
    clearMuteButton();
    socket.send("plus");
}

// function for making the robot wake up
function onBtnWakeUp(){
    socket.send("wake_up");
}

// function for making the robot rest
function onBtnRest(){
    socket.send("rest");
}

function onBtnRaiseHand() {
    socket.send("raise_hand");
}

// function to submit the text written by the user and that the robot has to say

function onBtnSend(){
    const behavior = "tts ";
    var to_speak = document.getElementById("speechText").value;
    socket.send(behavior.concat(to_speak));
}

function onBtnShutdown(){
    socket.send("shutdown");
}

function textEntered(event) {
    if (event.isComposing || event.keyCode === 229) {
	return;
    }
    if (event.keyCode === 13) {
	onBtnSend();
    }
}
