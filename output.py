from parser import parser
import os
import subprocess


def handleOutput(situation_path, have_moved, have_not_moved):
    with open(situation_path) as f:
        string = f.read()

    lines = string.splitlines()

    shape_lines = list(filter(lambda line: line.startswith("shape"), lines))
    non_shape_lines = list(
        filter(lambda line: not line.startswith("shape"), lines))

    have_moved_ids = list(map(lambda obj: obj.id, have_moved))
    have_not_moved_ids = list(map(lambda obj: obj.id, have_not_moved))

    lines_have_moved = list(filter(lambda line: get_id(
        line) in have_moved_ids, shape_lines))
    lines_have_not_moved = list(filter(lambda line: get_id(
        line) in have_not_moved_ids, shape_lines))

    if not os.path.exists('./output'):
        os.makedirs('./output')
    write_single_file(situation_path, non_shape_lines, lines_have_moved, True)
    write_single_file(situation_path, non_shape_lines,
                      lines_have_not_moved, False)


def write_single_file(situation_path, non_shape_lines, specific_lines, has_moved):

    file_name = os.path.basename(situation_path)
    file = os.path.splitext(file_name)[0]

    cmd_template = "swipl -s {}/planner/main.pl draw.pl -- {}"

    path_to_bambirds = "../bambirds"
    content = build_content(non_shape_lines, specific_lines, file, has_moved)
    filename = os.path.join(
        "./output/", file + ("-has-moved.pl" if has_moved else "-has-not-moved.pl"))
    with open(filename, "w") as f:
        f.write(content)
    subprocess.call(cmd_template.format(
        path_to_bambirds, filename), shell=True)


def build_content(non_shape_lines, shape_lines, file, has_moved):
    return "\n".join(list(filter(lambda line: not line.startswith("situation_name("), non_shape_lines))
                     ) + "\nsituation_name('{}-{}').\n".format(file, "has-moved" if has_moved else "has-not-moved") + "\n".join(shape_lines)


def get_id(line):
    return parser.parseString(line).get("fact")[0][1]
