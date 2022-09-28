from flask import current_app

def get_global_manager(primary_key, sub_key):
    sub_key_items = current_app.GlobalManager.get(primary_key)
    if sub_key_items is None:
        return None
    else:
        for item in sub_key_items:
            if item.get(sub_key,None) is not None:
                return item.get(sub_key)
        return None

def set_global_manager(primary_key, sub_key, sub_value):
    sub_key_items = current_app.GlobalManager.get(primary_key)
    if sub_key_items is not None:
        sub_key_items.append({sub_key: sub_value})
        current_app.GlobalManager.set(primary_key, sub_key_items)
    else:
        current_app.GlobalManager.set(primary_key, [{sub_key: sub_value}])

def global_manager_remove(primary_key, sub_key, sub_value):
    sub_key_items = current_app.GlobalManager.get(primary_key)
    if sub_key_items is not None:
        sub_key_items.append({sub_key: sub_value})
        current_app.GlobalManager.remove(primary_key, sub_key_items)
    else:
        current_app.GlobalManager.remove(primary_key, [{sub_key: sub_value}])