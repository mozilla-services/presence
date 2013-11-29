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


 <div class="status" style="display: none">
  <h2 class="title">Status</h2>
  <span id="status">offline</span>
   <div>
    <button id="online">Go Online</button>
    <button id="offline">Go Offline</button>
   </div>
  </div>

  <div class="apps" id="apps" style="display: none">
    <h2 class="title">Apps permissions</h2>
    <ul id="applist">
    %for app in apps:
      <li>{{app['name']}}<button onclick="revokeApp('{{app['uid']}}')">Revoke</button>
    </li>
    %end
    </ul>
  </div>


<script>
%if session.get('logged_in'):
currentUser = '{{session['email']}}';
%else:
currentUser = null;
%end
</script>

  <script src="/js/presence.js"></script>



</body>

</html>

