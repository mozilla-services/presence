<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<title>{{title}}</title>
		<script src="/js/jquery-1.7.2.min.js"></script>
		<script>
			$(function(){
				if (!window.WebSocket) {
					if (window.MozWebSocket) {
						window.WebSocket = window.MozWebSocket;
					} else {
						alert('Your browser doesn\'t support WebSockets.');
					}
				}

				var ws = new WebSocket('ws://localhost:8080/++presence++');
			});
		</script>
	</head>
	<body>Presence notified to the server.
	</body>
</html>

