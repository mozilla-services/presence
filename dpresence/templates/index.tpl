<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="/js/jquery-1.7.2.min.js"></script>
  <script src="/js/browserDetection.js"></script>
  <link rel="stylesheet" media="all" href="/css/presence.css"/>

</head>
<body>
 <header id="login">
  <h1 class="title">Mozilla Presence</h1>
 </header>

 <h2>User</h2>
 <p>To install the Mozilla Presence sidebar, click the button to add it to Firefox</p>
  <button onclick="browserDetection.activateSocial(this)">Activate Presence</button>

 <h2>Developer</h2>
 <p>To manage your own Presence-aware applications, go to your <a href="/myapps">My Apps</a> page
 </p>

 <script>
   browserDetection.initialize();
 </script>

</body>
</html>

