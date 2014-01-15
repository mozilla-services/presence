<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="/js/jquery-1.7.2.min.js"></script>
  <script>
  $(function() {

    var ws = new WebSocket('ws://presence.services.mozilla.com/_presence/_admin');
      ws.onmessage = function(evt) {
        $('#events').val($('#events').val() + '\n' + evt.data);
      };

  });
  </script>
</head>
<body>
  <h1>What's happening</h1>
  <textarea id="events" style="width: 100%; height: 100px"></textarea>
</body>
</html>

