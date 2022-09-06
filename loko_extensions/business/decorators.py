import functools


def extract_value_args(f):
    @functools.wraps(f)
    def temp(*args, **kwargs):
        if len(args) > 0:
            request = args[0]
        args = request.json.get('args')
        value = request.json.get("value")
        return f(value, args)

    return temp
