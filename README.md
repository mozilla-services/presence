Mozilla Presence
================

This prototype implements https://wiki.mozilla.org/Services/Presence


Presence API
------------

The presence API is a web socket at wss://<server>/presence

The client can connect to this end point and send presence updates.

A Presence update is a JSON mapping containing 3 fields:

  * **email** - the Persona e-mail
  * **assertion** - a valid Persona assertion
  * **status** - the status: 'online', 'offline' or 'unavailable'


Example:

   {'email': 'tarek@mozilla.com',
    'assertion': '<valid persona assertion>',
    'status': 'online'}


For every status received, the server sends back an ACK message.

Example:

    {'result': 'OK'}


In case of an error, the server may send back an extra 'errno' field with an
error code (codes to be documented) and an optional 'error' message.

Example:

    {'result': 'KO', 'errno': 34, 'error': 'Invalid assertion'}

The user can send as many updates as it wants, but the server can ask it to slow
down with a specific error code (codes to be documented)

The server or the user can disconnect from the socket at any time and for any
reason. The number of socket connections is limited to one connection per device
and per email.
