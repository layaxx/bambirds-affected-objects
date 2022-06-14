def add_case_to_db(result, relevant_lines, affected_ids, shot):

    database_location = "database.pl"

    with open(database_location, "r") as file:
        try:
            last_line = file.readlines()[-1]
            last_line = last_line.strip("% ")
            case_index = int(last_line.strip())
        except:
            case_index = 1

    res = list(filter(lambda line: get_id(line) in (
        affected_ids), relevant_lines))

    new_ids = list(map(lambda old_id: get_new_id(
        old_id, case_index), affected_ids))

    with open(database_location, "a") as file:
        if case_index == 1:
            file.write("%1")
        file.write("\n")
        for line in res:
            file.write("case_" + replace_id(line, case_index) + "\n")

        # case(id, target, impact_angle, strategy, bird, [...shot])
        file.write("shot(s{}, {}, {}, {}, {}, {}, [{}]).\n".format(
            case_index,
            shot.get("target_object"),
            shot.get("impact_angle"),
            shot.get("strategy"),
            shot.get("bird"),
            shot.get("target_object"),
            ", ".join(map(str, shot.get("shot").values()))
        ))

        file.write("case(c{}, [{}], s{}).\n".format(
            case_index,
            ",".join(new_ids),
            case_index))

        for id in affected_ids:
            file.write("effect(c{}, {}, {}).\n".format(case_index,
                                                       get_new_id(
                                                           id, case_index),
                                                       result[id]))
        # TODO: write shot to file
        file.write("%" + str(case_index + 1))


def get_id(line):
    line = line.split("(")[1]
    id = line.split(",")[0]

    return id


def replace_id(line, case_index):
    id = get_id(line)
    return line.replace(id, get_new_id(id, case_index))


def get_new_id(old_id, case_index):
    return str(case_index) + "-" + old_id
