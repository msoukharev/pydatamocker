def assert_equals(expected, actual, message=None):
    full_msg = f"Expected: {expected}, Actual: {actual}."
    if message is not None and len(message) > 0:
        full_msg = f"{message}: {full_msg}"
    assert expected == actual, full_msg
