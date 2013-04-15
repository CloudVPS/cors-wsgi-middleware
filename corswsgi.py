

DEFAULT_CONFIGURATION = {
    'allow_origin': '*',
    'allow_method': 'GET, POST, PUT, DELETE, OPTIONS',
    'allow_headers': 'Origin, Content-type, Accept, X-Auth-Token',
    'expose_headers': 'etag, x-timestamp, x-trans-id, vary',
    'allow_credentials':  'false',
    'hijack_options': 'true',
    'max_age': '3600',
}

TRUTHS = ("yes", "1", "on", "true")

class CorsMiddleware(object):
    "WSGI middleware allowing CORS requests to succeed"

    def __init__(self, application, conf):
        self.application = application

        self.allowed_origins = set(conf['allow_origin'].split())
        self.allowed_methods = set(method.strip().upper() for method in
                                   conf['allow_method'].split(','))
        self.hijack_options = conf['hijack_options'].strip().lower() in TRUTHS

        headers = {}
        headers['access-control-allow-origin'] = ' '.join(self.allowed_origins)
        headers['access-control-max-age'] = conf['max_age']
        headers['access-control-allow-methods'] = conf['allow_method']
        headers['access-control-allow-headers'] = conf['allow_headers']
        headers['access-control-expose-headers'] = conf['expose_headers']
        headers['access-control-allow-credentials'] = conf['allow_credentials']
        self.cors_headers = headers.items()


    def __call__(self, env, start_response):
        """
        Enforce the allow_origin option, and optionally hijack OPTIONS reqs.
        """
        origin = env.get("HTTP_ORIGIN")
        if origin:

            if origin not in self.allowed_origins and \
                    '*' not in self.allowed_origins:
                # Enforce access control
                status = '401 Unauthorized'
                start_response(status, [])
                return ["Invalid origin"]

            method = env['REQUEST_METHOD']

            if method not in self.allowed_methods:
                status = '401 Unauthorized'
                start_response(status, [])
                return ["Invalid method"]

            if self.hijack_options and method == 'OPTIONS':
                start_response('200 Ok', self.cors_headers)
                return []

            def inject_headers(status, headers, exc_info=None):
                return start_response(status, headers + self.cors_headers, exc_info)

            return self.application(env, inject_headers)
        else:
            return self.application(env, start_response)


def filter_factory(global_conf, **local_conf):
    """Standard filter factory to use the middleware with paste.deploy"""
    conf = DEFAULT_CONFIGURATION.copy()
    conf.update(global_conf)
    conf.update(local_conf)

    def cors_filter(app):
        return CorsMiddleware(app, conf)

    return cors_filter
