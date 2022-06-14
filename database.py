def add_case_to_db(result, relevant_lines, affected_ids):

    database_location = "database.pl"

    with open(database_location, "r") as file:
        last_line = file.readlines()[-1]
        last_line = last_line.strip("% ")
        case_index = int(last_line.strip())

    res = list(filter(lambda line: get_id(line) in (
        affected_ids), relevant_lines))

    new_ids = list(map(lambda old_id: get_new_id(
        old_id, case_index), affected_ids))

    with open(database_location, "a") as file:
        file.write("\n")
        for line in res:
            file.write(replace_id(line, case_index) + "\n")
        file.write("case(c{}, [{}]).\n".format(
            case_index, ",".join(new_ids)))
        for id in affected_ids:
            file.write("effect(c{}, {}, {}).\n".format(case_index,
                                                       get_new_id(
                                                           id, case_index),
                                                       result[id]))
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
