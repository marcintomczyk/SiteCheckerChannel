=====
Checker Channel
=====

The Checker Channel is an app based on Django Channels allowing to extend the simple 'site-checker' application with communication via websockets

Key things to note:
- redis is required as a broker. One of the simplest way to run it is to use default docker image
 - docker run -p 6379:6379 -d redis - in case there is no redis image available locally it should be automatically pulled for the first time (if not, one can execute 'docker pull redis' explicitly)
 
- some things must be added to the main project:
 - add file routing.py with the following content:
  application = ProtocolTypeRouter({
     # (http->django views is added by default)
     'websocket': AuthMiddlewareStack(
         URLRouter(
             checker_channel.routing.websocket_urlpatterns
         )
     ),
    })
 - add to the settings.py
  - to the INSTALLED_APP add the following entries:
   - 'channels' #for django-channels
   - 'checker_channel' # for our new application
  - to the end of file add the following:
    # Channels
    ASGI_APPLICATION = 'egnytex.routing.application'
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('127.0.0.1', 6379)],
            },
	    },
    }
 - to the urls.py add the following path:
  - path('checker_channel/', include('checker_channel.urls')),
