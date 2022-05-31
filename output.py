from parser import parser
import os
import subprocess


def handleOutput(situation_path, have_moved, have_not_moved, path_to_bambirds):
    with open(situation_path) as f:
        string = f.read()

    lines = string.splitlines()

    shape_lines = list(filter(lambda line: line.startswith("shape"), lines))
    non_shape_lines = list(
        filter(lambda line: not line.startswith("shape"), lines))

    have_moved_ids = list(map(lambda obj: obj.id, have_moved))
    have_not_moved_ids = list(map(lambda obj: obj.id, have_not_moved))

    complete = list(map(lambda line:
                        f"hasMaterial({get_id(line)}, red, 1, 2, 3, 4)."
                        if (line.startswith("hasMaterial") and (get_id(line) in have_moved_ids))
                        else line,
                    lines))

    lines_have_moved = list(filter(lambda line: get_id(
        line) in have_moved_ids, shape_lines))
    lines_have_not_moved = list(filter(lambda line: get_id(
        line) in have_not_moved_ids, shape_lines))

    if not os.path.exists('./output'):
        os.makedirs('./output')
    write_single_file(situation_path, non_shape_lines,
                      lines_have_moved, "has-moved", path_to_bambirds)
    write_single_file(situation_path, non_shape_lines,
                      lines_have_not_moved, "has-not-moved", path_to_bambirds)
    write_single_file(situation_path, complete, [],
                      "combined", path_to_bambirds)


def write_single_file(situation_path, non_shape_lines, specific_lines, postfix, path_to_bambirds):

    file_name = os.path.basename(situation_path)
    file = os.path.splitext(file_name)[0]

    cmd_template = "swipl -s {}/planner/main.pl draw.pl -- {}"

    content = build_content(non_shape_lines, specific_lines, file, postfix)
    filename = os.path.join(
        "./output/", file + "-" + postfix + ".pl")
    with open(filename, "w") as f:
        print('writing: ' + filename)
        f.write(content)
    try:
        subprocess.run(
            cmd_template.format(
                path_to_bambirds, filename),
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
    except:
        print("Failed to produce PDF Output.")


def build_content(non_shape_lines, shape_lines, file, postfix):
    return "\n".join(
        list(filter(lambda line: not line.startswith("situation_name("), non_shape_lines))) \
        + "\nsituation_name('{}-{}').\n".format(file, postfix)\
        + "\n".join(shape_lines)


def get_id(line):
    return parser.parseString(line).get("fact")[0][1]
