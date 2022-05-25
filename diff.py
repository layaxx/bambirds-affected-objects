def diff(objs_1, objs_2):
    has_not_moved = []
    has_moved = []

    for o in objs_1:
        if o in objs_2:
            # if second set has an object that is similar enough,
            # we assume it was not affected
            has_not_moved.append(o)
        else:
            has_moved.append(o)

    return (has_moved, has_not_moved)
