def float_range(start: float, end: float=None, step: float=1):
    if not end:
        end = start
        start = 0.0
    counter = start
    range_ = list()
    while counter < end:
        range_.append(counter)
        counter += step
    return range_
