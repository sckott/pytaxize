from functools import reduce


def assert_range_numeric(x, start, stop):
    if x is None:
        return
    if int(x) not in range(start, stop):
        raise ValueError("value must be between " + str(start) + " and " + str(stop))


def str2list(x):
    if isinstance(x, str):
        nametmp = list()
        nametmp.append(x)
        x = nametmp
    if not isinstance(x, list):
        raise TypeError("'x' must be of class list")
    return x


def flatten(l):
    return reduce(lambda x, y: x + y, l)


def lists2dict(vals, names):
    if not isinstance(vals, list):
        raise TypeError("'vals' must be of class list")
    if not isinstance(names, list):
        raise TypeError("'names' must be of class list")
    return dict(zip(names, vals))
