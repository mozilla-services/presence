<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="{{root_url}}/js/jquery-1.7.2.min.js"></script>
  <script src="{{root_url}}/js/persona.js"></script>
  <link rel="stylesheet" media="all" href="{{root_url}}/css/presence.css"/>

</head>
<body style="width: 300px; height: 400px">
<header id="login">
  <h1 class="title">Mozilla Presence</h1>
  <span id="user">{{session.get('email', '')}}</span>

    <div>
      <p>
%if session.get('logged_in'):
        <a href="#" id="signin" style="display: none">
          <img src="{{root_url}}/img/persona_sign_in_blue.png" alt="Sign in with Persona">
        </a>
%else:
        <a href="#" id="signin">
          <img src="{{root_url}}/img/persona_sign_in_blue.png" alt="Sign in with Persona">
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

<form action="" method="POST">

  <h3>Allow ChatRoom to see when you are present ?</h3>
  <div>
    <input type="hidden" name="redirect" value="{{redirect}}"/>
    <input type="submit" name="allow" value="Yes"/>
    <input type="submit" name="disallow" value="No"/>
  </div>
</form>


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



navigator.id.watch({
  loggedInUser: currentUser,
  onlogin: function(assertion) {
    $.ajax({
      type: 'POST',
      url: '{{root_url}}/login',
      dataType: 'json',
      data: {assertion: assertion},
      success: function(res, status, xhr) {
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
      url: '{{root_url}}/logout', // This is a URL on your website.
      success: function(res, status, xhr) {
        $('#signin').show();
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

