import argparse
import pathlib
from diff import diff
from load_objects import load_objects_from_file
from output import handle_output


def main(args):
    objs_1 = load_objects_from_file(args[0])
    objs_2 = load_objects_from_file(args[1])

    if len(objs_1) <= 0:
        raise Exception("Failed to load any Objects from file 1")
    if len(objs_2) <= 0:
        raise Exception("Failed to load any Objects from file 2")

    (has_moved, has_not_moved) = diff(objs_1, objs_2)

    handle_output(args[0], has_moved, has_not_moved, args[2], args[3])

    print("{} objects {} moved or were destroyed, {} remain{} in place.".format(
        len(has_moved),
        "has" if len(has_moved) == 1 else "have",
        len(has_not_moved),
        "s" if len(has_not_moved) == 1 else ""))

    if(len(has_moved)):
        if len(has_moved) > 1:
            print("The following items have moved or were destroyed:")
        else:
            print("The following item has moved or wa destroyed:")
        for o in has_moved:
            print(o.id)
    else:
        print("No Objects have moved")


def get_default(path):
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

    path_two = None
    if vars(args).get("situation_after"):
        path_two = pathlib.Path(vars(args).get("situation_after"))
        if not (path_two.exists() and path_one.is_file()):
            raise Exception(
                "A second path was provided but not valid")
    else:
        path_two = pathlib.Path(get_default(
            vars(args).get("situation-before")))
        if not (path_two.exists() and path_one.is_file()):
            raise Exception(
                "A second path was not provided and a default could not be found")
    return [path_one, path_two, vars(args).get("bambirds"), vars(args).get("debug")]


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
