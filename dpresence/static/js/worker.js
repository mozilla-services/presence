
var apiPort;
var ports = [];

onconnect = function(e) {
    var port = e.ports[0];
    ports.push(port);
    port.onmessage = function (msgEvent)
    {
        var msg = msgEvent.data;
        if (msg.topic == "social.port-closing") {
            if (port == apiPort) {
                apiPort.close();
                apiPort = null;
            }
            return;
        }
        if (msg.topic == "social.initialize") {
            apiPort = port;
            initializeAmbientNotifications();
        }
        if (msg.topic == "social.user-profile") {
		console.log(data);
            if (data.userName) { 
               userIsConnected(data);
            }
			else {
  			 userIsDisconnected();
			}
        }

    }
}


function userIsConnected(userdata)
{
  console.log(userdata);
}

function userIsDisconnected()
{
}


// XXX move to sidebar.js
messageHandlers = {
  "social.user-profile": function(data) {
    if (data.userName)
      userIsConnected(data);
    else
      userIsDisconnected();
  }
};

navigator.mozSocial.getWorker().port.onmessage = function onmessage(e) {
    //dump("SIDEBAR Got message: " + e.data.topic + " " + e.data.data +"\n");
    var topic = e.data.topic;
    var data = e.data.data;
		console.log(data + ' 2');

    if (messageHandlers[topic])
        messageHandlers[topic](data);
    if (topic && topic == "social.port-closing") {
      dump("!!!!!!!!! port has closed\n");
    }
};


// send a message to all provider content
function broadcast(topic, data) {
  for (var i = 0; i < ports.length; i++) {
    ports[i].postMessage({topic: topic, data: data});
  }
}


