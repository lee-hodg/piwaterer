# Blynk

BlynkLib taken from https://github.com/vshymanskyy/blynk-library-python/blob/master/BlynkLib.py

To fix the ssl issue I found the following
https://github.com/vshymanskyy/blynk-library-python/pull/82 useful.
It was necessary to edit BlynkLib.py: instead of ssl.create_default_context(), we can use ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) to avoid the problem with ssl_create_default_context.

