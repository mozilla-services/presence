<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="/js/jquery-1.7.2.min.js"></script>
  <script>
  $(function() {

    var ws = new WebSocket('ws://localhost:8080/presence');
      ws.onmessage = function(evt) {
        var data = jQuery.parseJSON(evt.data);
        $('#status').text(data.status);
      };

    $('#online').click(function(){
      ws.send('online');
    });
    $('#offline').click(function(){
      ws.send('offline');
    });

  });
  </script>
</head>
<body>

  <div id="status">unknown</div>
  <div>
    <button id="online">Online</button>
    <button id="offline">Offline</button>
  </div>

</body>
</html>

