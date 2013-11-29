
function loadApps() {
  $.getJSON("getApps", function(data) {
     var ul = "<ul id='applist'>";
     $.each(data.apps, function(key, app) {
       var revoke = "<button onclick=\"revokeApp('" + app.uid + "')\">";
       revoke += "Revoke</button>";

       ul += '<li>' + app.name + revoke + '</li>\n';
       }
     );
    ul += '</ul>';
    $('#applist').replaceWith(ul);
  });
}

function revokeApp(appid) {
  $.getJSON("/revoke/" + appid, function(data) {
     if (data.result == 'OK') {
       loadApps();
     } else {
       alert(data.result);
     }
  });

}

var signinLink = document.getElementById('signin');
if (signinLink) {
  signinLink.onclick = function() { navigator.id.request(); };
}

var signoutLink = document.getElementById('signout');
if (signoutLink) {
    signoutLink.onclick = function() { navigator.id.logout(); };
    }

var currentUser = null;
var ws = new WebSocket('ws://localhost:8282/presence');

ws.onmessage = function(evt) {
  var data = jQuery.parseJSON(evt.data);

  if (data.status=='notification') {
    $.each(data.notifications, function(key, notification){
       notify(notification.message);
    });
    return;
  }
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
        $('#apps').show();
        loadApps();
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
        /*$('#signin').show();
        $('div.status').hide();
        $('#signout').hide();
        $('#user').text('');
        currentUser = null;
        */
        window.location.reload();
      },
      error: function(xhr, status, err) { alert("Logout failure: " + err); }
    });
  }
});

var baselocation = location.href.substr(0, location.href.indexOf("sidebar"));

function notify(msg) {
  var port = navigator.mozSocial.getWorker().port;
  data = {
    id: "foo",
    type: null,
    body: msg,
    action: "link",
    actionArgs: {
        toURL: baselocation + "redirect?url=http://localhost:8080"
      }
    }
    port.postMessage({topic:"social.notification-create", data: data});
}

