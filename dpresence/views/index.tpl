<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="/js/jquery-1.7.2.min.js"></script>
  <script src="/js/persona.js"></script>
</head>
<body>
  <fieldset>
    <legend>Login</legend>
    %if session.get('logged_in'):
    <div>
      <strong>Logged in as <span id="user">{{session['email']}}</span></strong>
      <button id="signout">Sign Out</button>
    </div>


    %else:
    <div>
      <strong>Logged in as <span id="user">no one</span></strong>

      <button id="signin">Sign In</button>
      <button id="signout" style="display: none">Sign Out</button>
    </div>

    %end
  </fieldset>
  <fieldset>
    <legend>Status</legend>

  <div>
    <strong id="status">offline</strong>
    <button id="online">Go Online</button>
    <button id="offline">Go Offline</button>
  </div>

  </fieldset>
  <fieldset>
    <legend>Apps permissions</legend>

  </fieldset>

<script>
      var signinLink = document.getElementById('signin');
      if (signinLink) {
          signinLink.onclick = function() { navigator.id.request(); };
        }

        var signoutLink = document.getElementById('signout');
        if (signoutLink) {
            signoutLink.onclick = function() { navigator.id.logout(); };
          }


%if session.get('logged_in'):
var currentUser = '{{session['email']}}';
%else:
var currentUser = null;
%end


    var ws = new WebSocket('ws://localhost:8080/presence');
      ws.onmessage = function(evt) {
        var data = jQuery.parseJSON(evt.data);
        $('#status').text(data.status);
      };

    $('#online').click(function(){
      ws.send(JSON.stringify({'status': 'online', 'user': currentUser}));
    });
    $('#offline').click(function(){
      ws.send(JSON.stringify({'status': 'offline', 'user': currentUser}));
    });



navigator.id.watch({
  loggedInUser: currentUser,
  onlogin: function(assertion) {
    $.ajax({
      type: 'POST',
      url: '/login',
      dataType: 'json',
      data: {assertion: assertion},
      success: function(res, status, xhr) {
        console.log('success');
        $('#signin').hide();
        $('#signout').show();
        $('#user').text(res.email);
        currentUser = res.email;
      },
      error: function(xhr, status, err) {
        navigator.id.logout();
        alert("Login failure: " + err);
      }
    });
  },
  onlogout: function() {
    $.ajax({
      type: 'POST',
      url: '/logout', // This is a URL on your website.
      success: function(res, status, xhr) {
        console.log('success logout');

        window.location.reload(); },
      error: function(xhr, status, err) { alert("Logout failure: " + err); }
    });
  }
});
    </script>

</body>
</html>

