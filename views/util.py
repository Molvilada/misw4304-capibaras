from flask import request

def class_route(self, rule, **options):
    def decorator(cls):
        self.add_url_rule(rule, view_func=cls.as_view(cls.__name__), **options)
        return cls

    return decorator

def get_token():
    header = request.headers.get('Authorization')
    if header is None:
        return None
    
    header = header.split(' ', 1)
    if len(header) != 2:
        return None
    
    method, token = header

    if method != 'Bearer':
        return None

    return token
