def assert_range_numeric(x, start, stop):
    if x is None:
        return
    if int(x) not in range(start, stop):
        raise ValueError("value must be between " + str(start) + " and " + str(stop))
