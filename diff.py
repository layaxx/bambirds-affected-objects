def diff(objs_1, objs_2):
    has_changed = []

    for o in objs_1:
        if not o in objs_2:
            has_changed.append(o)

    return has_changed
