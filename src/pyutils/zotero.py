def update_item_added_date(session, key, date):
    query = ItemQueryByKey(key)
    item = session.get(query).json()

    previous_date = item["data"]["dateAdded"]
    new_date = date.strftime("%Y-%m-%dT%H:%M:%SZ")
    if previous_date != new_date:
        item_updater = ItemUpdater(item)
        req = session.put(item_updater)
