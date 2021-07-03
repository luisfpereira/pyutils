

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
