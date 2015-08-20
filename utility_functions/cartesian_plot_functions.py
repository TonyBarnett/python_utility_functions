from numpy import mean


def _get_mean(y: list) -> float:
    return mean(y)


def _get_y_minus_y_hat(x: list, y: list, a: float, b: float, min_y: float=None) -> float:
    y_minus_y_hat = 0
    for i, y_i in enumerate(y):
        if min_y is not None and (a * x[i] + b) < min_y:
            y_minus_y_hat += min_y
        else:
            y_minus_y_hat += (y_i - (a * x[i] + b)) ** 2
    return y_minus_y_hat


def _get_y_minus_y_bar(y: list, yt: float) ->float:
    y_minus_y_bar = 0
    y_bar = mean(y)
    for y_i in y:
        y_minus_y_bar += (y_i - y_bar) ** 2
    return y_minus_y_bar


def get_r_squared(x: list, y: list, a: float, b: float, minimum_value_y: float=None) -> float:
    y_minus_y_hat = _get_y_minus_y_hat(x, y, a, b)
    yt = _get_mean(y)
    y_minus_y_bar = _get_y_minus_y_bar(y, yt)
    return 1 - (y_minus_y_hat / y_minus_y_bar)
