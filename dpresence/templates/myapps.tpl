<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="/js/jquery-1.7.2.min.js"></script>
  <script src="/js/persona.js"></script>
  <link rel="stylesheet" media="all" href="/css/presence.css"/>

</head>
<body>
<header id="login">
  <h1 class="title">My apps</h1>
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

%for app in apps:
  <div class="app">
  <h4>{{app.name}}</h4>
  <p>{{app.description}}</p>
  <div>Domain: <a href="{{app.domain}}">{{app.domain}}</a></div>
  %if app.valid_domain:
  <div>
    API Key:
    <pre>{{app.api_key}}</pre>
  </div>
  <div>
  <form action="activate_app" method="POST">
    %if not app.notified:
    {{app.name}} does not receive presence notifications.

    <input type="submit" name="activate" value="Activate"/>
    %end
    %if app.notified:
    {{app.name}} receives presence notifications.

    <input type="submit" name="deactivate" value="Deactivate"/>
    %end
    <input type="hidden" name="name" value="{{app.name}}"/>
  </form>
  </div>

  </div>
  %end

  %if not app.valid_domain:
  <strong>Not validated</strong>
  <p>To validate the application, you need to add a file at
  <i>{{app.domain}}/__presence</i> with this content</p>

  <pre>{{app.domain_key}}</pre>

  <p>Then click on the validate button below</p>

  <form action="validate_app" method="POST">
    <button name="validate">Validate</button>
    <input type="hidden" name="name" value="{{app.name}}"/>
  </form>

  %end
  </div>
%end

<div class="add">
  <h4>Add a new app</h4>

  <form action="" method="POST">
   <div>
    <label for="name">Name</label>
    <input name="name" type="text"/>
   </div>
   <div>
    <label for="domain">Domain</label>
    <input name="domain" type="text"/>
   </div>
   <div>
    <label for="description">Description</label>
    <input name="description" type="text"/>
   </div>

   <div class="submit">
    <input name="submit" type="submit"/>
   </div>
   <div style="clear: both"></div>
  </form>
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
      url: '/login',
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
      url: '/logout', // This is a URL on your website.
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

