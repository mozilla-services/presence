<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="/js/jquery-1.7.2.min.js"></script>
  <link rel="stylesheet" media="all" href="/css/presence.css"/>

</head>
<body>
 <header id="login">
  <h1 class="title">Mozilla Presence</h1>
 </header>

 <h2>User</h2>
 <p>To install the Mozilla Presence sidebar, click the button to add it to Firefox</p>
  <button onclick="activate(this)">Activate Presence</button>

 <h2>Developer</h2>
 <p>To manage your own Presence-aware applications, go to your <a href="/myapps">My Apps</a> page
 </p>

 <script>
    var loc = location.href;
    var baseurl = loc.substring(0,loc.lastIndexOf('/'));

    var data = {
    // currently required
    "name": "Presence Service",
    "iconURL": baseurl+"/img/presence16.png",
    "icon32URL": baseurl+"/img/presence32.png",
    "icon64URL": baseurl+"/img/presence64.png",
    "sidebarURL": baseurl+"/sidebar",
    "description": "Chat Room",
    "author": "Mozilla",
    "homepageURL": "https://wiki.mozilla.org/CloudServices/Presence",

    "workerURL": baseurl+"/js/worker.js",

    // optional
    "version": "1.0"
    }

    function activate(node) {
      var event = new CustomEvent("ActivateSocialFeature");
      node.setAttribute("data-service", JSON.stringify(data));
      node.dispatchEvent(event);
    }

 </script>

</body>
</html>

