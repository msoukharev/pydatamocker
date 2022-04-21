class TableException(Exception):
    pass

def NO_TITLE():
    raise TableException('Table must have a value for title')

def NO_SIZE():
    raise TableException('Table must have a value for size')
