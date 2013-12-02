Mozilla Presence
================

This prototype implements https://wiki.mozilla.org/Services/Presence

Read the terminology at : https://wiki.mozilla.org/Services/Presence#Terminology

The server provides:

  * **Device Presence Channel**: used by *users* to send presence updates and
    get live notifications.
  * **Registration**: used by *AppDeveloper* to register applications
  * **AppService Presence Channel**: used by *AppService* to get presence
    updates and send live notifications.
  * **Permissions**: used to *users* manage applications permissions


Device Presence Channel
-----------------------

The Device Presence Channel is a web socket at *wss://server/presence*

It's a channel of communications between a phone/browser device and Mozilla
Presence that carries live notifications from Presence and presence data to
Presence.

### Presence updates

The device can update its presence by sending a JSON mapping containing 3
fields:

  * **email** - the Persona e-mail
  * **assertion** - a valid Persona assertion
  * **status** - the status: 'online', 'offline' or 'unavailable'

Example:

	{'email': 'tarek@mozilla.com',
	 'assertion': '<valid persona assertion>',
	 'status': 'online'}

For every presence status received, the server sends back an ACK message.

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

### Live notifications

The Presence server can send live notifications to the device.
When the server has some notifications pending for the device, they
will all be sent at once whenever the device is connected.

Live notifications are sent as a JSON mapping containing 1 key:

  * **notifications**: a list of notifications

A notification is a mapping with 3 keys:

  * **source**: the sender -- usually an e-mail
  * **message**: the message
  * **action**: the action -- can be an URL

Once the notifications are sent through the channel, they are discarded
from the server.



Registration
------------

XXX

AppService Presence Channel
---------------------------


The AppService Channel is a web socket at *wss://server/myapps/<appid>*

It's a channel of communication between Mozilla Presence and an AppService that
carries presence updates for users sharing their presence with the AppService
and live notifications from the AppService to be delivered to a PUID.

XXX


Permissions API
---------------

A user may grant an application to see their presence by performing a POST
call with the application unique identifier as provided by the application.

The server will keep track of this choice.

	POST /grant/<appid>

	XXX


