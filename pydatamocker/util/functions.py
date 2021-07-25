def compose(apply: bool = True, *funcs, **kwargs):
    f = funcs[0]
    for func in funcs[1:]:
        f = func(f)
    return f(**kwargs) if apply else f
