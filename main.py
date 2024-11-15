import argparse
import pathlib
from diff import diff
from load_objects import load_objects_from_file, load_shot
from object2 import object2
from output import handle_output
from database import add_case_to_db


def main(args):
    (objs_1, relevant_lines) = load_objects_from_file(args[0])
    (objs_2, _) = load_objects_from_file(args[1])
    shot = load_shot(args[0])

    if len(objs_1) <= 0:
        raise Exception("Failed to load any Objects from file 1")

    not_in_sit_2 = diff(objs_1, objs_2)
    not_in_sit_1 = diff(objs_2, objs_1)

    print("{} items must have been destroyed, {} items must have moved".format(
        len(not_in_sit_2) - len(not_in_sit_1), len(not_in_sit_1)))

    not_in_sit_1_converted = [object2(obj) for obj in not_in_sit_1]

    result = dict([(obj.id, ("unchanged")) for obj in objs_1])
    result["count-destroyed"] = 0
    result["count-moved"] = 0

    affected_ids = []

    for obj_old in not_in_sit_2:
        obj = object2(obj_old)
        try:
            idx = not_in_sit_1_converted.index(obj)
            not_in_sit_1_converted.pop(idx)
            result[obj.id] = "moved"
            result["count-moved"] += 1
            affected_ids.append(obj.id)
            print("Object {} was determined to have moved.".format(obj.id))
        except ValueError:
            result[obj.id] = "destroyed"
            result["count-destroyed"] += 1
            affected_ids.append(obj.id)
            print("Object {} was determined to have been destroyed.".format(obj.id))

    result["count-unchanged"] = len(objs_1) - (result["count-moved"] +
                                               result["count-destroyed"])

    print("{} objects {} moved, {} {} destroyed, {} remain{} in place.".format(
        result["count-moved"],
        "has" if result["count-moved"] == 1 else "have",
        result["count-destroyed"],
        "was" if result["count-destroyed"] == 1 else "were",
        result["count-unchanged"],
        "s" if result["count-unchanged"] == 1 else ""))

    add_case_to_db(result, relevant_lines, affected_ids, shot)

    # this is only the PDF visual debug output
    output_pdf = False
    if output_pdf:
        handle_output(situation_path=args[0],
                      result=result,
                      path_to_bambirds=args[2],
                      debug=args[3])


def get_default_second_path(path):
    try:
        path = str(path)
        split_path = path.split("-")
        split_ending = split_path[1].split(".")
        increased_number = int(split_ending[0]) + 1
        return "-".join(split_path[0:-1]) + "-" + str(increased_number) + "." + split_ending[1]
    except:
        raise Exception(
            "Failed to produce default value for second arg from first arg")


def validate_args(args):

    path_one = pathlib.Path(vars(args).get("situation-before"))

    if not (path_one.exists() and path_one.is_file()):
        raise Exception(
            "Please provide a VALID path to at least one situation")

    path_to_bambirds = pathlib.Path(vars(args).get("bambirds"))

    if not (path_to_bambirds.exists()):
        print("WARNING: Invalid path to bambirds, PDF creation will fail")

    path_two = None
    if vars(args).get("situation_after"):
        path_two = pathlib.Path(vars(args).get("situation_after"))
        if not (path_two.exists() and path_one.is_file()):
            raise Exception(
                "A second path was provided but not valid")
    else:
        path_two = pathlib.Path(get_default_second_path(
            vars(args).get("situation-before")))
        if not (path_two.exists() and path_one.is_file()):
            raise Exception(
                "A second path was not provided and a default could not be found")
    return [path_one, path_two, path_to_bambirds, vars(args).get("debug")]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Compute difference between two situations.')
    parser.add_argument('situation-before', type=pathlib.Path,
                        help='first situation file')

    parser.add_argument("-s", '--situation-after', type=pathlib.Path,
                        help='second situation file', default=False)

    parser.add_argument("-b", '--bambirds', type=pathlib.Path,
                        help='path of bambirds folder', default="../bambirds")

    parser.add_argument("-d", '--debug', type=bool, nargs='?',
                        help='display output of PDF generation', const=True, default=False)

    args = parser.parse_args()

    main(validate_args(args))
