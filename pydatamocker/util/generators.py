# def configure(resolution_graph: dict, *required):
#     def traverse(obj: str, kwargs: dict):
#         for key, val in obj:
#             req = resolution_graph[key]
#             val = kwargs.get(key)
#         if not req:
#             return
#         if isinstance(req, (set, dict)):
#             if len(val) > 0 and not val in req:
#                 raise ValueError('Unsupported value ' + key) # TODO: handle tuples
#         if isinstance(req, (dict)):
#             next = req[val]
#             traverse(val, next)

#         spec = kwargs.get(key)
#         if not spec:
#             raise ValueError('Required argument missing ' + key)
#         if isinstance(spec, (dict)):
#             next =
#         if isinstance(spec, (tuple)):
#             kwargs[spec[0]] = spec[1]
#         elif isinstance(spec, (str)) and not kwargs.get(spec):
#             raise ValueError('Required argument missing' + spec)
#         else:
#             raise ValueError('Misconfigured generator resolution graph ' + resolution_graph)
#     def decorator(generator: function):
#         def transform(size: int, **kwargs):
#             for arg in required:
#                 if not arg in kwargs:
#                     raise ValueError('Required argument missing ' + arg)

#                 prockwargs = dict(kwargs)
#                 for key in resolution_graph:
#                     traverse(key, prockwargs)
#             return generator(size, **prockwargs)
#         return transform
#     return decorator
