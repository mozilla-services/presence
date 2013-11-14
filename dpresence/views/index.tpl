<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8">
  <title>{{title}}</title>
  <script src="/js/jquery-1.7.2.min.js"></script>
  <script src="/js/browserDetection.js"></script>
</head>
<body>
  <h1>Mozilla Presence</h1>
 <p>To get started on Mozilla Presence, click the button to add it to Firefox:
   <button onclick="browserDetection.activateSocial(this)">Activate Presence</button>
 </p>
 <script>
   browserDetection.initialize();
 </script>

</body>
</html>

