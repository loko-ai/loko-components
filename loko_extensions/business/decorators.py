import functools
def extract_value_args(_request=None, file=False):
    """
       Decorator used to extract value and args from services.
       It works with Flask and Sanic frameworks.
    """
    def get_value_args(f):
        @functools.wraps(f)
        def tmp(*args, **kwargs):
            request = _request or args[0]
            value = request.files['file'] if file else request.json.get('value')
            args = request.files['args'] if file else request.json.get('args')
            ### flask ###
            if file and _request:
                args = args.read().decode()
            ### sanic ###
            elif file and not _request:
                args = args[0].body.decode()
            return f(value, args)
        return tmp
    return get_value_args
