var apiPort;


onconnect = function(e) {
    var port = e.ports[0];

    port.onmessage = function (msgEvent) {
       var msg = msgEvent.data;

       if (msg.topic == 'social.initialize') {
           apiPort = port;
           return;
       }
       else {
           apiPort.postMessage(msg);
       }
    }
}

// send a message to all provider content
function broadcast(topic, data) {
  for (var i = 0; i < ports.length; i++) {
    ports[i].postMessage({topic: topic, data: data});
  }
}


