cors-wsgi-middleware
====================

WSGI Middleware for enabling Cross Origin Resource Requests.

Paste configuration:

    [filter:cors_wsgi]
    paste.filter_factory = corswsgi:filter_factory
    allow_origin: *
    allow_method: GET, POST, PUT, DELETE, OPTIONS
    allow_headers: Origin, Content-type, Accept, X-Auth-Token
    expose_headers: etag, x-timestamp, x-trans-id, vary
    allow_credentials:  false
    hijack_options: true
    max_age: 3600



