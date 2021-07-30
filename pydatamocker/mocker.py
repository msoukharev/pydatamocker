mocker_config = {}


def config(**kwargs):
    mocker_config.update(kwargs)


def get_config(key):
    return mocker_config.get(key)
