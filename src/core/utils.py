
def apply_intervals_filter(
    target, min_value, max_value, size, on_failure_cb = None
):
    print(target)
    print(min_value)
    print(max_value)
    
    if not (target >= min_value and target <= max_value):
        raise "The value entered exceeded the limits"

    if (target - min_value) % size != 0:
        if on_failure_cb:
            return on_failure_cb(target)
        raise "The value entered is invalid"

    return target, target


def find_valid_range(value, portion = 0):
    """ Finds up/down portion which its module is 0 """
    lower = int(value / portion) * portion
    higher = lower + portion
    return lower, higher


def get_valid_range(value, min_value, max_value, portion_size):
    """ Returns valid up/down values of given value and rules """
  
    return apply_intervals_filter(
        value, 
        min_value=min_value,
        max_value=max_value, 
        size=portion_size,
        on_failure_cb=lambda v: find_valid_range(v, portion_size),
    )