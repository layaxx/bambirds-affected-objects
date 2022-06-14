from parser import parser
import os
import subprocess


def update_material(line, result):
    if line.startswith("hasMaterial"):
        id = get_id(line)
        if result[id] == "moved":
            return f"hasMaterial({get_id(line)}, yellow, 1, 2, 3, 4)."
        if result[id] == "destroyed":
            return f"hasMaterial({get_id(line)}, red, 1, 2, 3, 4)."
    return line


def handle_output(situation_path, result, path_to_bambirds, debug):
    with open(situation_path) as f:
        string = f.read()

    lines = string.splitlines()

    shape_lines = [line for line in lines if line.startswith("shape(")]
    non_shape_lines = [line for line in lines if (not line.startswith(
        "shape(")) and (not line.startswith("situation_name("))]

    # only useful for PDF output
    complete = [update_material(line,
                                result) for line in lines if not line.startswith("situation_name(")]

    lines_have_changed = [line for line in shape_lines if result[get_id(
        line)] in ["moved", "destroyed"]]
    lines_have_not_changed = [line for line in shape_lines if result[get_id(
        line)] == "unchanged"]

    if not os.path.exists('./output'):
        os.makedirs('./output')

    write_file_curried = (lambda lines, postfix: write_single_file(
        situation_path, lines, postfix, path_to_bambirds, debug))

    write_file_curried(non_shape_lines + lines_have_changed,
                       "has-changed")
    write_file_curried(non_shape_lines + lines_have_not_changed,
                       "has-not-changed")
    write_file_curried(complete, "combined")


def write_single_file(situation_path, lines, postfix, path_to_bambirds, debug):

    file_name = os.path.basename(situation_path)
    file = os.path.splitext(file_name)[0]

    content = build_content(lines, file, postfix)
    filename = os.path.join(
        "./output/", file + "-" + postfix + ".pl")

    with open(filename, "w") as f:
        print('writing: ' + filename)
        f.write(content)
    try:
        subprocess.run(
            "swipl -s {}/planner/main.pl draw.pl -- {}".format(
                path_to_bambirds, filename),
            shell=True,
            stdout=None if debug else subprocess.DEVNULL,
            stderr=None if debug else subprocess.DEVNULL)
    except:
        print("Failed to produce PDF Output.")


def build_content(lines, file, postfix):
    return "\n".join(
        lines)\
        + "\nsituation_name('{}-{}').\n".format(file, postfix)


# returns the first argument in a Prolog fact, which usually is the id.
def get_id(line):
    return parser.parseString(line).get("fact")[0][1]
