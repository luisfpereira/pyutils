

def transform_into_dict(items, id_key='id', remove_id=True):
    """Transforms list into dictionary based on 'id' field.

    Args:
        remove_id (bool): removes id from dict.
    """
    items_dict = {item[id_key]: item for item in items}

    if remove_id:
        for item in items:
            del item[id_key]

    return items_dict


def unravel_array(array):
    collector = []
    _unravel_array(array, collector)
    return collector


def _unravel_array(array, collector):
    if type(array) in [list, tuple]:
        for item in array:
            _unravel_array(item, collector)
    else:
        collector.append(array)


def count_repetitions(ls, thresh=1):
    reps = {}
    for item in set(ls):
        c = ls.count(item)
        if c >= thresh:
            reps[item] = c

    return reps
