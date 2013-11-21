<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="/js/jquery-1.7.2.min.js"></script>
  <script src="/js/persona.js"></script>
  <link rel="stylesheet" media="all" href="/css/presence.css"/>

</head>
<body style="width: 300px; height: 400px">


<header id="login">
  <h1 class="title">Mozilla Presence</h1>
  <span id="user">{{session.get('email', '')}}</span>

    <div>
      <p>
%if session.get('logged_in'):
        <a href="#" id="signin" style="display: none">
          <img src="/img/persona_sign_in_blue.png" alt="Sign in with Persona">
        </a>
%else:
        <a href="#" id="signin">
          <img src="/img/persona_sign_in_blue.png" alt="Sign in with Persona">
        </a>

%end
      </p>
    </div>
%if session.get('logged_in'):
      <button id="signout">Sign Out</button>
%else:
      <button id="signout" style="display: none">Sign Out</button>
%end
</header>

%if session.get('logged_in'):
  <div class="status"><span id="status">offline</span>
%else:
  <div class="status" style="display: none"><span id="status">offline</span>
%end
   <div>
    <button id="online">Go Online</button>
    <button id="offline">Go Offline</button>
   </div>
  </div>

  <script>
var signinLink = document.getElementById('signin');
if (signinLink) {
  signinLink.onclick = function() { navigator.id.request(); };
}

var signoutLink = document.getElementById('signout');
if (signoutLink) {
    signoutLink.onclick = function() { navigator.id.logout(); };
    }
console.log('here');

%if session.get('logged_in'):
var currentUser = '{{session['email']}}';
%else:
var currentUser = null;
%end

var ws = new WebSocket('ws://localhost:8282/presence');
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
        $('#signin').hide();
        $('div.status').show();
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
        $('#signin').show();
        $('div.status').hide();
        $('#signout').hide();
        $('#user').text('');
        currentUser = null;
      },
      error: function(xhr, status, err) { alert("Logout failure: " + err); }
    });
  }
});


    </script>

</body>

</html>

